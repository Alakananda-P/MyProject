# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Website Stock',
    'version': '14.0.1.0.0',
    'summary': 'Website Stock Availablility Software',
    'sequence': -100,
    'category': 'Hidden',
    'description': """Website Stock Availablility Software""",
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/stock_availability.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
