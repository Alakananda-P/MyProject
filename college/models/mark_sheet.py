# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CollegeMarksheet(models.Model):
    _name = "college.marksheet"
    _description = "College MarkSheet"

    name = fields.Char(string='Student Name')
    exam = fields.Char(string='Exam')
    classes = fields.Char(string='Class')
    course = fields.Char(string='Course')
    semester = fields.Char(string='Semester')
    pass_fail = fields.Boolean(string='Pass/Fail')
    rank = fields.Integer(string='Rank')
    marksheet_id = fields.Many2one('college.exam', string='Exam')
    mark_line_ids = fields.One2many('marksheet.marks.lines',
                                    'mark_id', string='Marks')
    total_mark = fields.Float(string='Total Mark', compute='_total_mark')
    check_valuation_completed = fields.Boolean(string='Valuation Completed or Not')

    # Calculate Total Mark
    @api.depends('mark_line_ids', 'mark_line_ids.mark')
    def _total_mark(self):
        for record in self:
            total = 0
            for line in record.mark_line_ids:
                total += line.mark
            record['total_mark'] = total

    @api.onchange('mark_line_ids', 'mark_line_ids.mark')
    # Check Pass or Fail
    def _pass_fail(self):
        check = self.mark_line_ids
        flag = 1
        for record in check:
            if not record.pass_fail:
                flag = 0
        if flag == 0:
            self.pass_fail = False
        else:
            self.pass_fail = True

    # Set Rank
    @api.onchange('mark_line_ids')
    def _rank(self):
        student = self.search([
            ('course', '=', self.course),
            ('semester', '=', self.semester),
            ('exam', '=', self.exam)
        ])
        values = []
        for rec in student:
            vals = {
                'id': rec.id,
                'name': rec.name,
                'total_mark': rec.total_mark
            }
            values.append(vals)
        sort_mark = sorted(values, key=lambda x: x['total_mark'], reverse=True)
        rank = 1
        for key in sort_mark:
            key.update({'ranks': rank})
            search_id = self.search([('id', '=', key.get('id'))])
            search_id.rank = rank
            rank += 1


class MarksheetMarksLines(models.Model):
    _name = "marksheet.marks.lines"
    _description = "MarkSheet Marks Lines"

    subject = fields.Char(string='Subject')
    mark = fields.Float(string='Mark')
    max_mark = fields.Float(string='Max Mark')
    pass_mark = fields.Float(string='Pass Mark')
    pass_fail = fields.Boolean(string='Pass/Fail')
    mark_id = fields.Many2one('college.marksheet', string='Semester')
    check_valuation_complete = fields.Boolean(
        related='mark_id.check_valuation_completed')

    # Check Pass or Fail
    @api.onchange('mark')
    def _onchange_mark(self):
        if self.mark >= self.pass_mark:
            self.pass_fail = True
        else:
            self.pass_fail = False
