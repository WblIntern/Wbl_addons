/** @odoo-module **/

import { Component } from '@odoo/owl';
import publicWidget from '@web/legacy/js/public/public_widget';
import { browser } from '@web/core/browser/browser';
import { _t } from '@web/core/l10n/translation';
import { rpc } from "@web/core/network/rpc";

export const websiteCashOnDelivery = publicWidget.Widget.extend({
    selector: '#o_payment_form',
    events: Object.assign({}, publicWidget.Widget.prototype.events, {
        'click [name="o_payment_radio"]': '_selectPaymentOption',
        'click [name="o_payment_submit_button"]': '_submitForm',
    }),

    /**
     * @override
     */
    init() {
        this._super(...arguments);
    },
    _selectPaymentOption: async function (ev) {
        const checkedRadio = ev.target;
        var providerId = Number(checkedRadio.dataset['providerId']);
        var providerCode = checkedRadio.dataset['providerCode'];
        const result = await rpc('/shop/cash_payment', {
            'provider_id': providerId,
        });
        this.result = result;
        var amountTax = document.querySelector('#order_total_taxes .monetary_field');
        var amountTotal = document.querySelectorAll('#order_total .monetary_field, #amount_total_summary.monetary_field');
        if (result.is_cod_fee) {
            amountTax.innerHTML = result.new_amount_tax;
            amountTotal.forEach(total => total.innerHTML = result.new_amount_total);
            $("#cod_payment_fee").show();
        } else {
            amountTax.innerHTML = result.new_amount_tax;
            amountTotal.forEach(total => total.innerHTML = result.new_amount_total);
            $("#cod_payment_fee").hide();
        }
    }
});
publicWidget.registry.websiteCashOnDelivery =  websiteCashOnDelivery;
