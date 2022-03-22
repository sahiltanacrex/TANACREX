from odoo import models, fields, api
class Product_template(models.Model):
    _inherit='product.template'

    hs_code = fields.Char(
        string='HS CODE',
        required=False)
    product_format_id = fields.Many2one(
        comodel_name='product.format',
        string='Product Format',
        required=False)
    length = fields.Float(
        string='Length mm',
        required=False)
    height = fields.Float(
        string='Height mm',
        required=False)
    diameter = fields.Float(
        string='Diameter mm',
        required=False)
    
    origin = fields.Char(
        string='Origin', 
        required=False)
    supplier = fields.Char(
        string='Supplier', 
        required=False)
    latin_name = fields.Char(
        string='Latin name', 
        required=False)
    collection_site = fields.Char(
        string='Collection site',
        required=False)
    info_frs = fields.Char(
        string='Info frs',
        required=False)
    # divers
    miscellaneous = fields.Char(
        string='Miscellaneous', 
        required=False)
    