# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentMarksheetXlsx(models.AbstractModel):
    _name = "report.college.report_student_marksheet_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, students):
        sheet = workbook.add_worksheet('Student MarkSheet')
        head = workbook.add_format({'bold': True,
                                    'align': 'center',
                                    'font_size': '14px'})
        sub_head = workbook.add_format({'align': 'center',
                                        'bold': True})
        bold = workbook.add_format({'bold': True})
        form_data = data['form']
        student = data['student']
        count = data['count']
        subject_mark = data['subject_mark']
        if form_data['marklist'] == 'student':
            sheet.set_column('A:A', 30)
            sheet.set_column('B:B', 12)
            sheet.set_column('C:C', 20)
            sheet.set_column('D:D', 18)
            student_marklist = form_data['student_id'][1] + ': ' + 'Mark List'
            sheet.merge_range('A1:D1', student_marklist, head)
            course_academic_year = form_data['student_course_id'
                                   ] + '-' + form_data['student_academic_year']
            sheet.merge_range('A2:D2', course_academic_year, sub_head)
            if form_data['exam_type_id']:
                exam = 'Exam' + ': ' + form_data['exam_type_id']
                sheet.merge_range('A3:C3', exam, bold)
            else:
                exam = 'Exam' + ': ' + ' '
                sheet.merge_range('A3:C3', exam, bold)
            if student[0]['pass_fail'] == True:
                result = 'Result' + ': ' + 'Pass'
                sheet.merge_range('A4:C4', result, bold)
            else:
                result = 'Result' + ': ' + 'Failed'
                sheet.merge_range('A4:C4', result, bold)
            row = 4
            col = 0
            sheet.write(row, col, 'Subject', bold)
            sheet.write(row, col+1, 'Mark', bold)
            sheet.write(row, col+2, 'Pass Mark', bold)
            sheet.write(row, col+3, 'Pass/Fail', bold)
            for line in student:
                row += 1
                sheet.write(row, col, line['subject'])
                sheet.write(row, col+1, line['mark'])
                sheet.write(row, col+2, line['passmark'])
                if line['subject_pass_fail'] == True:
                    sheet.write(row, col+3, 'Pass')
                else:
                    sheet.write(row, col+3, 'Fail')
        if form_data['marklist'] == 'class':
            sheet.set_column('A:A', 30)
            sheet.set_column('B:B', 20)
            sheet.set_column('C:C', 20)
            sheet.set_column('D:D', 20)
            sheet.set_column('E:E', 20)
            sheet.set_column('F:F', 20)
            sheet.set_column('G:G', 20)
            sheet.set_column('H:H', 15)
            sheet.set_column('I:I', 15)
            sheet.set_column('J:J', 18)
            student_marklist = form_data['class_id'][1] + ': ' + 'Mark List'
            sheet.merge_range('A1:J1', student_marklist, head)
            course_academic_year = form_data['class_course_id'][1] + '-' + form_data['class_academic_year']
            sheet.merge_range('A2:J2', course_academic_year, sub_head)
            if form_data['exam_type_id']:
                exam = 'Exam' + ': ' + form_data['exam_type_id']
                sheet.merge_range('A3:C3', exam, bold)
            else:
                exam = 'Exam' + ': ' + ' '
                sheet.merge_range('A3:C3', exam, bold)
            total_student = 'Total' + ': ' + str(count[0][0]['total_student'])
            sheet.merge_range('A4:C4', total_student, bold)
            total_pass = 'Pass' + ': ' + str(count[0][0]['total_pass'])
            sheet.merge_range('A5:C5', total_pass, bold)
            total_fail = 'Fail' + ': ' + str(count[0][0]['total_fail'])
            sheet.merge_range('A6:C6', total_fail, bold)
            total_ratio = 'Ratio' + ': ' + str(count[0][0]['ratio'])
            sheet.merge_range('A7:C7', total_ratio, bold)
            row = 7
            col = 0
            sheet.write(row, col, 'Student Name', bold)
            for subject in subject_mark[0]:
                col += 1
                sheet.write(row, col, subject['subject'], bold)
            sheet.write(row, col + 1, 'Obtained Mark', bold)
            sheet.write(row, col + 2, 'Total Mark', bold)
            sheet.write(row, col + 3, 'Pass/Failed', bold)
            for line in subject_mark:
                row += 1
                col = 0
                sheet.write(row, col, line[0]['student'])
                for mark in line:
                    col += 1
                    sheet.write(row, col, mark['mark'])
                sheet.write(row, col+1, line[0]['obtained_mark'])
                sheet.write(row, col+2, line[0]['total_mark'])
                if line[0]['pass_fail'] == True:
                    sheet.write(row, col+3, 'Pass')
                else:
                    sheet.write(row, col+3, 'Fail')
