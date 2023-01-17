# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Point Of Sale Multi Currency Pricelist",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Point Of Sale",
    "license": "OPL-1",
    "summary": "POS Different Currency POS Multi-Currency Point Of Sale Multi Pricelist Point Of Sale Various Currency Pricelist POS Multi-Currency Payment POS Multiple Currency Pricelist POS Pricelist Management POS Multi Currency Pricelist Odoo",
    "description": """By default, odoo provides only a single currency in the POS. This module supports a multi-currency pricelist in the point of sale. If the user selects the different currency's pricelist then pricelist currency and price changed based on the currency. You can print a POS receipt with a different currency.Point Of Sale Multi Currency Pricelist Odoo, POS Different Currency, Point Of Sale Multi Pricelist, POS Multi-Currency Payment, POS Multiple Currency Module, Point Of Sale Various Currency Pricelist, Allow Multi Currencies Pricelist In POS, POS Pricelist Management Odoo,POS Different Currency, POS Multi-Currency App, Point Of Sale Multi Pricelist,  Point Of Sale Various Currency Pricelist, POS Multi-Currency Payment, POS Multiple Currency Modulet, POS Pricelist Management Odoo""",
    "version": "15.0.3",
    "depends": ["point_of_sale"],
    "application": True,
    'assets': {'point_of_sale.assets': ['sh_pos_multi_pricelist/static/src/js/pos.js',
                                        'sh_pos_multi_pricelist/static/src/css/pos.css', ],
                'web.assets_qweb': ['sh_pos_multi_pricelist/static/src/xml/pos.xml']
            },
    "auto_install": False,
    "installable": True,
    "price": 35,
    "currency": "EUR",
    "images": ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/4M0J6kHFsMA",
}
