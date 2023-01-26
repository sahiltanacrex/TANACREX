# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class tnx_purchase(models.Model):
#     _name = 'tnx_purchase.tnx_purchase'
#     _description = 'tnx_purchase.tnx_purchase'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
