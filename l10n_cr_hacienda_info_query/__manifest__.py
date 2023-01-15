{
    "name": "Consultar Información en Hacienda",
    'version': '15.1.1.1.1',
    "author": "Julio CRR",
    'license': 'LGPL-3',
    "website": "https://www.facturaodoocr.com",
    "category": "API",
    "summary": """Consulta de nombres directamente al ministerio de Hacienda de Costa Rica""",
    "description": """El Ministerio de Hacienda de Costa Rica pone a dispocisión el servicio API de consulta a partir del número de identificación""",
    "depends": ['base', 'contacts', 'base_setup', 'l10n_cr_country_codes'],
    "data": [
        'views/res_config_settings_views.xml',
        'data/res_config_settings.xml'
    ],
    "installable": True
}
