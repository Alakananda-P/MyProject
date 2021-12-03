# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'POS Purchase Limit',
    'version': '14.0.1.0.0',
    'summary': 'POS Purchase Limit Software',
    'sequence': -100,
    'category': 'Hidden',
    'description': """POS Purchase Limit Software""",
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
        'product',
        'contacts',
        'base',
    ],
    'data': [
        'views/purchase_limit.xml',
        'views/assets.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
