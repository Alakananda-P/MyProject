# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CollegeStudentClass(models.Model):
    _name = "college.student.class"
    _description = "College Student Class"

    name = fields.Char(string='Name')
    semester_id = fields.Many2one('college.semester', string='Semester',
                                  required=True)
    course_id = fields.Many2one('college.course', string='Course',
                                required=True)
    academic_year = fields.Integer(string='Academic Year', required=True)
    student_line_ids = fields.One2many('class.students.lines',
                                       'class_id', string='Students')

    # Name Format
    @api.onchange('semester_id', 'academic_year')
    def class_name(self):
        self.name = str(self.semester_id.name) + ' ' + str(
                self.academic_year)

    # Generate Students in Students Line
    def action_generate(self):
        student = self.env['college.student'].search([
            ('academic_year', '=', self.academic_year),
            ('course', '=', self.course_id.name),
            ('semester', '=', self.semester_id.name)
        ])
        print(student)
        values = [(5, 0, 0)]
        print(values)
        for record in student:
            vals = {
                'name': record.name,
                'email': record.email
            }
            print("hi", vals)
            values.append((0, 0, vals))
            self.student_line_ids = values


class ClassStudentsLines(models.Model):
    _name = "class.students.lines"
    _description = "Class Students Lines"

    name = fields.Char(string='Student')
    email = fields.Char(string='Email')
    class_id = fields.Many2one('college.student.class', string='Class')
