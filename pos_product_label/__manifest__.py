# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'POS Product Label',
    'version': '14.0.1.0.0',
    'summary': 'POS Product Label Software',
    'sequence': -100,
    'category': 'Hidden',
    'description': """POS Product Label Software""",
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
        'product',
    ],
    'data': [
        'views/product_label.xml',
        'views/assets.xml',
    ],
    'demo': [],
    'qweb': [
        'static/src/xml/product_label.xml',
        'static/src/xml/receipt_label.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
