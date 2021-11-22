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
        # args = {
        #     'student_id': self.student_id.id,
        #     'class_id': self.class_id.id,
        #     'semester_id': self.semester_id.id,
        #     'exam_id': self.exam_id.id,
        # }
        # print("args", args)
        # self.env.cr.execute("""SELECT cm.name as student,
        #                         m.subject as subject,
        #                         m.mark as mark,
        #                         m.pass_mark as passmark,
        #                         m.pass_fail as pass_fail
        #                     FROM college_marksheet cm
        #                     LEFT OUTER JOIN marksheet_marks_lines m ON(
        #                         cm.mark_line_ids = m.mark_id)
        #                     WHERE(cm.name = %(student_id)s
        #                     AND m.semester = %(semester_id)s )""", args)
        # result = self.env.cr.dictfetchall()
        # print(result)
        if self.marklist == 'student':
            marksheet = self.env['college.marksheet'].search([
                ('name', '=', self.student_id.name),
                ('semester', '=', self.semester_id.name),
                ('exam', '=', self.exam_id.name)
            ])
            result = marksheet.pass_fail
            marks = marksheet.mark_line_ids
            values = []
            for record in marks:
                vals = {
                    'subject': record.subject,
                    'mark': record.mark,
                    'pass_mark': record.pass_mark,
                    'pass_fail': record.pass_fail,
                }
                values.append(vals)
            data = {
                'form': self.read()[0],
                'mark': values,
                'result': result
            }
            return self.env.ref('college.action_report_student_marksheet'
                                ).report_action(self, data=data)
        elif self.marklist == 'class':
            paper = self.semester_id.syllabus_line_ids
            marksheet = self.env['college.marksheet'].search([
                ('classes', '=', self.class_id.name),
                ('semester', '=', self.semester_id.name),
                ('exam', '=', self.exam_id.name)
            ])
            marks = marksheet.mark_line_ids

            line = []
            papers = []
            for name in marksheet:
                vals = {
                    'id': name.id,
                    'name': name.name,
                    'total_mark': name.total_mark,
                }
                line.append(vals)
                for i in marks:
                    # search_id = self.search([('id', '=', vals.get('id'))])
                    # print(search_id)
                    vals = {
                        'subject': i.subject,
                        'mark': i.mark
                    }
                    papers.append(vals)
                    print(i.mark)
            #     rank = {}
            #     for values in line:
            #         values.update({'mark': rec.mark})
            #         # search_id = self.search([('id', '=', values.get('id'))])
            #         # search_id.mark = values.mark
            #     # line.append(vals)
            #     print("Paper",
            #           rank['mark'])
            values = []
            for record in paper:
                vals = {
                    'subject': record.subject,
                }
                values.append(vals)
            data = {
                'form': self.read()[0],
                'mark': values,
                'paper': papers,
                'lines': line
            }
            print(data)
            return self.env.ref('college.action_report_class_marksheet'
                                ).report_action(self, data=data)
