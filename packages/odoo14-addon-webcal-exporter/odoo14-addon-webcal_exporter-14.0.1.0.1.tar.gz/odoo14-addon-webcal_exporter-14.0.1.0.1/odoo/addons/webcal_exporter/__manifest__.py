{
    'name': 'Webcal Exporter',
    'version': '14.0.1.0.1',
    'category': 'Extra Tools',
    'summary': 'Export Odoo calendar events to external webcal',
    'author': 'Coopdevs',
    'website': 'https://coopdevs.org',
    'license': 'AGPL-3',
    'depends': ['base', 'calendar'],
    'data': [
        'data/ir_cron_data.xml',
        'views/res_users_view.xml',
    ],
    'external_dependencies': {
        'python': ['ics', 'requests', 'pytz'],
    },
    'installable': True,
    'application': False,
}
