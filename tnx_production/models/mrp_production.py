# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning
import datetime


class MrpProduction(models.Model):
    """Manufacturing Orders"""

    _inherit = "mrp.production"

    partner_id = fields.Many2one("res.partner", string="client")
    order_id = fields.Many2one("sale.order", string="BC")
    sale_order_date = fields.Datetime(related='order_id.date_order')
    developments = fields.Selection(
        [("1", "0%"), ("2", "25%"), ("3", "50%"), ("4", "75%"), ("5", "100%")],
        default="1",
        string="Avancement",
    )
    check_bc = fields.Boolean("Check Bc")
    image_1920 = fields.Image("Image", related="product_id.image_1920")
    bc_client = fields.Char("Bc Client")
    line_product = fields.Float("Ligne", related="product_id.line")
    material_product = fields.Char(related="product_id.material")
    product_type = fields.Selection(
        "Type de produit", related="product_id.product_type"
    )
    color_product = fields.Char("Couleur", related="product_id.product_tmpl_id.color")
    categorie_id = fields.Many2one(
        "product.category",
        "Catégorie d'article",
        related="product_id.categ_id",
    )
    end_of_production = fields.Date(compute="_compute_end_of_production")

    @api.depends('date_planned_start', 'order_id.production_duration')
    def _compute_end_of_production(self):
        for record in self:

            record.end_of_production = record.date_planned_start + datetime.timedelta(days=record.order_id.production_duration)

    comment = fields.Text()

    def action_send_mail_odf(self):
        self.clear_caches()
        if self.partner_id.lang:
            self = self.with_context(lang=self.partner_id.lang)
        developments_perccent = dict(self._fields["developments"].selection).get(
            self.developments
        )

        if self.partner_id:
            template_id = self.env.ref("tnx_production.send_mail_order_manufacture").id
            compose_form_id = self.env.ref("mail.email_compose_message_wizard_form").id
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

    @api.depends("origin")
    def _compute_source_id(self):
        for production in self:
            if production.origin:
                devis_name = production.origin.split(" - ")
                if len(devis_name) > 1:
                    source = self.env["sale.order"].search(
                        [("name", "=", devis_name[1])]
                    )
                    if source:
                        try:
                            production.partner_id = source.partner_id
                            production.check_bc = True

                        except Exception as e:
                            print(e)
                            pass

    def report_analyse(self):
        ids = self.env.context.get("active_ids", [])
        productions = self.env["mrp.production"].browse(ids)
        return self.env.ref(
            "tnx_production.action_production_nexource_report"
        ).report_action(productions)
