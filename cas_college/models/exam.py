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
    valuation_count = fields.Integer(string='Valuation Count',
                                     compute='_compute_valuation_count')

    # Name Format
    @api.onchange('type', 'semester_id', 'course_id')
    def _onchange_type_semester_course(self):
        self.name = str(self.type) + ': ' + str(
            self.semester_id.name) + ' ' + str(self.course_id.name)
        # Generate Paper in Paper Line Based on a Field
        if self.type == 'semester':
            print(self.semester_id)
            semester = self.semester_id.syllabus_line_ids
            print(semester)
            values = [(5, 0, 0)]
            # print(values)
            for record in semester:
                vals = {
                    'subject': record.subject,
                    'max_mark': record.max_mark
                }
                print("hi", vals)
                values.append((0, 0, vals))
                self.paper_line_ids = values

    # State is Changed Based on End Date
    def test_cron_job(self):
        for record in self.search([('state', '!=', 'completed')]):
            print(record)
            if record.end_date and record.end_date == fields.Date.today():
                print(record)
                record.write({'state': 'completed'})

    def _compute_valuation_count(self):
        for record in self:
            valuation_count = self.env['college.student'].search_count(
                [('name', '=', record.id)])
            record.valuation_count = valuation_count

    def action_open_valuation(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Valuations',
            'res_model': 'college.student',
            'domain': [('name', '=', self.name)],
            'view_mode': 'tree,form',
            'target': 'current',
        }


class ExamPaperLines(models.Model):
    _name = "exam.paper.lines"
    _description = "Exam Paper Lines"

    subject = fields.Char(string='Subject', required=True)
    pass_mark = fields.Integer(string='Pass Mark')
    max_mark = fields.Integer(string='Maximum Marks')
    exam_id = fields.Many2one('college.exam', string='Exam')
