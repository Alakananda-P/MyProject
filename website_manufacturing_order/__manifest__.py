# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Website Manufacturing Order',
    'version': '14.0.1.0.0',
    'summary': 'Website Manufacturing Order Software',
    'sequence': -100,
    'category': 'Hidden',
    'description': """Website Manufacturing Order Software""",
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'portal',
        'mrp',
        'contacts',
        'base',
        'product',
        # 'mrp_portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/website_mo_security.xml',
        'views/portal_template.xml',
        'views/mo_customer.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
