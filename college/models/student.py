# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CollegeStudent(models.Model):
    _name = "college.student"
    _description = "College Student"

    adm_no = fields.Char(string='Admission No')
    adm_date = fields.Date(string='Admission Date')
    name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    father_name = fields.Char(string='Father Name')
    mother_name = fields.Char(string='Mother Name')
    com_address = fields.Text(string='Communication Address')
    same_com_address = fields.Boolean(string='Same as Communication Address')
    per_address = fields.Text(string='Permanent Address')
    phone_no = fields.Char(string='Phone No')
    email = fields.Char(string='Email')
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    academic_year = fields.Integer(string='Academic Year')
    course = fields.Char(string='Course')
    semester = fields.Char(string='Semester')
    classes = fields.Char(string='Class')
