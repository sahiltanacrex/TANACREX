# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning
import datetime


class MrpProduction(models.Model):
    """Manufacturing Orders"""

    _inherit = "mrp.production"

    partner_id = fields.Many2one("res.partner", string="client")
    order_id = fields.Many2one(
        "sale.order", string="BC",compute='_set_fields_depends_on_origin', inverse="inverse_production_bc_fields",store=True)
    sale_order_date = fields.Datetime(compute='_set_fields_depends_on_origin',inverse="inverse_sale_order_date_bc_fields",store=True)
    developments = fields.Selection(
        [("1", "0%"), ("2", "25%"), ("3", "50%"), ("4", "75%"), ("5", "100%")],
        default="1",
        string="Avancement",
    )
    advancements = fields.Float('Avancement', compute='_compute_qty_development' , default=0.0)
    check_bc = fields.Boolean("Check Bc")
    image_1920 = fields.Image("Image", related="product_id.image_1920")
    bc_client = fields.Char(
        "Bc Client", compute='_set_fields_depends_on_origin',inverse="inverse_bc_client_fields",store=True)
    line_product = fields.Float("Ligne", related="product_id.line")
    dimension = fields.Char(sting="Dimension", related="product_id.product_tmpl_id.dimension")
    material_product = fields.Char(store=True, compute="_compute_material_product", default=lambda self: self.product_id.material_id.name if self.product_id else False)
    product_type = fields.Selection(
        "Type de produit", related="product_id.product_type", store=True
    )
    color_product = fields.Char(
        "Couleur", related="product_id.product_tmpl_id.color")
    categorie_id = fields.Many2one(
        "product.category",
        "Catégorie d'article",
        related="product_id.categ_id", store=True
    )
    end_of_production = fields.Date(compute="_compute_end_of_production")
    product_qty_delivered = fields.Float('Delivered Quantity', compute='_compute_qty_delivered_product', store=True , default=0.0)
    product_qty_still_to_be_delivered = fields.Float(compute='_compute_qty_still_to_be_delivered' , default=0.0)

    @api.depends('order_id')
    def _compute_qty_delivered_product(self):
        for production in self:
            if production.order_id and production.order_id.state == 'sale' and production.order_id.order_line.filtered(lambda line: line.product_id == production.product_id).mapped('qty_delivered'):
                production.product_qty_delivered = float(sum(production.order_id.order_line.filtered(lambda line: line.product_id == production.product_id).mapped('qty_delivered')))
            else:
                production.product_qty_delivered = 0.0


    def _compute_qty_still_to_be_delivered(self):
        for production in self:
            production.product_qty_still_to_be_delivered = production.product_qty - production.product_qty_delivered



    def _compute_qty_development(self):
        for production in self:
            production.advancements = float((production.product_qty_delivered / production.product_qty)*100)/100



    @api.depends('product_id', 'product_id.material_id')
    def _compute_material_product(self):
        for rec in self:
            if rec.product_id:
                if rec.product_id.material_id:
                    rec.material_product = rec.product_id.material_id.name
                else:
                    rec.material_product = False
            else:
                rec.material_product = False
            
    @api.depends('origin')
    def _set_fields_depends_on_origin(self):
        for production_id in self:
            production_id.bc_client = False
            production_id.sale_order_date = False
            production_id.order_id = False
            if production_id.origin:
                try:
                    origin_name = production_id.origin.split(' - ')[1]
                except IndexError:
                    origin_name = False
                if origin_name:
                    order_id = self.env['sale.order'].sudo().search(
                        [('name', '=', origin_name)])
                    production_id.bc_client = order_id.sale_order_partner
                    production_id.sale_order_date = order_id.date_order
                    production_id.order_id = order_id.id

    def inverse_production_bc_fields(self):
        for production_id in self:
            production_id.origin = production_id.order_id.name

    def inverse_sale_order_date_bc_fields(self):
        pass

    def inverse_bc_client_fields(self):
        pass

    @api.depends('date_planned_start', 'order_id.production_duration')
    def _compute_end_of_production(self):
        for record in self:

            record.end_of_production = record.date_planned_start + \
                datetime.timedelta(days=record.order_id.production_duration)

    comment = fields.Text()

    def action_send_mail_odf(self):
        self.clear_caches()
        if self.partner_id.lang:
            self = self.with_context(lang=self.partner_id.lang)
        developments_perccent = dict(self._fields["developments"].selection).get(
            self.developments
        )

        if self.partner_id:
            template_id = self.env.ref(
                "tnx_production.new_send_mail_order_manufacture_inherit").id
            compose_form_id = self.env.ref(
                "mail.email_compose_message_wizard_form").id
            ctx = {
                "default_model": "mrp.production",
                "default_res_id": self.id,
                "default_use_template": bool(template_id),
                "default_template_id": template_id,
                "default_composition_mode": "comment",
                "custom_layout": "mail.mail_notification_light",
                "force_email": True,
                "company_name": self.env.company.name,
                "company_id": self.env.company.id,
                "mail_partner_id": self.partner_id.id,
                "mail_partner_name": self.partner_id.name,
                "order_origin": self.order_id.name,
                "developments_states": developments_perccent,
                "subject": _('Status fabrication BC Client {}').format(self.bc_client if self.bc_client else '---'),
                "bc_client": self.bc_client if self.bc_client else '---',
            }
            return {
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "mail.compose.message",
                "views": [(compose_form_id, "form")],
                "view_id": compose_form_id,
                "target": "new",
                "context": ctx,
            }

    # @api.depends("origin")
    # def _compute_source_id(self):
    #     for production in self:
    #         if production.origin:
    #             devis_name = production.origin.split(" - ")
    #             if len(devis_name) > 1:
    #                 source = self.env["sale.order"].search(
    #                     [("name", "=", devis_name[1])]
    #                 )
    #                 if source:
    #                     try:
    #                         production.obc_clientrder_id = source
    #                         production.partner_id = source.partner_id
    #                         production.check_bc = True
    #                         production.bc_client = source.sale_order_partner
    #                     except Exception as e:
    #                         raise UserError(e)

    # @api.depends("origin")
    # def _compute_source_id(self):
    #     for production in self:
    #         if production.origin:
    #             devis_name = production.origin.split(" - ")
    #             if len(devis_name) > 1:
    #                 source = self.env["sale.order"].search(
    #                     [("name", "=", devis_name[1])]
    #                 )
    #                 if source:
    #                     try:
    #                         production.obc_clientrder_id = source
    #                         production.partner_id = source.partner_id
    #                         production.check_bc = True
    #                         production.bc_client = source.sale_order_partner

    #                     except Exception as e:
    #                         print(e)
    #                         pass

    def report_analyse(self):
        ids = self.env.context.get("active_ids", [])
        productions = self.env["mrp.production"].browse(ids)
        return self.env.ref(
            "tnx_production.action_production_nexource_report"
        ).report_action(productions)
