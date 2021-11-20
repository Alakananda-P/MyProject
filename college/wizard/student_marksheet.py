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
    student_course_id = fields.Char(related='student_id.course',
                                    string='Student Course')
    student_academic_year = fields.Char(related='student_id.academic_year',
                                        string='Student Academic Year')
    class_course_id = fields.Many2one(related='class_id.course_id',
                                      string='Class Course')
    class_academic_year = fields.Selection(related='class_id.academic_year',
                                           string='Class Academic Year')

    def action_print_pdf(self):
        data = {
            'form': self.read()[0]
        }
        if self.marklist == 'student':
            return self.env.ref('college.action_report_student_marksheet'
                                ).report_action(self, data=data)
        elif self.marklist == 'class':
            return self.env.ref('college.action_report_class_marksheet'
                                ).report_action(self, data=data)

