from collections import OrderedDict

from odoo import http
from odoo.http import request, Response
from odoo.tools.translate import _
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        print(counters)
        # user = request.env.user.partner_id.id
        values = super()._prepare_home_portal_values(counters)
        if 'manufacture_count' in counters:
            values['manufacture_count'] = request.env['mrp.production'].search_count([
                ('state', 'in', ['confirmed', 'done', 'cancel']),
                # ('customer_id', '=', user)
            ]) if request.env['mrp.production'].check_access_rights('read', raise_exception=False) else 0
        print(values)
        return values

    def _manufacturing_order_get_page_view_values(self, order, access_token, **kwargs):
        #
        def resize_to_48(b64source):
            if not b64source:
                b64source = base64.b64encode(Binary.placeholder())
            return image_process(b64source, size=(48, 48))

        values = {
            'order': order,
            'resize_to_48': resize_to_48,
        }
        return self._get_page_view_values(order, access_token, values, 'my_manufacture_history', False, **kwargs)

    @http.route(['/my/manufacture', '/my/manufacture/page/<int:page>'], type='http',
                auth="user", website=True)
    def portal_my_manufacturing_orders(self, page=1, date_begin=None, date_end=None,
                                  sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        ManufacturingOrder = request.env['mrp.production']

        domain = []

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        searchbar_sortings = {
            'date': {'label': _('Newest'),
                     'order': 'create_date desc, id desc'},
            'name': {'label': _('Name'), 'order': 'name asc, id asc'},
            # 'amount_total': {'label': _('Total'),
            #                  'order': 'amount_total desc, id desc'},
        }
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'),
                    'domain': [('state', 'in', ['confirmed', 'done', 'cancel'])]},
            'confirmed': {'label': _('Confirmed'),
                         'domain': [('state', '=', 'confirmed')]},
            'cancel': {'label': _('Cancelled'),
                       'domain': [('state', '=', 'cancel')]},
            'done': {'label': _('Done'), 'domain': [('state', '=', 'done')]},
        }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # count for pager
        manufacture_count = ManufacturingOrder.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/manufacture",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby, 'filterby': filterby},
            total=manufacture_count,
            page=page,
            step=self._items_per_page
        )
        # search the purchase orders to display, according to the pager data
        orders = ManufacturingOrder.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_manufacture_history'] = orders.ids[:100]
        print(orders)

        values.update({
            'date': date_begin,
            'orders': orders,
            'page_name': 'manufacture',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'default_url': '/my/manufacture',
        })
        return request.render("website_manufacturing_order.portal_my_manufacturing_orders", values)

    @http.route(['/my/manufacture/<int:order_id>'], type='http', auth="public",
                website=True)
    def portal_my_manufacturing_order(self, order_id=None, access_token=None, **kw):
        try:
            order_sudo = self._document_check_access('mrp.production', order_id,
                                                     access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        report_type = kw.get('report_type')
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type,
                                     report_ref='mrp.action_report_production_order',
                                     download=kw.get('download'))

        confirm_type = kw.get('confirm')
        if confirm_type == 'reminder':
            order_sudo.confirm_reminder_mail(kw.get('confirmed_date'))
        if confirm_type == 'reception':
            order_sudo._confirm_reception_mail()

        values = self._manufacturing_order_get_page_view_values(order_sudo,
                                                           access_token, **kw)
        update_date = kw.get('update')
        if order_sudo.company_id:
            values['res_company'] = order_sudo.company_id
        if update_date == 'True':
            return request.render(
                "website_manufacturing_order.portal_my_manufacturing_order_update_date", values)
        return request.render("website_manufacturing_order.portal_my_manufacturing_order", values)
