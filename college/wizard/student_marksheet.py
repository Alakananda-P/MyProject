# -*- coding: utf-8 -*-
from odoo import api, fields, models
import math
from itertools import groupby


class StudentMarksheetWizard(models.TransientModel):
    _name = "student.marksheet.wizard"
    _description = "Student Marksheet Wizard"

    marklist = fields.Selection([
        ('student', 'Student'), ('class', 'Class')], 'MarkList')
    student_id = fields.Many2one('college.student', string='Student')
    class_id = fields.Many2one('college.student.class', string='Class')
    semester_id = fields.Many2one('college.semester', string='Semester')
    exam_id = fields.Many2one('college.exam', string='Exam')
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
        subject_mark = []
        result = []
        if self.marklist == 'student':
            args = {
                'student_id': self.student_id.name,
                'semester_id': self.semester_id.name,
                'exam_id': self.exam_id.name
            }
            self.env.cr.execute("""SELECT cm.name as student,
                                    cm.pass_fail as pass_fail,
                                    cm.course as course,
                                    m.subject as subject,
                                    m.mark as mark,
                                    m.pass_mark as passmark,
                                    m.pass_fail as subject_pass_fail
                                FROM college_marksheet cm
                                LEFT OUTER JOIN marksheet_marks_lines m ON(
                                    cm.id = m.mark_id)
                                WHERE (cm.name = %(student_id)s 
                                AND cm.semester = %(semester_id)s 
                                AND cm.exam = %(exam_id)s )""", args)

        elif self.marklist == 'class':
            args = {
                'class_id': self.class_id.name,
                'semester_id': self.semester_id.name,
                'exam_id': self.exam_id.name
            }
            self.env.cr.execute("""SELECT 
                                    cm.name as student,
                                    m.subject as subject,
                                    m.mark as mark,                                 
                                    cm.total_mark as obtained_mark,
                                    cm.total_max_mark as total_mark,
                                    cm.pass_fail as pass_fail
                                FROM college_marksheet cm
                                LEFT OUTER JOIN marksheet_marks_lines m 
                                ON(cm.id = m.mark_id) 
                                WHERE (cm.classes = %(class_id)s 
                                AND cm.semester = %(semester_id)s 
                                AND cm.exam = %(exam_id)s )""", args)

        student = self.env.cr.dictfetchall()
        print(student)

        # self.env.cr.execute("""SELECT
        #                                 COUNT(ma.id) as total
        #                                 FROM college_marksheet ma
        #                                 WHERE (ma.classes = %(class_id)s
        #                                 AND ma.semester = %(semester_id)s
        #                                 AND ma.exam = %(exam_id)s )""", args)
        # count = self.env.cr.dictfetchall()

        def key_func(k):
            return k['student']
        info = sorted(student, key=key_func)
        for key, value in groupby(info, key_func):
            result.append(key)
            subject_mark.append(list(value))

        data = {
            'form': self.read()[0],
            'student': student,
            'result': result,
            'subject_mark': subject_mark
        }
        print(data)
        return self.env.ref('college.action_report_student_marksheet_pdf'
                            ).report_action(self, data=data)

        # student_pass_fail = []
        # count_detail = []
        # student_detail = []
        # class_detail = []
        # subject = []
        # if self.marklist == 'student':
        #     marksheet = self.env['college.marksheet'].search([
        #         ('name', '=', self.student_id.name),
        #         ('semester', '=', self.semester_id.name),
        #         ('exam', '=', self.exam_id.name)
        #     ])
        #     pass_fail = marksheet.pass_fail
        #     marks = marksheet.mark_line_ids
        #     for record in marks:
        #         vals = {
        #             'subject': record.subject,
        #             'mark': record.mark,
        #             'pass_mark': record.pass_mark,
        #             'pass_fail': record.pass_fail
        #         }
        #         student_detail.append(vals)
        #     student_pass_fail.append({'student_pass_fail': pass_fail})
        #
        # elif self.marklist == 'class':
        #     marksheet = self.env['college.marksheet'].search([
        #         ('classes', '=', self.class_id.name),
        #         ('semester', '=', self.semester_id.name),
        #         ('exam', '=', self.exam_id.name)
        #     ])
        #     line_detail = []
        #     for record in marksheet:
        #         vals = {
        #             'name': record.name,
        #             'obtained_mark': record.total_mark,
        #             'total_mark': record.total_max_mark,
        #             'pass_fail': record.pass_fail
        #         }
        #         line_detail.append(vals)
        #
        #     subject_marks = []
        #     marks = marksheet.mark_line_ids
        #     for record in marks:
        #         vals = {
        #             record.subject: record.mark
        #         }
        #         subject_marks.append(vals)
        #
        #     subject_len = len(self.semester_id.syllabus_line_ids)
        #     res = tuple(subject_marks[n:n+int(subject_len)] for n, i in
        #                 enumerate(subject_marks) if n % int(subject_len) == 0)
        #     output = list(zip(line_detail, res))
        #     class_detail.append(output)
        #
        #     pass_count = 0
        #     fail_count = 0
        #     for line in output:
        #         if line[0]['pass_fail'] == True:
        #             pass_count += 1
        #         else:
        #             fail_count += 1
        #     div = math.gcd(pass_count, fail_count)
        #     ratio = str(int(pass_count / div)) + ':' + str(int(
        #         fail_count / div))
        #     count = {
        #         'total_student': len(marksheet),
        #         'total_pass': pass_count,
        #         'total_failed': fail_count,
        #         'ratio': ratio
        #     }
        #     count_detail.append(count)
        #     paper = self.semester_id.syllabus_line_ids
        #     for record in paper:
        #         vals = {
        #             'subject': record.subject,
        #         }
        #         subject.append(vals)
        #
        # data = {
        #     'form': self.read()[0],
        #     'subject': subject,
        #     'class_detail': class_detail,
        #     'count': count_detail,
        #     'student_detail': student_detail,
        #     'student_pass_fail': student_pass_fail
        # }
        # return self.env.ref('college.action_report_student_marksheet'
        #                     ).report_action(self, data=data)

    def action_print_excel(self):
        print("Hello Excel")
