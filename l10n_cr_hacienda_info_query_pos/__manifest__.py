{
    "name": "Consultar  Clientes en Hacienda - Punto de Venta",
    'version': '15.1.1.1.1',
    "author": "Julio CRR",
    'license': 'LGPL-3',
    "website": "https://www.facturaodoocr.com",
    "category": "API",
    "summary": """Consulta de Clientes desde Hacienda""",
    "description": """Consultar directamente a Hacienda un cliente""",
    "depends": ['base', 'contacts', 'point_of_sale', 'l10n_cr_hacienda_info_query'],
    'assets': {
        'point_of_sale.assets': [
            'l10n_cr_hacienda_info_query_pos/static/src/js/actualizar_pos.js',
            'l10n_cr_hacienda_info_query_pos/static/src/js/models.js',
            'l10n_cr_hacienda_info_query_pos/static/src/js/Screens/ClientListScreen/ClientDetailsEdit.js'
        ],
        'web.assets_qweb': [
            'l10n_cr_hacienda_info_query_pos/static/src/xml/**/*',
        ]
    },
    "installable": True
}
