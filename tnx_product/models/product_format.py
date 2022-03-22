from odoo import models, fields, api
class Product_format(models.Model):
    _name='product.format'
    name = fields.Char(
        string='Name',
        required=False)