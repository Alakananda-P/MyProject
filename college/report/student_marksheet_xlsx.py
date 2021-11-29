# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentMarksheetXlsx(models.AbstractModel):
    _name = "report.college.report_student_marksheet_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, students):
        sheet = workbook.add_workbook('Student MarkSheet')
        bold = workbook.add_format({'bold': True})

