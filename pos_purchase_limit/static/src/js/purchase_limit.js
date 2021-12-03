odoo.define('pos_purchase_limit.purchase_limit', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var n = models.load_fields('res.partner','purchase_limit');
    var PosComponent = require('point_of_sale.PosComponent');
    var Registries = require('point_of_sale.Registries');
    var core = require('web.core');
    var _t = core._t;
    console.log("Models",models);
    console.log("N", n);
    console.log("Screens",PosComponent);

    var PurchaseLimit = PosComponent => class extends PosComponent {
        constructor(){
        super(this);
        }
        onClick(){
            console.log("Hello");
        }

    };
//    ActionpadWidget.template = 'ActionpadWidget';
    Registries.Component.extend(PosComponent, PurchaseLimit);
    return PurchaseLimit;
});

//odoo.define('point_of_sale.ActionpadWidget',function(require){'use strict';const PosComponent=require('point_of_sale.PosComponent');const Registries=require('point_of_sale.Registries');class ActionpadWidget extends PosComponent{get isLongName(){return this.client&&this.client.name.length>10;}
//get client(){return this.props.client;}}
//ActionpadWidget.template='ActionpadWidget';Registries.Component.add(ActionpadWidget);return ActionpadWidget;});;
