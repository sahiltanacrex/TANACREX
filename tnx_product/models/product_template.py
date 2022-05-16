from math import pi
from odoo import models, fields, api
class Product_template(models.Model):
    _inherit='product.template'

    hs_code = fields.Char(
        string='HS CODE',
        required=True)

    # product_format = fields.Selection([
    #     ('circle', 'Cercle'),
    #     ('rectangle', 'Rectangle'),
    #     ('other', 'Autres'),
    # ], string='Format du produit')
    
    

    @api.onchange('product_type')
    def _onchange_surface(self):
        for record in self:
            if record.product_type == 'button':
                record.surface= record.line * record.diameter   
                record.length=0
                record.height=0
                record.surface=0
            elif record.product_type in ['label','sticker']:
                record.surface = record.length * record.height
                record.line=0
                record.diameter=0
                record.surface=0
                record.number_holes=0
            # elif record.product_type == 'other':
            #     record.surface = 0
            
    
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

    #! add fields
    product_type = fields.Selection([
        ('button', 'Boutton'),
        ('label', 'Etiquette'),
        ('sticker', 'Autocollant'),
        ('other', 'Autres'),
    ], string='Type du produit')

    material = fields.Char('Matière')
    thickness = fields.Char('Epaisseur')
    customer_reference = fields.Char('Référence Client')
    partner_id = fields.Many2one('res.partner', string='Client')

    # field based on condition
    #?if button_type = button
    line = fields.Float('Ligne')
    diameter = fields.Float(
        string='Diamètre mm',
        required=False)

    surface = fields.Float('Surface')

    number_holes = fields.Integer('Nombre de trous')

    #? if sticker or a label
    #! search surface  by this fields
    length = fields.Float(
        string='Longueur mm',
        required=False)
    height = fields.Float(
        string='Hauteur mm',
        required=False)


    # TODO BAT here

    employee_validator_id = fields.Many2one('hr.employee', string='Validateur')
    bat_date = fields.Date('Date')
    validation_tools = fields.Char('Moyen de validation')
    # attachment_id = fields.Many2one('ir.attachment', string='Attachment', ondelete='cascade')
    attachment_ids = fields.Binary("Fichier BAT")