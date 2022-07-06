# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Sale_order(models.Model):
    _inherit = "sale.order"
    sale_order_partner = fields.Char("BC client")
    production_duration = fields.Char("Manufacturing time", required=True)
    delivery_time = fields.Char("Delivery time", required=True)
