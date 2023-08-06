import requests
import caldav
import logging

from calendar import Calendar
from requests.auth import HTTPBasicAuth
from odoo import models, fields, api
from datetime import datetime
from pytz import timezone
from icalendar import Calendar, vDatetime

_logger = logging.getLogger(__name__)

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    external_uuid = fields.Char(string='External UUID')

    def add_unsynced_tag(self):
        unsynced_tag_name = '#unsynced'
        category = self.env['calendar.event.type']
        unsynced_tag = category.search([('name', '=', unsynced_tag_name)])
        if not unsynced_tag:
            unsynced_tag = category.create({'name': unsynced_tag_name})
        self.categ_ids = [(4, unsynced_tag.id)]

    def update_event_in_external_calendar(self):
        for event in self:
            # Obtén los asistentes al evento antes y después de la actualización
            partner_before_update = event._origin.partner_id
            partner_after_update = event.partner_id
            all_partners = partner_before_update | partner_after_update

            for partner in all_partners:
                user = self.env['res.users'].search(
                    [('partner_id', '=', partner.id)], limit=1)
                if not user or not user.calendar_credentials_verified:
                    continue
                client = caldav.DAVClient(
                    url=user.calendar_url, username=user.calendar_user, password=user.calendar_password)
                principal = client.principal()
                calendars = principal.calendars()

                if calendars:
                    calendar = calendars[0]

                    external_event = calendar.event_by_uid(event.external_uuid)
                    if external_event:
                        ical = Calendar.from_ical(external_event.data)
                        ical_event = ical.walk('VEVENT')[0]
                        ical_event['SUMMARY'] = event.name
                        ical_event['DTSTART'] = vDatetime(event.start.replace(tzinfo=timezone('UTC')))
                        ical_event['DTEND'] = vDatetime(event.stop.replace(tzinfo=timezone('UTC')))
                        ical_event['LOCATION'] = event.location or ''
                        ical_event['DESCRIPTION'] = event.description or ''                        # Update the event in the external calendar
                        external_event.data = ical.to_ical()
                        external_event.save(no_overwrite=False)

    def delete_event_in_external_calendar(self):
        for event in self:
            if not event.external_uuid:
                continue

            partner = event.partner_id
            user = self.env['res.users'].search(
                [('partner_id', '=', partner.id)], limit=1)

            if not user or not user.calendar_credentials_verified:
                continue
            base_url = user.calendar_url
            calendar_user = user.calendar_user
            calendar_password = user.calendar_password
            user_sync = user.calendar_credentials_verified

            if base_url and calendar_user and calendar_password and user_sync:
                event_url = base_url + event.external_uuid + ".ics"
                try:
                    self._delete_ical_event(
                        event_url, calendar_user, calendar_password)
                except Exception as e:
                    _logger.error(
                        "Error deleting event from external calendar: %s", str(e))
                    event.add_unsynced_tag()

    def _delete_ical_event(self, event_url, calendar_user, calendar_password):
        try:
            response = requests.request(
                'DELETE', event_url, auth=HTTPBasicAuth(calendar_user, calendar_password), timeout=10
            )
            _logger.debug("Response: %s %s" %
                          (response.status_code, response.reason))
            if response.status_code not in (204, 404):
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.error("Error deleting event: %s %s" %
                          (response.status_code, response.reason))
            raise e
