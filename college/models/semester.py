# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CollegeSemester(models.Model):
    _name = "college.semester"
    _description = "College Semester"
    # _rec_name = "course_id"

    name = fields.Char(string='Name')
    no_semester = fields.Integer(string='No of Semester', required=True)
    course_id = fields.Many2one('college.course', string='Course',
                                required=True)
    syllabus_line_ids = fields.One2many('semester.syllabus.lines',
                                        'semester_id', string='Syllabus')

    # Name Format
    @api.onchange('no_semester', 'course_id')
    def _semester_name(self):
        self.name = str(self.no_semester) + 'Sem: ' + str(self.course_id.name)


class SemesterSyllabusLines(models.Model):
    _name = "semester.syllabus.lines"
    _description = "Semester Syllabus Lines"

    subject = fields.Char(string='Subject', required=True)
    max_mark = fields.Float(string='Maximum Marks')
    semester_id = fields.Many2one('college.semester', string='Semester')
