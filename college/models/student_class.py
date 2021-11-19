# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class CollegeStudentClass(models.Model):
    _name = "college.student.class"
    _description = "College Student Class"

    name = fields.Char(string='Name')
    semester_id = fields.Many2one('college.semester', string='Semester',
                                  required=True)
    course_id = fields.Many2one(related='semester_id.course_id',
                                string='Course', required=True)
    academic_year = fields.Selection([(str(num), str(num)) for num in range(
        1900, (datetime.now().year)+1)], 'Academic Year', required=True)
    student_line_ids = fields.One2many('class.students.lines',
                                       'class_id', string='Students')
    next_class = fields.Many2one('college.student.class', string='Next Class')
    # next_class = fields.Char(string='Next Class')
    sem_no = fields.Integer(string='Number Semester')

    # Name Format
    # @api.onchange('semester_id', 'academic_year')
    # def class_name(self):
    #     self.name = str(self.semester_id.name) + ' ' + str(
    #             self.academic_year)

    def name_get(self):
        result = []
        for rec in self:
            rec.name = str(rec.semester_id.name) + ' ' + str(rec.academic_year)
            result.append((rec.id, rec.name))
        return result

    # Generate Students in Students Line
    def action_generate(self):
        student = self.env['college.student'].search([
            ('academic_year', '=', self.academic_year),
            ('course', '=', self.course_id.name),
            ('semester', '=', self.semester_id.name)
        ])
        values = [(5, 0, 0)]
        for record in student:
            vals = {
                'name': record.name,
                'id': record.id
            }
            values.append((0, 0, vals))
            self.student_line_ids = values

    # @api.onchange('name')
    # def _next_class(self):
    #     no_semester = self.semester_id.no_semester
    #     self.sem_no = no_semester + 1
    #     no = self.env['college.semester'].search([
    #         ('no_semester', '=', self.sem_no)
    #     ])
    #     vals = {}
    #     for record in no:
    #         vals = {
    #             'next_class': record.name,
    #         }
    #     sem = vals.get('next_class')
    #     if self.academic_year != 0:
    #         academic_month = datetime.strptime(str(self.academic_year),
    #                                            '%Y-%m-%d').strftime('%m')
    #         academic_year = datetime.strptime(str(self.academic_year),
    #                                           '%Y-%m-%d').year
    #         date = int(academic_month) + 6
    #         if date > 12:
    #             year = academic_year + 1
    #             difference = date - 12
    #             month = 0
    #             months = month + difference
    #             if months < 10:
    #                 zero_filled_months = str(months).zfill(2)
    #                 self.next_class = sem + ' ' + str(year) + '-' + str(
    #                     zero_filled_months)
    #             else:
    #                 self.next_class = sem + ' ' + str(year) + '-' + str(months)
    #         else:
    #             if date < 10:
    #                 zero_filled_months = str(date).zfill(2)
    #                 self.next_class = sem + ' ' + str(
    #                     academic_year) + '-' + str(zero_filled_months)
    #             else:
    #                 self.next_class = sem + ' ' + str(
    #                     academic_year) + '-' + str(date)


class ClassStudentsLines(models.Model):
    _name = "class.students.lines"
    _description = "Class Students Lines"

    name = fields.Char(string='Student')
    id = fields.Integer(string='Id')
    class_id = fields.Many2one('college.student.class', string='Class')
