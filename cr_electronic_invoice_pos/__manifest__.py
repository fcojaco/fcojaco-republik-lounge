{
    'name': 'Facturación electrónica para Costa Rica Punto de Venta - FACTURAODOOCR.COM',
    'version': '15.0.1.0.0',
    'author': 'Julio CRR',
    'license': 'OPL-1',
    'website': 'http://www.facturaodoocr.com',
    'category': 'Account',
    'description':
    '''
    Facturación electronica para Costa Rica. Actualización módulo Punto de Venta (POS)
    ''',
    'depends': [
        'cr_electronic_invoice',
        'point_of_sale'
    ],
    'data': [
        'views/electronic_invoice_views.xml',
        'data/data.xml',
        'data/payment_methods_data.xml',
        'views/pos_payment_method.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'cr_electronic_invoice_pos/static/src/js/models.js'
        ],
        'web.assets_qweb': [
            'cr_electronic_invoice_pos/static/src/xml/**/*'
        ]
    },
    "qweb": [
        "static/src/xml/pos.xml"
    ],
    'installable': True,
}
