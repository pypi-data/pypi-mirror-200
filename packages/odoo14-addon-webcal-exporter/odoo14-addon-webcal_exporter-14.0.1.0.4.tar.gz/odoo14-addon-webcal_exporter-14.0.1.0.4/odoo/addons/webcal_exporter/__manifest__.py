{
    'name': 'Webcal Exporter',
    'version': '14.0.1.0.4',
    'category': 'Extra Tools',
    'summary': 'Export Odoo calendar events to external webcal',
    'author': 'Coopdevs',
    'website': 'https://coopdevs.org',
    'license': 'AGPL-3',
    'depends': ['base', 'calendar'],
    'data': [
        'data/ir_cron_data.xml',
        'data/ir_actions_server_data.xml',
        'views/res_users_view.xml',
        'security/ir.model.access.csv',
    ],
    'external_dependencies': {
        'python': ['ics', 'requests', 'pytz', 'caldav'],
    },
    'installable': True,
    'application': False,
}
