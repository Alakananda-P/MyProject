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
            # domain = []
            # domain_mark = []
            # marksheets_name = []
            # domain_names = []
            # marksheets_id = []
            # mark_id = []
            # mark_name = []
            # marksheet = self.env['college.marksheet'].search([
            #     ('classes', '=', self.class_id.name),
            #     ('semester', '=', self.semester_id.name),
            #     ('exam', '=', self.exam_id.name)
            # ])
            # marks = marksheet.mark_line_ids
            #
            # for name in marksheet:
            #     marksheets_id.append(name)
            #     marksheets_name.append(name.name)
            # print(marksheets_name)
            # for name in marksheets_id:
            #     domain_names += [
            #         ('name', '=', name.name),
            #         ('total_mark', '=', name.total_mark)
            #     ]
            #
            # for mark in marks:
            #     mark_id.append(mark)
            #     mark_name.append(mark.mark)
            # for mark in mark_id:
            #     domain_mark += [('mark', '=', mark.mark)]
            #
            # if domain_names:
            #     domain += (domain_names)
            # if domain_mark:
            #     domain += (domain_mark)
            #
            # subject_len = len(domain_mark)/len(marksheets_name)
            #
            # res = tuple(domain_mark[n:n+int(subject_len)] for n, i in enumerate(
            #     domain_mark) if n % int(subject_len) == 0)
            #
            #
            # result = tuple(
            #     domain_names[n:n + 2] for n, i in enumerate(
            #         domain_names) if n % 2 == 0)
            #
            # output = list(zip(result, res))
            #
            # for i in output:
            #     print(i)
            # # sub_len = 0
            # j = 1
            # for i in domain_mark:
            #     print("I",i)
            #     if j <= subject_len:
            #         names.append(i)
            #         j = j+1
            #         print("J",j)
            #     # if j <= sub_len
            #     sub_len += subject_len
            #     print(sub_len)
            #     if j <= sub_len:
            #         j = j + 1
            #         print(j)
            result = []
            marksheet = self.env['college.marksheet'].search([
                ('classes', '=', self.class_id.name),
                ('semester', '=', self.semester_id.name),
                ('exam', '=', self.exam_id.name)
            ])
            marks = marksheet.mark_line_ids
            for record in marksheet:
                vals = {
                    'name': record.name,
                    'obtained_mark': record.total_mark
                }
                result.append(vals)
            print("Result", result)
            subject_len = len(self.semester_id.syllabus_line_ids)
            mark = []
            for record in marks:
                vals = {
                    record.subject: record.mark
                }
                mark.append(vals)
            print("Mark",mark)

            res = tuple(mark[n:n+int(subject_len)] for n, i in enumerate(
                mark) if n % int(subject_len) == 0)

            output = list(zip(result, res))
            print(output)
            # for line in output:
                # print(line[0]['total_mark'])
                # for i in line[1]:
                #     print(list(i.values())[0])







            # print(domain_names[2])

            paper = self.semester_id.syllabus_line_ids
            # marksheet = self.env['college.marksheet'].search([
            #     ('classes', '=', self.class_id.name),
            #     ('semester', '=', self.semester_id.name),
            #     ('exam', '=', self.exam_id.name)
            # ])
            # marks = marksheet.mark_line_ids
            # print(marksheet)
            # line = []
            # papers = []
            # for name in marksheet:
            #     vals = {
            #         'id': name.id,
            #         'name': name.name,
            #         'total_mark': name.total_mark,
            #
            #     }
            #     line.append(vals)
            #
            # for i in marks:
            #     vals = {
            #         'subject': i.subject,
            #         'mark': i.mark
            #     }
            #     papers.append(vals)
            # print(papers)
            # print(line)
            values = []
            for record in paper:
                vals = {
                    'subject': record.subject,
                }
                values.append(vals)
            data = {
                'form': self.read()[0],
                'mark': values,
                # 'paper': papers,
                # 'lines': line
                'output': output
            }
            print(data)
            return self.env.ref('college.action_report_class_marksheet'
                                ).report_action(self, data=data)
