# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Manufacturing Order in Bill of Material',
    'version': '14.0.1.0.0',
    'summary': 'Manufacturing Order in Bill of Material Software',
    'sequence': -100,
    'category': 'Hidden',
    'description': """Manufacturing Order in Bill of Material Software""",
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mrp',
    ],
    'data': [
        'views/bom.xml',
    ],
    'demo': [],
    'qweb': [
        'static/src/xml/bom.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
