odoo.define('pos_purchase_limit.purchase_limit', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    models.load_fields('res.partner','purchase_limit');
    var PosComponent = require('point_of_sale.PosComponent');
    var ActionpadWidget = require('point_of_sale.ActionpadWidget');
    var Registries = require('point_of_sale.Registries');
    var core = require('web.core');
    var _t = core._t;
    const { useListener } = require('web.custom_hooks');
    const { Gui } = require('point_of_sale.Gui');

    const PurchaseLimit = (ActionpadWidget) =>
        class extends ActionpadWidget {
            constructor() {
                super(...arguments);
                useListener('click-pay', this.onClick);
            }
            async onClick() {
                var self = this;
                var client = self.env.pos.get_client();
                var order = self.env.pos.get_order();
                var order_subtotal = order.get_subtotal();
                if (!client){
                    Gui.showPopup('ErrorPopup', {
                        'title': _t('Select a Customer'),
                        'body': _t('If no customer is selected, Please select a customer'),
                    });
                }
                if (client){
                    if(order_subtotal > client.purchase_limit){
                        Gui.showPopup('ErrorPopup', {
                            'title': _t('Exceeds Purchase Limit'),
                            'body': _t(' Purchase Limit Amount is ' + client.purchase_limit),
                        });
                    }
                }
            }
        }
    Registries.Component.extend(ActionpadWidget, PurchaseLimit);
    return PurchaseLimit
});
