# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime


class CollegeAdmission(models.Model):
    _name = "college.admission"
    _description = "College Admission"

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last name')
    name = fields.Char(string="Admission No", required=True, copy=False,
                       readonly=True, default=lambda self: 'New')
    father_name = fields.Char(string='Father Name')
    mother_name = fields.Char(string='Mother Name')
    com_address = fields.Text(string='Communication Address')
    same_com_address = fields.Boolean(string='Same as Communication Address')
    per_address = fields.Text(string='Permanent Address')
    phone_no = fields.Char(string='Phone No')
    email = fields.Char(string='Email', required=True)
    date_app = fields.Date(string='Date of Application')
    academic_year = fields.Char(string='Academic Year', required=True)
    prev_edu_qualification = fields.Selection([
        ('hse', 'Higher Secondary'),
        ('ug', 'UG'),
        ('pg', 'PG')
    ], string='Previous Educational Qualification')
    edu_institute = fields.Char(string='Educational Institute')
    tran_certificate = fields.Binary(string='Transfer Certificate')
    course_id = fields.Many2one('college.course', string='Course',
                                required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('application', 'Application'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected')
    ], default='draft', string='Status')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    admission_date = fields.Date(string='Admission Date')
    semester_id = fields.Many2one('college.semester', string='Semester',
                                  required=True)
    class_id = fields.Many2one('college.student.class', string='Class',
                               required=True)

    @api.depends('tran_certificate')
    def action_confirm(self):
        # State Check & Move
        if self.state == 'draft':
            self.state = 'application'
            # Set Warning
            if self.tran_certificate == 0:
                raise UserError("Please Add Attachment")
        # State Check & Move
        elif self.state == 'application':
            self.state = 'done'
            # Sequence
            self.name = self.env['ir.sequence'].next_by_code(
                'college.admission') or 'New'
            # Current Date
            self.admission_date = datetime.today()
            # Create Record in Student Model
            vals = {
                'adm_no': self.name,
                'adm_date': self.admission_date,
                'name': self.first_name,
                'last_name': self.last_name,
                'father_name': self.father_name,
                'mother_name': self.mother_name,
                'com_address': self.com_address,
                'same_com_address': self.same_com_address,
                'per_address': self.per_address,
                'phone_no': self.phone_no,
                'email': self.email,
                'academic_year': self.academic_year,
                'course': self.course_id.name,
                'semester': self.semester_id.name,
                'classes': self.class_id.name
            }
            self.env['college.student'].create(vals)
            # Send Email for Admission
            self.env.ref('college.admission_application_email_template'
                         ).send_mail(self.id, force_send=True)

    def action_approve(self):
        self.state = 'approved'

    def action_draft(self):
        self.state = 'draft'

    def action_reject(self):
        self.state = 'rejected'
        # Send Email for Rejection
        self.env.ref('college.admission_reject_email_template').send_mail(
            self.id, force_send=True)
