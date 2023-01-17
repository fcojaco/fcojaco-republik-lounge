odoo.define("sh_pos_secondary.screens", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    var DB = require("point_of_sale.DB");
    var utils = require("web.utils");
    var field_utils = require("web.field_utils");
    var round_di = utils.round_decimals;
    const PaymentScreenStatus = require("point_of_sale.PaymentScreenStatus")
    const Registries = require("point_of_sale.Registries");

    models.load_models({
        model: "res.currency",
        fields: ["name", "symbol", "position", "rounding", "rate"],
        loaded: function (self, currencies) {
            self.currency = currencies[0];
            if (self.currency.rounding > 0 && self.currency.rounding < 1) {
                self.currency.decimals = Math.ceil(Math.log(1.0 / self.currency.rounding) / Math.log(10));
            } else {
                self.currency.decimals = 0;
            }

            self.company_currency = currencies[1];
            self.db.add_currencies(currencies);
        },
    });
    models.load_fields("product.pricelist", ["currency_id"]);

    DB.include({
        init: function (options) {
            this._super(options);
            this.currencies = [];
            this.currency_by_id = {};
        },

        add_currencies: function (currencies) {
            if (!currencies instanceof Array) {
                currencies = [currencies];
            }
            for (var i = 0, len = currencies.length; i < len; i++) {
                var currency = currencies[i];
                this.currencies.push(currency);
                this.currency_by_id[currency.id] = currency;
            }
        },
    });

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        convert_currency: function (from_currency, currency, amount) {
            if (parseFloat(currency.rate) > 0.0 && parseFloat(from_currency.rate) > 0.0) {
                amount = parseFloat(amount) * (parseFloat(currency.rate) / parseFloat(from_currency.rate));
                return amount;
            } else {
                return amount;
            }
        },

        format_currency: function (amount, precision) {
            var currency_id = this.env.pos.get_order().pricelist.currency_id[0];
            var currency = this.env.pos.db.currency_by_id[currency_id];
            var from_currency_id = this.env.pos.config.currency_id[0];
            var from_currency = this.env.pos.db.currency_by_id[from_currency_id];

            amount = this.convert_currency(from_currency, currency, amount);
            amount = this.format_currency_no_symbol(amount, precision);

            if (currency.position === "after") {
                return amount + " " + (currency.symbol || "");
            } else {
                return (currency.symbol || "") + " " + amount;
            }
        },
        format_currency_no_symbol: function (amount, precision) {
            var currency_id = this.env.pos.get_order().pricelist.currency_id[0];
            var currency = this.env.pos.db.currency_by_id[currency_id];
            var decimals = currency.decimals || 2;
            
            if (precision && this.env.pos.dp[precision] !== undefined) {
                decimals = this.env.pos.dp[precision];
            }
            
            if (typeof amount === "number") {
                amount = round_di(amount, decimals).toFixed(decimals);
                amount = field_utils.format.float(round_di(amount, decimals), { digits: [69, decimals] });
            }

            return amount;
        },
    });
    
    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function () {
            var self = this;
            var lines = _super_orderline.export_for_printing.call(this);

            var currency_id = this.pos.get_order().pricelist.currency_id[0];
            var currency = this.pos.db.currency_by_id[currency_id];
            var from_currency_id = this.pos.config.currency_id[0];
            var from_currency = this.pos.db.currency_by_id[from_currency_id];
            var amount = self.pos.convert_currency(from_currency, currency, self.get_unit_price())
            lines['price_display_one'] = amount
            lines['price_display'] = this.get_quantity() * amount;
            return lines;
        },
    });

    var _super_paymentline = models.Paymentline.prototype;
    models.Paymentline = models.Paymentline.extend({
        export_for_printing: function(){
            var payment_detail = _super_paymentline.export_for_printing.call(this);
            var currency_id = this.pos.get_order().pricelist.currency_id[0];
            var currency = this.pos.db.currency_by_id[currency_id];
            var from_currency_id = this.pos.config.currency_id[0];
            var from_currency = this.pos.db.currency_by_id[from_currency_id];
            payment_detail['amount'] = this.pos.convert_currency(from_currency, currency, payment_detail['amount'])
            return payment_detail
        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function(){
            var receipt = _super_order.export_for_printing.call(this);
            var self = this;
            var currency_id = this.pricelist.currency_id[0];
            var currency = this.pos.db.currency_by_id[currency_id];
            var from_currency_id = this.pos.config.currency_id[0];
            var from_currency = this.pos.db.currency_by_id[from_currency_id];

            if(receipt.change){

                var total = receipt.total_with_tax
                total = this.pos.convert_currency(from_currency, currency, total).toFixed(2)

                var total_paid = receipt.total_paid

                var change = total_paid - total

                if (currency.position === "after") {
                    change = change.toFixed(2) + " " + (currency.symbol || "");
                } else {
                    change = (currency.symbol || "") + " " + change.toFixed(2);
                }
                receipt['change'] = change
            }else{
                if (currency.position === "after") {
                    receipt['change'] = receipt['change'].toFixed(2) + " " + (currency.symbol || "");
                } else {
                    receipt['change'] = (currency.symbol || "") + " " + receipt['change'].toFixed(2);
                }
            }
            if(currency_id != from_currency_id && receipt.tax_details && receipt.tax_details.length > 0){
                _.each(receipt.tax_details, function(each_tax){
                    each_tax['amount'] = (self.pos.convert_currency(from_currency,currency,each_tax['amount'])).toFixed(2)
                });
            }
            return receipt
        },
    });

    const PosPaymentScreenStatus = (PaymentScreenStatus) =>
    class extends PaymentScreenStatus {
        get totalDueText() {
            if(this.env.pos.get_order() && this.env.pos.get_order().paymentlines && this.env.pos.get_order().paymentlines.length > 0){

                var order_currency_id = this.env.pos.get_order().pricelist.currency_id[0];
                var config_currency_id = this.env.pos.config.currency_id[0];
                
                if(order_currency_id == config_currency_id){
                    return super.totalDueText
                }else{
                    var currency = this.env.pos.db.currency_by_id[config_currency_id];
                    var amount = this.currentOrder.get_total_with_tax() + this.currentOrder.get_rounding_applied()
                    amount = amount.toFixed(2)
                    if (currency.position === "after") {

                        return amount + " " + (currency.symbol || "");
                    } else {
                        return (currency.symbol || "") + " " + amount;
                    }
                }
            }else{
                return super.totalDueText
            }
        }
        get changeText() {
            if(this.env.pos.get_order() && this.env.pos.get_order().paymentlines && this.env.pos.get_order().paymentlines.length > 0){

                var order_currency_id = this.env.pos.get_order().pricelist.currency_id[0];
                var config_currency_id = this.env.pos.config.currency_id[0];
                
                if(order_currency_id == config_currency_id){
                    return super.changeText
                }else{
                    var currency = this.env.pos.db.currency_by_id[config_currency_id];
                    var amount = this.currentOrder.get_change()
                    amount = amount.toFixed(2)
                    if (currency.position === "after") {

                        return amount + " " + (currency.symbol || "");
                    } else {
                        return (currency.symbol || "") + " " + amount;
                    }
                }
            }else{
                return super.changeText
            }
        }
    };
    Registries.Component.extend(PaymentScreenStatus, PosPaymentScreenStatus);

});
