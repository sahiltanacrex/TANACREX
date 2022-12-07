# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductMaterial(models.Model):
    _name = 'product.material'
    _description = 'Product.material'

    product_type = fields.Selection(
        [
            ("button", "Bouton"),
            ("label", "Etiquette"),
            ("sticker", "Autocollant"),
            ("other", "Autres"),
        ],
        string="Type du produit",
        default='other'
    )

    material = fields.Char()

