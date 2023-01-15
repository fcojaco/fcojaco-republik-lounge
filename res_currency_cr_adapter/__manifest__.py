# copyright 2023 Julio CRR
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Tipo de cambio automático - Costa Rica',
    'version': '15.0.1.0.0',
    'category': 'Account',
    'author': "Julio CRR",
    'website': 'https://www.facturaodoocr.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account'
    ],
    'data': [
        'data/currency_data.xml',
        'views/res_currency_view.xml',
        'views/res_currency_rate_view.xml',
        'views/res_config_settings_views.xml',
    ],
    'external_dependencies': {'python': ['zeep']},
    'installable': True,
    'auto_install': False,
}
