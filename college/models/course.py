# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CollegeCourse(models.Model):
    _name = "college.course"
    _description = "College Course"

    name = fields.Char(string='Name', required=True)
    category = fields.Selection([
        ('ug', 'Under Graduate'),
        ('pg', 'Post Graduate'),
        ('diploma', 'Diploma')
    ], string='Category')
    duration_year = fields.Integer(string='Duration in Year')
    no_semester = fields.Integer(string='No of Semester')
    semester_ids = fields.One2many('college.semester', 'course_id',
                                   string='Semester')
    currency_id = fields.Many2one('res.currency', string='Currency')
    fee = fields.Monetary(string='Fees')
