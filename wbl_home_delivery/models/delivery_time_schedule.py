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

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _name = 'delivery.time.schedule'
    _description = "Delivery Time Schedule"

    delivery_carrier_id = fields.Many2one(
        'delivery.person',
        string="Delivery Carrier",
        ondelete='cascade',
        required=True,
        index=True
    )

    @staticmethod
    def _get_delivery_week_days():
        return [
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ]

    @staticmethod
    def _get_delivery_time_hours():
        return [
            ('00', '00'),
            ('01', '01'),
            ('02', '02'),
            ('03', '03'),
            ('04', '04'),
            ('05', '05'),
            ('07', '07'),
            ('08', '08'),
            ('09', '09'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
            ('14', '14'),
            ('15', '15'),
            ('16', '16'),
            ('17', '17'),
            ('18', '18'),
            ('19', '19'),
            ('20', '20'),
            ('21', '21'),
            ('22', '22'),
            ('23', '23'),
            ('24', '24'),
        ]

    @staticmethod
    def _get_delivery_time_minutes():
        return [
            ('00', '00'),
            ('01', '01'),
            ('02', '02'),
            ('03', '03'),
            ('04', '04'),
            ('05', '05'),
            ('06', '06'),
            ('07', '07'),
            ('08', '08'),
            ('09', '09'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
            ('14', '14'),
            ('15', '15'),
            ('16', '16'),
            ('17', '17'),
            ('18', '18'),
            ('19', '19'),
            ('20', '20'),
            ('21', '21'),
            ('22', '22'),
            ('23', '23'),
            ('24', '24'),
            ('25', '25'),
            ('26', '26'),
            ('27', '27'),
            ('28', '28'),
            ('29', '29'),
            ('30', '30'),
            ('31', '31'),
            ('32', '32'),
            ('33', '33'),
            ('34', '34'),
            ('35', '35'),
            ('36', '36'),
            ('37', '37'),
            ('38', '38'),
            ('39', '39'),
            ('40', '40'),
            ('41', '41'),
            ('42', '42'),
            ('43', '43'),
            ('44', '44'),
            ('45', '45'),
            ('46', '46'),
            ('47', '47'),
            ('48', '48'),
            ('49', '49'),
            ('50', '50'),
            ('51', '51'),
            ('52', '52'),
            ('53', '53'),
            ('54', '54'),
            ('55', '55'),
            ('56', '56'),
            ('57', '57'),
            ('58', '58'),
            ('59', '59'),
            ('60', '60'),
        ]

    week_days = fields.Selection(
        selection='_get_delivery_week_days',
        string='Days',
        default='Monday'
    )
    open_time_hours = fields.Selection(
        selection='_get_delivery_time_hours',
        string='Open Time (Hour)',
        default='00'
    )
    open_time_minutes = fields.Selection(
        selection='_get_delivery_time_minutes',
        string='Open Time (Minute)',
        default='00'
    )
    close_time_hours = fields.Selection(
        selection='_get_delivery_time_hours',
        string='Close Time (Hour)',
        default='00'
    )
    close_time_minutes = fields.Selection(
        selection='_get_delivery_time_minutes',
        string='Close Time (Minute)',
        default='00'
    )

    @api.constrains('open_time_hours', 'close_time_hours')
    def _check_open_close_time(self):
        for record in self:
            if record.open_time_hours > record.close_time_hours:
                raise ValidationError(
                    "Open time hours must be less than close time hours!"
                )
