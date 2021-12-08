# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Website Buy Now',
    'version': '14.0.1.0.0',
    'summary': 'Website Buy Now Software',
    'sequence': -100,
    'category': 'Hidden',
    'description': """Website Buy Now on Shop Software""",
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'website_sale',
    ],
    'data': [
        'views/templates.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
