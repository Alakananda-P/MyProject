# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'College Management',
    'version': '14.0.1.0.0',
    'summary': 'College Management Software',
    'sequence': -100,
    'category': 'Hidden',
    'description': """College Management Software""",
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/mail_template_reject.xml',
        'data/mail_template_admission.xml',
        'data/cron.xml',
        'views/student.xml',
        'views/admission.xml',
        'views/course.xml',
        'views/semester.xml',
        'views/exam.xml',
        'views/student_class.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
