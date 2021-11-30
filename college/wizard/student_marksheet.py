# -*- coding: utf-8 -*-
from odoo import api, fields, models
# import math
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
        count_values = []
        if self.marklist == 'student' and self.semester_id and self.exam_id:
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
        elif self.marklist == 'student' and self.semester_id:
            args = {
                'student_id': self.student_id.name,
                'semester_id': self.semester_id.name
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
                                AND cm.semester = %(semester_id)s )""", args)
        elif self.marklist == 'student':
            args = {
                'student_id': self.student_id.name
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
                                WHERE (cm.name = %(student_id)s)""", args)

        elif self.marklist == 'class' and self.semester_id and self.exam_id:
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

            self.env.cr.execute("""SELECT
                                    COUNT(cm.id) as total_student,
                                    COUNT(CASE WHEN cm.pass_fail IS NULL or false THEN 1 END) as total_fail,
                                    COUNT(cm.pass_fail = true) as total_pass,
                                    ROUND((COUNT(NULLIF(cm.pass_fail,false))/COUNT(cm.id)::float)*100) as ratio
                                    FROM college_marksheet cm
                                    WHERE (cm.classes = %(class_id)s
                                    AND cm.semester = %(semester_id)s
                                    AND cm.exam = %(exam_id)s )""", args)
            count = self.env.cr.dictfetchall()
            count_values.append(count)

            def key_func(k):
                return k['student']
            info = sorted(student, key=key_func)
            for key, value in groupby(info, key_func):
                # result.append(key)
                subject_mark.append(list(value))

        elif self.marklist == 'class' and self.semester_id:
            args = {
                'class_id': self.class_id.name,
                'semester_id': self.semester_id.name
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
                                AND cm.semester = %(semester_id)s )""", args)

            student = self.env.cr.dictfetchall()

            self.env.cr.execute("""SELECT
                                    COUNT(cm.id) as total_student,
                                    COUNT(CASE WHEN cm.pass_fail IS NULL or false THEN 1 END) as total_fail,
                                    COUNT(cm.pass_fail = true) as total_pass,
                                    ROUND((COUNT(NULLIF(cm.pass_fail,false))/COUNT(cm.id)::float)*100) as ratio
                                    FROM college_marksheet cm
                                    WHERE (cm.classes = %(class_id)s
                                    AND cm.semester = %(semester_id)s)""", args)
            count = self.env.cr.dictfetchall()
            count_values.append(count)

            def key_func(k):
                return k['student']

            info = sorted(student, key=key_func)
            for key, value in groupby(info, key_func):
                # result.append(key)
                subject_mark.append(list(value))

        elif self.marklist == 'class':
            args = {
                'class_id': self.class_id.name
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
                                WHERE (cm.classes = %(class_id)s )""", args)

            student = self.env.cr.dictfetchall()

            self.env.cr.execute("""SELECT
                                    COUNT(cm.id) as total_student,
                                    COUNT(CASE WHEN cm.pass_fail IS NULL or false THEN 1 END) as total_fail,
                                    COUNT(cm.pass_fail = true) as total_pass,
                                    ROUND((COUNT(NULLIF(cm.pass_fail,false))/COUNT(cm.id)::float)*100) as ratio
                                    FROM college_marksheet cm
                                    WHERE (cm.classes = %(class_id)s)""", args)
            count = self.env.cr.dictfetchall()
            count_values.append(count)

            def key_func(k):
                return k['student']

            info = sorted(student, key=key_func)
            for key, value in groupby(info, key_func):
                # result.append(key)
                subject_mark.append(list(value))

        result = self.env.cr.dictfetchall()
        data = {
            'form': self.read()[0],
            'count': count_values,
            'subject_mark': subject_mark,
            'student': result,
        }
        return self.env.ref('college.action_report_student_marksheet_pdf'
                            ).report_action(self, data=data)

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
    def action_print_excel(self):
        if self.marklist == 'student' and self.semester_id and self.exam_id:
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
        elif self.marklist == 'student' and self.semester_id:
            args = {
                'student_id': self.student_id.name,
                'semester_id': self.semester_id.name
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
                                AND cm.semester = %(semester_id)s )""", args)
        elif self.marklist == 'student':
            args = {
                'student_id': self.student_id.name
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
                                WHERE (cm.name = %(student_id)s)""", args)

        student = self.env.cr.dictfetchall()
        data = {
            'form': self.read()[0],
            'student': student
        }
        return self.env.ref('college.action_report_student_marksheet_xlsx'
                            ).report_action(self, data=data)