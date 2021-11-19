# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class CollegeExam(models.Model):
    _name = "college.exam"
    _description = "College Exam"

    name = fields.Char(string='Name')
    type = fields.Selection([
        ('internal', 'Internal'),
        ('semester', 'Semester'),
        ('unit_test', 'Unit Test')
    ], string='Type', default='semester')
    class_id = fields.Many2one('college.student.class', string='Class')
    semester_id = fields.Many2one(related='class_id.semester_id',
                                  string='Semester')
    course_id = fields.Many2one(related='class_id.course_id', string='Course')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('completed', 'Completed')
    ], default='draft', string='Status')
    paper_line_ids = fields.One2many('exam.paper.lines', 'exam_id',
                                     string='Papers')
    valuation_count = fields.Integer(string='Valuation Count')
    marksheet_ids = fields.Many2many('college.marksheet', 'marksheet_id',
                                     string='Student Name')
    valuation_completed = fields.Boolean(string='Valuation Completed')

    def name_get(self):
        result = []
        for rec in self:
            rec.name = str(rec.type) + ': ' + str(
                rec.semester_id.name) + ' ' + str(rec.course_id.name)
            result.append((rec.id, rec.name))
        return result

    @api.onchange('class_id')
    def _onchange_type_semester_course(self):
        # self.name = str(self.type) + ': ' + str(
        #     self.semester_id.name) + ' ' + str(self.course_id.name)
        # Generate Paper Line Based on a Field
        if self.type == 'semester':
            semester = self.semester_id.syllabus_line_ids
            values = [(5, 0, 0)]
            for record in semester:
                vals = {
                    'subject': record.subject,
                    'max_mark': record.max_mark
                }
                values.append((0, 0, vals))
                self.paper_line_ids = values

    # State is Changed Based on End Date
    def test_cron_job(self):
        for record in self.search([('state', '!=', 'completed')]):
            if record.end_date and record.end_date == fields.Date.today():
                record.write({'state': 'completed'})

    def action_valuation_completed(self):
        self.valuation_completed = True
        # values = [(5, 0, 0)]
        student = self.env['college.marksheet'].search([])
        for record in student:
            vals = {
                'check_valuation_completed': record.check_valuation_completed,
            }
            vals.update({'check_valuation_completed': self.valuation_completed})
            student.write(vals)
        next_class_id = self.class_id.next_class.name
        pass_stud = self.env['college.marksheet'].search([
            ('pass_fail', '=', True),
        ])
        for record in pass_stud:
            pass_stud_name = {
                'name': record.name
            }
            print(pass_stud_name)
            student_name = self.env['college.student'].search([
                ('name', '=', pass_stud_name.get('name'))
            ])
            print(student_name)
            next_class = {
                'next_class': next_class_id,
            }
            print(next_class)
            student_name.write(next_class)
        fail_stud = self.env['college.marksheet'].search([
            ('pass_fail', '=', False),
        ])
        same_class_id = self.class_id.name
        for record in fail_stud:
            fail_stud_name = {
                'name': record.name
            }
            print(fail_stud_name)
            student_name = self.env['college.student'].search([
                ('name', '=', fail_stud_name.get('name'))
            ])
            print(student_name)
            same_class = {
                'next_class': same_class_id,
            }
            print(same_class)
            student_name.write(same_class)

    @api.model
    def _compute_line_data(self, line):
        return {
            'subject': line.subject,
            'max_mark': line.max_mark,
            'pass_mark': line.pass_mark
        }

    def data_line(self):
        order_lines = [(5, 0, 0)]
        for line in self.paper_line_ids:
            data = self._compute_line_data(line)
            order_lines.append((0, 0, data))
        return order_lines

    def action_generate(self):
        self.valuation_count = len(self.class_id.student_line_ids)
        # Generate MarkSheet Line
        data = self.data_line()
        student = self.class_id.student_line_ids
        values = [(5, 0, 0)]
        for record in student:
            vals = {
                'name': record.name,
                'exam': self.name,
                'classes': self.class_id.name,
                'course': self.class_id.course_id.name,
                'semester': self.class_id.semester_id.name,
                'mark_line_ids': data,
            }
            print("hi", vals)
            values.append((0, 0, vals))
        print(values)
        self.marksheet_ids = values
        # Marks Line
        # data = self.data_line()
        # res = self.env['college.marksheet'].create({
        #     'mark_line_ids': data
        # })

    # Valuation Smart Button
    def action_open_valuation(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Valuations',
            'res_model': 'college.marksheet',
            'domain': [('classes', '=', self.class_id.name)],
            'view_mode': 'tree,form',
            'target': 'current',
        }


class ExamPaperLines(models.Model):
    _name = "exam.paper.lines"
    _description = "Exam Paper Lines"

    subject = fields.Char(string='Subject', required=True)
    pass_mark = fields.Float(string='Pass Mark')
    max_mark = fields.Float(string='Maximum Marks')
    exam_id = fields.Many2one('college.exam', string='Exam')
