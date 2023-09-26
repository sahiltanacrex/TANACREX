from email.policy import default
import math
from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError

LINE_DIAMETER = {
    '10': 6.35,
    '12': 7.62,
    '13': 8.26,
    '14': 8.90,
    '16': 10.16,
    '17': 10.80,
    '18': 11.43,
    '20': 12.70,
    '22': 13.97,
    '24': 15.24,
    '26': 16.51,
    '28': 17.78,
    '30': 19.05,
    '32': 20.32,
    '34': 21.59,
    '36': 22.86,
    '40': 25.40,
    '44': 27.94,
    '48': 30.48,
    '54': 34.29,
    '60': 38.10,
    '70': 44.45,
    '80': 50.80,
    '90': 57.15,
    '100': 63.50
}


class Product_template(models.Model):
    _inherit = "product.template"
    hs_code = fields.Many2one("hscode.product", string="Hs Code")
    color = fields.Char(string="Couleur", help="Choose your color")

    detailed_type = fields.Selection(default="product")
    donneur_ordre = fields.Many2one("res.partner", string="Donneur d'ordre")
    ref_donneur_ordre = fields.Char(string=" Réf. donneur d'ordre")

    # matiere_id = domain("[('type_id', '=', type_id)]")

    @tools.ormcache()
    def _get_default_uom_id(self):
        # Deletion forbidden (at least through unlink)
        return self.env.ref('tnx_product.product_uom_hundred')

    uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_uom_id, required=True,
        help="Default unit of measure used for all stock operations.")

    uom_po_id = fields.Many2one(
        'uom.uom', 'Purchase UoM',
        default=_get_default_uom_id, required=True,
        help="Default unit of measure used for purchase orders. It must be in the same category as the default unit of measure.")

    @api.onchange("product_type")
    def _onchange_surface(self):
        for record in self:
            if record.product_type in ["button", "other"]:
                record.surface = 0
                record.length = 0
                record.wide = 0
                record.side = 0
                record.radius = 0
                if record.product_type == "other":
                    record.form = "other"
            elif record.product_type in ["label", "sticker"]:
                record.line = 0
                record.diameter = 0
                record.number_holes = 0

    origin = fields.Char(string="Origine", required=False)
    supplier = fields.Char(string="Fournisseur", required=False)
    latin_name = fields.Char(string="Nom latin", required=False)
    collection_site = fields.Char(string="Site de collecte", required=False)
    info_frs = fields.Char(string="Info frs", required=False)
    # divers
    miscellaneous = fields.Char(string="Divers", required=False)
    client_order = fields.Char(string="Bon de commande client", required=False)

    # ! add fields
    product_type = fields.Selection(
        [
            ("ruban", "Ruban"),
            ("button", "Bouton"),
            ("label", "Etiquette"),
            ("sticker", "Autocollant"),
            ("satin_a_lysiere", "Satin à Lysière"),
            ("satin", "Satin"),
            ("satin_recycle", "Satin recyclé"),
            ("encre", "Encre"),
            ("nylon", "Nylon"),
            ("dp", "DP"),
            ("other", "Autres"),
        ],
        string="Type du produit",
    )

    material = fields.Char("Matière", related='material_id.name')
    material_id = fields.Many2one(
        comodel_name='product.material',
        string='Matière',
        required=False, domain="[('product_type','=', product_type)]")
    thickness = fields.Float("Epaisseur (mm)")
    customer_reference = fields.Char("Référence Client")
    partner_id = fields.Many2one("res.partner", string="Client", store=True)

    # field based on condition
    # ?if button_type = button
    line = fields.Float("Ligne")
    diameter = fields.Float(string="Diamètre (mm)", required=False)
    surface = fields.Float(
        "Surface (mm²)",
    )
    dimension = fields.Char(sting="Dimension", compute="_compute_dimension")
    form = fields.Selection(
        [
            ("rectangle", "Rectangle"),
            ("square", "Carré"),
            ("circle", "Cercle"),
            ("other", "Other")
        ], default="rectangle"
            )
    
    def get_right_number(self, val):
        val_string = str(val)
        val_split = val_string.split('.')
        if len(val_split) == 1:
            return '{:,}'.format(int(val)).replace(',', ' ')
        if int(val_split[1]) > 0:
            return '{:,}'.format(val).replace(',', ' ')
        else:
            return '{:,}'.format(int(val)).replace(',', ' ')

    @api.depends("line", "form", "length", "wide", "side", "surface")
    def _compute_dimension(self):
        for record in self:
            record.dimension = False
            if record.product_type == 'button':
                # record.dimension = '' + record.line + ' L'
                record.dimension = '%sL' % record.get_right_number(record.line)
            elif record.product_type == 'other':
                # record.dimension = '' + record.surface + ' mm²'
                record.dimension = '%smm²' % record.get_right_number(record.surface)
            else:
                if record.form == 'rectangle':
                    # record.dimension = '' + record.lenght + 'mm' 
                    record.dimension = '%smm x %smm' % (record.get_right_number(record.length), record.get_right_number(record.wide))
                elif record.form == 'square':
                    record.dimension = '%smm x %smm' % (record.get_right_number(record.side), record.get_right_number(record.side))
                else:
                    record.dimension = '%smm²' % record.get_right_number(record.surface)

    @api.onchange("form")
    def _onchage_form(self):
        for record in self:
            record.surface = 0
            record.length = 0
            record.wide = 0
            record.side = 0
            record.radius = 0
    
    @api.onchange("line", "diameter", "length","wide", "side", "radius")
    def _onchange_dimension(self):
        for record in self:
            if record.product_type == "button":
                record.surface = math.pi * ((record.diameter /2) ** 2)
            if record.form == 'rectangle':
                record.surface = record.length * record.wide
            if record.form == 'square':
                record.surface = record.side ** 2
            if record.form == 'circle':
                record.surface = math.pi * (record.radius ** 2)

    @api.onchange('line')
    def _onchange_line(self):
        for rec in self:
            if rec.line:
                line = int(rec.line)
                rec.diameter = LINE_DIAMETER.get(str(line)) or 0.0

    number_holes = fields.Integer("Nombre de trous")

    # ? if sticker or a label
    # ! search surface  by this fields
    length = fields.Float(string="Longueur (mm)", required=False)
    # height = fields.Float(string="Hauteur", required=False)
    side = fields.Float(string="Côté (mm)", required=False)
    wide = fields.Float(string="Largeur (mm)", required=False)
    radius = fields.Float(string="Rayon (mm)", required=False)


    # TODO BAT here

    employee_validator_id = fields.Many2one("hr.employee", string="Validateur")
    bat_date = fields.Date("Date")
    validation_tools = fields.Char("Moyen de validation")
    attachment_ids = fields.Binary("Fichier BAT", attachment=True)


    def action_send_mail_bat(self):
        # import pudb; pudb.set_trace()
        if not self.name or not self.partner_id.name or not self.bat_date:
            raise UserError(
                _(
                    f"Veuillez vérifier que les champs nom et client et date BAT sont bien remplis."
                )
            )
        else:
            file_name = f"BAT_{self.name}_{self.partner_id.name}_{self.bat_date}"
        self.ensure_one()
        attachment = {
            "name": file_name,
            "datas": self.attachment_ids,
            "res_model": "product_template",
            "type": "binary",
        }

        id = self.env["ir.attachment"].create(attachment)

        ir_model_data = self.env["ir.model.data"]

        try:
            template_id = ir_model_data._xmlid_to_res_id(
                "tnx_product.send_mail_bat", raise_if_not_found=False
            )

        except ValueError:
            template_id = False
        ctx = {
            "default_model": "product.template",
            "default_res_id": self.ids[0],
            "default_use_template": bool(template_id),
            "default_template_id": template_id,
            "default_composition_mode": "comment",
            "default_attachment_ids": [(4, id.id, 0)] if self.attachment_ids else None,
        }

        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }

    devise = fields.Many2one(
        'res.currency', string='Devise', default=lambda self: self.env['res.currency'].search([('name', '=', 'MGA')]))
    minimum_price = fields.Monetary(
        "Prix au forfait",
        default=0,
        digits="Prix au forfait",
        help="Prix de vente minimum pour l'articles",
        currency_field='devise',
    )
    qty_min = fields.Integer("Quantité minimum", store=True, default=0)
    tax_string_min = fields.Char(compute="_compute_tax_string_min")

    @api.depends("taxes_id", "minimum_price")
    def _compute_tax_string_min(self):
        for record in self:
            record.tax_string_min = record._construct_tax_string(
                record.minimum_price)


class HsCode(models.Model):
    _name = "hscode.product"
    _rec_name = "hs_code"
    name = fields.Char("Désignation")
    hs_code = fields.Char("Hs Code")
