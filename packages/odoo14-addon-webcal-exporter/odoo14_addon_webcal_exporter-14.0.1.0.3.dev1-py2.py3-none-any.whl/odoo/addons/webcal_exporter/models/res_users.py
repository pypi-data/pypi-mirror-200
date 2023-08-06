from odoo import fields, models
from odoo import api, fields, models
from odoo.exceptions import UserError
from requests.auth import HTTPBasicAuth
from ics import Calendar, Event
from datetime import datetime, timedelta
import logging
import pytz
import requests
import uuid

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    calendar_url = fields.Char(string='Calendar URL')
    calendar_user = fields.Char(string='Calendar User')
    calendar_password = fields.Char(string='Calendar Password')
    calendar_credentials_verified = fields.Boolean(
        string="Calendar Credentials Verified", default=False
    )

    @api.onchange('calendar_url')
    def _onchange_calendar_url(self):
        self.write({'calendar_credentials_verified': False})
    
    @api.onchange('calendar_user')    
    def _onchange_calendar_user(self):
        self.write({'calendar_credentials_verified': False})

    @api.onchange('calendar_password')
    def _onchange_calendar_password(self):
        self.write({'calendar_credentials_verified': False})


    def check_calendar_credentials(self):
        self.ensure_one()
        if not (self.calendar_url and self.calendar_user and self.calendar_password):
            _logger.warning(
                "Missing calendar URL, user, or password for user %s.", self.login)
            raise UserError(
                "Please provide the calendar URL, user, and password.")
        url = self.calendar_url.rstrip('/')
        success = self.check_credentials(url, self.calendar_user, self.calendar_password)
        self.write({'calendar_credentials_verified': success})
        if  (not success):
            raise UserError("Invalid calendar credentials. Please check the URL, user, and password.")

    def check_credentials(self, url, user, password):
        headers = {
            'Content-Type': 'application/xml',
            'Depth': '0',
        }

        body = '''<?xml version="1.0" encoding="utf-8" ?>
        <propfind xmlns="DAV:">
            <prop>
                <displayname/>
            </prop>
        </propfind>
        '''

        try:
            response = requests.request(
                'PROPFIND', url, headers=headers, data=body, auth=HTTPBasicAuth(user, password), timeout=10
            )
            _logger.debug("Response: %s %s" %
                          (response.status_code, response.reason))

            if response.status_code == 207:
                return True
            elif response.status_code == 400:
                _logger.error("Bad Request: %s", response.text)
                return False
            else:
                _logger.error("Unexpected response status code: %d",
                              response.status_code)
                return False

        except requests.exceptions.RequestException as e:
            _logger.exception("Error while checking credentials: %s", str(e))
            return False

    def _publish_ical_event(self, url, user, password, calendar):
        headers = {
            'Content-Type': 'text/calendar',
            'User-Agent': 'Python-Requests',
        }
        _logger.debug("Publishing event to %s" % url)
        try:

            response = requests.put(url, auth=(user, password),
                                    headers=headers, data=calendar.serialize())
        except:
            return False
        if response.status_code in [201, 204]:
            return True
        else:
            _logger.error("Error publishing event:" %
                          (response.status_code, response.reason))
            return False

    def export_recent_events(self):
        env = self.env
        # Calculate the date and time of one hour ago
        one_hour_ago = datetime.now() - timedelta(hours=1)

        # Search for events created in the last hour
        events = env['calendar.event'].search([
            ('create_date', '>=', one_hour_ago.strftime('%Y-%m-%d %H:%M:%S')),
        ])
        _logger.debug("Found %s events to export" % len(events))
        # Publish each event to the corresponding user's external calendar
        for event_id in events:
            _logger.debug("Exporting event %s" % event_id.id)
            event = env['calendar.event'].browse(event_id.id)
            if event.external_uuid:
                _logger.debug("Event %s already exported" % event_id.id)
                continue
            event_uuid = str(uuid.uuid4())
            for partner in event.partner_ids:
                user = env['res.users'].search(
                    [('partner_id', '=', partner.id)], limit=1)
                if user.calendar_credentials_verified:
                    # Convert the event start and end times to the user's timezone
                    user_tz = pytz.timezone(user.tz or 'UTC')
                    event_start = pytz.utc.localize(
                        event.start).astimezone(user_tz)
                    event_end = pytz.utc.localize(
                        event.stop).astimezone(user_tz)
                    # If the user has the necessary information for their calendar, try to publish the event
                    if  user.calendar_url and user.calendar_user and user.calendar_password:
                        calendar = Calendar()
                        ics_event = Event()
                        ics_event.name = event.name
                        ics_event.begin = event_start
                        ics_event.end = event_end
                        ics_event.uid = event_uuid
                        calendar.events.add(ics_event)
                        event_url = user.calendar_url + ics_event.uid + ".ics"
                        try:
                            self._publish_ical_event(
                                event_url, user.calendar_user, user.calendar_password, calendar)
                            event.external_uuid = event_uuid
                            event._origin.write({'external_uuid': event_uuid})
                        except Exception as e:
                            _logger.error("Error publishing event to %s" % event_url)
                            event.add_unsynced_tag()
