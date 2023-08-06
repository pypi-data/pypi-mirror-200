This module allows you to export Odoo calendar events to an external webcal (such as Nextcloud) for each user. Users can provide their webcal URL and credentials in their user profile, and the module will automatically export events created within the last hour. A scheduled action runs hourly to check for recent events and export them to the corresponding user's webcal.

Updated or deleted events trigger an update or deletion in the webcal.

**Note:** This module is not really synchronizing events, but rather exporting them to a webcal. This means that events created in the webcal will not be imported back into Odoo.
