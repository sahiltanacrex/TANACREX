# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sale_order(models.Model):
    _inherit="sale.order"
    sale_order_partner = fields.Char('BC client')
    production_duration = fields.Char('Durée de fabrication',required=True)
    delivery_time = fields.Char('Délais de livraison',required=True)

    