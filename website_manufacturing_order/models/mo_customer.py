# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.addons.portal.models.portal_mixin import PortalMixin


class MoCustomer(models.Model):
    _inherit = 'mrp.production'
    # _inherit = ['mrp.production', 'portal.mixin']

    partner_id = fields.Many2one('res.partner', string='Customer')

    def _compute_access_url(self):
        super(MoCustomer, self)._compute_access_url()
        for order in self:
            order.access_url = '/my/manufacture/%s' % (order.id)
