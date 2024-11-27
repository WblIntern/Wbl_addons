# -*- coding: utf-8 -*-
#
#################################################################################
# Author      : Weblytic Labs Pvt. Ltd. (<https://store.weblyticlabs.com/>)
# Copyright(c): 2023-Present Weblytic Labs Pvt. Ltd.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
##################################################################################

from collections import Counter
from datetime import datetime, timedelta
from odoo import http
from odoo.http import request


class DeliveryTimeSchedule(http.Controller):

    @http.route('/slot_check', type='json', auth='public', website=True)
    def schedule_delivery(self, **post):
        current_home_delivery_date = post.get('home_delivery_date'),
        current_home_delivery_time = post.get('home_delivery_time'),
        current_home_delivery_person_id = post['home_delivery_person_id'],
        current_home_delivery_person_id = str(current_home_delivery_person_id[0])
        current_time = post['current_time'],
        order_preparing_time = post.get('order_preparing_time')

        delivery_person = request.env['delivery.person'].sudo().search([('id', '=', current_home_delivery_person_id)])
        all_slot = post.get('available_slots', []),
        pos_order = request.env['pos.order'].sudo().search(
            [('home_delivery_person_id', '=', current_home_delivery_person_id),
             ('home_delivery_date', '=', current_home_delivery_date)])
        available_all_alot = []

        for slot in all_slot:
            for time in slot:
                available_all_alot.append(time)
        formatted_available_all_slot = [self.format_time(slot) for slot in available_all_alot]
        filtered_slot = []
        today_date = datetime.today().strftime('%Y/%m/%d')
        order_preparing_time = int(order_preparing_time)
        coming_current_time = datetime.strptime(current_time[0], "%I:%M %p")
        new_time = coming_current_time + timedelta(minutes=order_preparing_time)
        current_time_with_preparing_time = new_time.strftime("%I:%M %p")
        if today_date == current_home_delivery_date[0]:
            current_time_obj = datetime.strptime(current_time_with_preparing_time, '%I:%M %p')
            updated_slot = [
                slot for slot in formatted_available_all_slot
                if datetime.strptime(slot.split('-')[0], '%I:%M %p') > current_time_obj
            ]
            formatted_available_all_slot = updated_slot

        for slots in formatted_available_all_slot:
            for order in pos_order:
                if order.home_delivery_time == slots:
                    filtered_slot.append(slots)

        slot_counts = Counter(filtered_slot)

        unique_slots = [slot for slot, count in slot_counts.items() if count < delivery_person.max_order_in_single_slot]

        for slot in formatted_available_all_slot:
            if slot not in filtered_slot:
                unique_slots.append(slot)

        sorted_slots = sorted(unique_slots, key=lambda x: datetime.strptime(x.split('-')[0], "%I:%M %p"))

        if delivery_person.max_order_in_single_slot >= 1:
            values = {
                "available_slots": sorted_slots
            }
        else:
            values = {
                "available_slots": formatted_available_all_slot
            }

        return values

    def format_time(self, interval):
        start_hour, end_hour = interval.split('-')
        start_time = datetime.strptime(f'{start_hour}:00', '%H:%M')
        end_time = datetime.strptime(f'{end_hour}:00', '%H:%M')

        return f'{start_time.strftime("%I:%M %p")}-{end_time.strftime("%I:%M %p")}'
