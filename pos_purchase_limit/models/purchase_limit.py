# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseLimt(models.Model):
    _inherit = 'res.partner'

    activate_purchase_limit = fields.Boolean(string='Activate Purchase Limit')
    purchase_limit = fields.Monetary(string='Purchase Limit')
