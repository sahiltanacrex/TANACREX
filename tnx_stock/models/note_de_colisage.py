from odoo import _, fields, models, api

from collections import defaultdict


class NoteDeColisage(models.TransientModel):
    _name = "note.colisage.wizard"
    name = fields.Char()
    partner_id = fields.Many2one("res.partner", string="Client")
    stock_picking_ids = fields.Many2many(
        "stock.picking", "colisage_id", string="Stock selected"
    )
    poids_net = fields.Float()
    poids_brut = fields.Float()
    description = fields.Char()
    move_id = fields.Many2one("account.move", string="Move")
    product_ids = fields.Many2many(comodel_name='product.product')
    inconterm = fields.Text()
    origin = fields.Text()
    note_de_colisage_line_ids = fields.One2many(
        comodel_name='note.de.colisage.line', inverse_name='note_colisage_id')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        self.name = 'Packing list' if self.partner_id.lang != 'fr_FR' else 'Note de colisage'

    def report_colisage(self):
        return self.env.ref("tnx_stock.action_tnx_package_report").report_action(self)

    def get_clean_data(self):
        packings = set(self.note_de_colisage_line_ids.mapped('packing_number'))
        product_group_by_packings = defaultdict(dict)
        for packing in packings:
            packing = int(packing)
            line_ids = self.note_de_colisage_line_ids.filtered(
                lambda l: int(l.packing_number) == packing)
            product_group_by_packings[str(packing)].update({
                'line_ids': line_ids,
                'gross_weight': sum(line.gross_weight for line in line_ids),
                'net_weight': sum(line.net_weight for line in line_ids),
                'items_count': sum(line.items_count for line in line_ids)
            })
        return product_group_by_packings

    def get_article_total_by_category(self):
        product_types = set(self.note_de_colisage_line_ids.mapped(
            'product_id.product_type'))
        out = list()
        for product_type in product_types:
            items_count = int(sum(line.bags * line.items_count for line in self.note_de_colisage_line_ids.filtered(
                lambda line_id: line_id.product_id.product_type == product_type)))

            out.append((items_count, product_type))
        return out

    def get_formatted_qty(self, qty):
        result = f'{qty:,.2f}'.split('.')[0]
        return result.replace(',', ' ')

    def get_formatted_weight(self, weight):
        result = f'{weight:,.1f}'
        return result.replace(',', ' ').replace('.', ',')


class NoteDeColisageLine(models.TransientModel):
    _name = 'note.de.colisage.line'

    product_id = fields.Many2one(comodel_name='product.product')
    bags = fields.Integer()
    packing_number = fields.Integer()
    note_colisage_id = fields.Many2one(comodel_name='note.colisage.wizard')
    product_ids = fields.Many2many(
        comodel_name='product.product', related='note_colisage_id.product_ids')
    gross_weight = fields.Float()
    net_weight = fields.Float()
    items_count = fields.Float()
    bc_client = fields.Char(related='product_id.product_tmpl_id.client_order')
