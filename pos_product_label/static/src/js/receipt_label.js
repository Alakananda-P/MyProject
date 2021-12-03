odoo.define('pos_product_label.receipt_label', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;
    models.load_fields('product.product','product_label');
    models.Orderline = models.Orderline.extend({
        export_for_printing: function() {
            var line = _super_orderline.export_for_printing.apply(this, arguments);
            line.product_label = this.get_product().product_label;
            return line;
        }
    });
});