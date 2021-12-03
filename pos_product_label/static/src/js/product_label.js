odoo.define('pos_product_label.product_label', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;
    models.load_fields('product.product','product_label');
    models.Orderline = models.Orderline.extend({
        initialize:function(attr,options){
            var line = _super_orderline.initialize.apply(this,arguments);
            this.product_label = this.product.product_label;
        }
    });
});