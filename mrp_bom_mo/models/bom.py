# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MoCustomer(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        super(MoCustomer, self).button_mark_done()
