from odoo import models, fields, api
class Product_template(models.Model):
    _inherit='product.template'

    hs_code = fields.Char(
        string='HS CODE',
        required=True)
    product_format_id = fields.Many2one(
        comodel_name='product.format',
        string='Format du produit',
        required=True)
    length = fields.Float(
        string='Longueur mm',
        required=False)
    height = fields.Float(
        string='Hauteur mm',
        required=False)
    diameter = fields.Float(
        string='Diamètre mm',
        required=False)
    
    origin = fields.Char(
        string='Origine', 
        required=False)
    supplier = fields.Char(
        string='Fournisseur', 
        required=False)
    latin_name = fields.Char(
        string='Nom latin', 
        required=False)
    collection_site = fields.Char(
        string='Site de collecte',
        required=False)
    info_frs = fields.Char(
        string='Info frs',
        required=False)
    # divers
    miscellaneous = fields.Char(
        string='Divers', 
        required=False)
    

    # TODO BAT here

    employee_validator_id = fields.Many2one('hr.employee', string='Validateur')
    bat_date = fields.Date('Date')
    validation_tools = fields.Char('Moyen de validation')
    # attachment_id = fields.Many2one('ir.attachment', string='Attachment', ondelete='cascade')
    attachment_ids = fields.Binary("Fichier BAT")