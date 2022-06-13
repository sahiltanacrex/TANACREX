import math
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Product_template(models.Model):
    _inherit = 'product.template'
    hs_code = fields.Many2one('hscode.product', string='Hs Code')
    color = fields.Char(
        string="Couleur",
        help="Choose your color"
    )

    @api.onchange('product_type')
    def _onchange_surface(self):
        for record in self:
            if record.product_type == 'button':
                record.length = 0
                record.height = 0
            elif record.product_type in ['label', 'sticker']:
                record.line = 0
                record.diameter = 0
                record.number_holes = 0
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

    # ! add fields
    product_type = fields.Selection([
        ('button', 'Boutton'),
        ('label', 'Etiquette'),
        ('sticker', 'Autocollant'),
        ('other', 'Autres'),
    ], string='Type du produit')

    material = fields.Char('Matière')
    thickness = fields.Char('Epaisseur')
    customer_reference = fields.Char('Référence Client')
    partner_id = fields.Many2one('res.partner', string='Client', store=True)

    # field based on condition
    # ?if button_type = button
    line = fields.Float('Ligne')
    diameter = fields.Float(
        string='Diamètre',
        required=False)
    surface = fields.Float('Surface',)

    @api.onchange('line', 'diameter', 'length', 'height')
    def _onchange_(self):
        for record in self:
            if self.product_type == 'button':
                self.surface = math.pi * self.diameter
            elif self.product_type in ['label', 'sticker']:
                self.surface = self.length * self.height
    number_holes = fields.Integer('Nombre de trous')

    # ? if sticker or a label
    # ! search surface  by this fields
    length = fields.Float(
        string='Longueur',
        required=False)
    height = fields.Float(
        string='Hauteur',
        required=False)
    # TODO BAT here

    employee_validator_id = fields.Many2one('hr.employee', string='Validateur')
    bat_date = fields.Date('Date')
    validation_tools = fields.Char('Moyen de validation')
    attachment_ids = fields.Binary("Fichier BAT", attachment=True)

    def action_send_mail_bat(self):
        # import pudb; pudb.set_trace()
        if not self.name or not self.partner_id.name or not self.bat_date:
            raise UserError(_(f'Veuillez remplir les champs {self.name} et {self.partner_id.name} et {self.bat_date}'))
        else:
            file_name = f"BAT_{self.name}_{self.partner_id.name}_{self.bat_date}"
        self.ensure_one()
        attachment = {
            'name': file_name,

            'datas': self.attachment_ids,

            'res_model': 'product_template',

            'type': 'binary'
        }

        id = self.env['ir.attachment'].create(attachment)

        ir_model_data = self.env['ir.model.data']

        try:
            template_id = ir_model_data._xmlid_to_res_id('tnx_product.send_mail_bat', raise_if_not_found=False)

        except ValueError:
            template_id = False
        ctx = {
            'default_model': 'product.template',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'default_attachment_ids': [(4, id.id, 0)] if self.attachment_ids else None,
        }

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
    minimum_price = fields.Monetary(
        'Prix au forfait', default=0,
        digits='Prix au forfait',
        help="Prix de vente minimum pour l'articles",
    )

    qty_min = fields.Float('Quantité minimum', store=True, default=0)
    tax_string_min = fields.Char(compute='_compute_tax_string_min')

    @api.depends('taxes_id', 'minimum_price')
    def _compute_tax_string_min(self):
        for record in self:
            record.tax_string_min = record._construct_tax_string(record.minimum_price)


class HsCode(models.Model):
    _name = 'hscode.product'
    name = fields.Char('Désignation')
    hs_code = fields.Char('Hs Code')
