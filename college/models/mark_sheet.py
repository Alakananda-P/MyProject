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

    @api.depends('mark_line_ids', 'mark_line_ids.mark')
    def _total_mark(self):
        for record in self:
            total = 0
            for line in record.mark_line_ids:
                total += line.mark
                print(line.mark)
                print(line.pass_fail)
                # if len(line.pass_fail) == len(line.mark):
                #     record['pass_fail'] = True
            record['total_mark'] = total

    # @api.depends('total_mark')
    # def _rank(self):
    #     self.env.cr.execute("""UPDATE college.marksheet SET rank=r.rank FROM
    #     (SELECT name, course, semester, exam, total_mark,
    #     DENSE_RANK() OVER(
    #     ORDER BY total_mark DESC)rank FROM
    #     college.marksheet ORDER BY rank)r WHERE pass_fail = TRUE;""")
    #     self.env.cr.fetchall()

    # @api.onchange('mark_line_ids')
    # def _onchange_pass_fail(self):
        # check = self.mark_line_ids
        # for record in check:
        #     print(record.pass_fail)
        #     if not record.pass_fail:
        #         self.pass_fail = False
        #         print(self.pass_fail)
        #     elif record.pass_fail:
        #         self.pass_fail = True
        #         print(self.pass_fail)

        # marks = self.mark_line_ids
        # for record in marks:
        #     student = self.name
        #     subject = record.subject
        #     mark = record.mark
        #     print(self.name, record.subject, record.mark)
        #     print(student, subject, mark)
        #     print(sum(int(mark)))
            # vals = {
            #     student: self.name,
            #     subject: record.subject,
            #     mark: record.mark
            # }
            # rank={}
            # print("hi", vals)
            # for key, value in vals.items():
            #     smark = sum(vals[key]["mark"])
            #     vals[key].update({"total":smark})
            # s = sorted(vals, key = lambda  x:student[x]["total"], reverse=True)
            # rank=1
            # for key in s:
            #     vals[key].update({"rank":rank})
            #     rank += 1
            # for i in vals.items():
            #     print(i)


class MarksheetMarksLines(models.Model):
    _name = "marksheet.marks.lines"
    _description = "MarkSheet Marks Lines"

    subject = fields.Char(string='Subject')
    mark = fields.Float(string='Mark')
    max_mark = fields.Float(string='Max Mark')
    pass_mark = fields.Float(string='Pass Mark')
    pass_fail = fields.Boolean(string='Pass/Fail')
    mark_id = fields.Many2one('college.marksheet', string='Semester')

    @api.onchange('mark')
    def _onchange_mark(self):
        if self.mark >= self.pass_mark:
            self.pass_fail = True

    # @api.depends('mark')
    # def _subtotal_mark(self):
    #     # for order in self:
    #     #     print(order)
    #     self.subtotal_mark = self.mark
            # print(order.mark_subtotal)

    # def _compute_amount_undiscounted(self):
    #     for order in self:
    #         total = 0.0
    #         for line in order.order_line:
    #             total += line.price_subtotal + line.price_unit * ((line.discount or 0.0) / 100.0) * line.product_uom_qty  # why is there a discount in a field named amount_undiscounted ??
    #         order.amount_undiscounted = total


