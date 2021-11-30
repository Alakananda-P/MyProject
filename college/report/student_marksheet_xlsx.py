# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentMarksheetXlsx(models.AbstractModel):
    _name = "report.college.report_student_marksheet_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, students):
        sheet = workbook.add_worksheet('Student MarkSheet')
        head = workbook.add_format({'bold': True, 'align': 'center', 'font_size': '14px'})
        sub_head = workbook.add_format({'align': 'center', 'bold': True})
        bold = workbook.add_format({'bold': True})
        form_data = data['form']
        student = data['student']
        # if form_data
        sheet.set_column('A:A', 30)
        sheet.set_column('B:B', 12)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 18)
        student_marklist = form_data['student_id'][1] + ': ' + 'Mark List'
        sheet.merge_range('A1:D1', student_marklist, head)
        course_academic_year = form_data['student_course_id'] + '-' + form_data['student_academic_year']
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
            result = 'Exam' + ': ' + 'Failed'
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
