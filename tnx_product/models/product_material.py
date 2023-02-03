# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductMaterial(models.Model):
    _name = 'product.material'
    _description = 'Product.material'
    name = fields.Char(
        string='Name',
        required=True)

    product_type = fields.Selection(
        [
            ("button", "Bouton"),
            ("label", "Etiquette"),
            ("sticker", "Autocollant"),
            ("other", "Autres"),
        ],
        string="Type du produit",
        default='other',
        required=True
    )


