/** @odoo-module */
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { OrderlineCustomerNoteButton } from "@point_of_sale/app/screens/product_screen/control_buttons/customer_note_button/customer_note_button";
import { HomeDeliveryButtonPopup } from "@wbl_home_delivery/js/home_delivery_button_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(OrderlineCustomerNoteButton.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
    async onClickHomeDeliveryButton() {
          if(!this.pos.selectedOrder.partner){
               this.popup.add(ErrorPopup, {
                    title: _t("Customer Not Selected"),
                    body: _t("Please select a customer first"),
               });
          }
          else {
             try {
               const { confirmed } = await this.popup.add(HomeDeliveryButtonPopup, {
               title: _t("Home Delivery Details"),
            });
            } catch (error) {
               console.error("Error showing popup:", error);
            }

          }
    },
});

