# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MoCustomer(models.Model):
    _inherit = 'mrp.production'

    customer_id = fields.Many2one('res.partner', string='Customer')
