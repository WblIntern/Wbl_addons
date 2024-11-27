/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(PaymentScreen.prototype, {
     setup() {
        super.setup();
        this.pos = usePos();
     },
     addNewPaymentLine(paymentMethod) {
        var current_pos_order = this.pos.get_order();
        if(!paymentMethod.use_home_delivery && this.pos.is_home_delivery =="True"){
            this.popup.add(ErrorPopup, {
                title: _t("Wrong Payment Method"),
                body: _t("You can't use this payment method for home delivery"),
            });
            return;
        }
        super.addNewPaymentLine(...arguments);

     },
     async _finalizeValidation() {
        if(!this.pos.selectedOrder.partner && this.pos.is_home_delivery =="True"){
           this.popup.add(ErrorPopup, {
                title: _t("Customer not Selected"),
                body: _t("Please select the customer"),
           });
           return;
        }
       super._finalizeValidation();
     }

})

