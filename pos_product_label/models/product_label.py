# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductLabel(models.Model):
    _inherit = 'product.template'

    product_label = fields.Char(string='Product Label')
