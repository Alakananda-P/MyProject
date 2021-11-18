# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentMarksheetWizard(models.TransientModel):
    _name = "student.marksheet.wizard"
    _description = "Student Marksheet Wizard"

    marklist = fields.Selection([
        ('student', 'Student'), ('class', 'Class')], 'MarkList')
    student_id = fields.Many2one('college.student', string='Student')
    class_id = fields.Many2one('college.student.class', string='Class')
    semester_id = fields.Many2one('college.semester', string='Semester')
    exam_id = fields.Many2one('college.exam', string='Exam Type Id')
    exam_type_id = fields.Selection(related='exam_id.type', string='Exam Type')

    def action_print_pdf(self):
        print("Hello")

