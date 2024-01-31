import datetime

# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveInherit(models.Model):
    _inherit = "account.move"
    origin_tnx = fields.Char("Origine")
    name_bis = fields.Char("name_bis")
    c_f = fields.Char("C&F")
    gross_weight = fields.Char("Poids brute")
    net_weight = fields.Char("Poids net")
    volume = fields.Integer("Volume")
    seal_serial = fields.Char("Leads")
    container_serial = fields.Char("Conteneur")
    have_signature = fields.Boolean()

    seq_bis = fields.Char("Réference Facture", store=True, index=True)

    def _get_mail_template(self):
        return (
            'tnx_account.email_template_edi_invoice_inherit')


    @api.model
    def create(self, vals):
        res = super(AccountMoveInherit, self).create(vals)
        sale_line_ids = res.invoice_line_ids.mapped("sale_line_ids")
        if sale_line_ids:
            for line in sale_line_ids:
                if line.order_id:
                    res.origin_sale_id = line.order_id
                    break
        return res

    origin_sale_id = fields.Many2one(
        "sale.order",
        string="Bank",
    )
    picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        string="Bound transfer",
        store=True,
        compute="_compute_picking_ids",
        help="Related pickings "
             "(Seulement quand la facture a été generer depuis un bot de commande).",
    )

    bank_company_ids = fields.Many2many(
        "bank.company", "account_move_id", string="Banque"
    )

    delivery_adress = fields.Many2one("res.partner", string="Addresse de livraison")

    def set_sequence_year(self):
        date = datetime.date.today()
        year = date.strftime("%Y")
        return year

    def action_post(self):

        """if sequences is set and every param is right create sequences by button click

        Returns:
            _sequences_: test type of customer and set if EX, LS , VL
        """
        check_partner_type = self.partner_id.partner_type
        if self.move_type == "out_invoice":
            if check_partner_type and not self.seq_bis:
                get_ex = self.env["tnx.ex"]
                get_ls = self.env["tnx.ls"]
                get_vl = self.env["tnx.vl"]

                if check_partner_type == "ex":
                    self._set_seq(get_ex)

                if check_partner_type == "ls":
                    self._set_seq(get_ls)

                if check_partner_type == "vl":
                    self._set_seq(get_vl)

        values = super(AccountMoveInherit, self).action_post()
        # TODO arakaraka eto no name mipoitra satria ilay name natao invisible de name bis no afficher am form fa name tsotra ny any am tree
        if self.move_type == "out_invoice" and check_partner_type:
            self.update({"name_bis": self.name + "-" + check_partner_type.upper()})
        else:
            self.update({"name_bis": self.name})

        return values

    def _set_seq(self, type):
        """
        This function create the second sequences from invoice
        """
        if self.state == "draft" and self.move_type == "out_invoice":
            check_partner_type = self.partner_id.partner_type

            sec_last = 1

            get_last_id = type.search([], limit=1, order="id desc")

            last_create_date = get_last_id.create_date

            # !TODO this get_year is for testing if it was new year and it restart count
            if last_create_date:
                get_last_year = last_create_date.strftime("%Y")
            else:
                get_last_year = 1993

            # import pudb; pudb.set_trace()

            get_year = self.set_sequence_year()

            if get_last_id:
                if get_last_year == get_year:
                    sec_last = get_last_id.name + 1

            get_year = str(get_year)
            l = len(get_year)
            get_year = get_year[l - 2:]

            type.create(
                {
                    "name": sec_last,
                    "sequences_year": get_year,
                    "rel_invoice_id": self.id,
                    "rel_state_invoice": "posted",
                }
            )

            seq_bis = f"{check_partner_type.upper()} {sec_last}/{get_year}"
            self.write({"seq_bis": seq_bis})
            # self.update({'name':self.name + '-' + check_partner_type.upper()})

    @api.depends("invoice_line_ids", "invoice_line_ids.move_line_ids")
    def _compute_picking_ids(self):
        for invoice in self:
            invoice.picking_ids = invoice.mapped(
                "invoice_line_ids.move_line_ids.picking_id"
            )

    def action_show_picking(self):
        """
        This function returns an action that display existing pickings
        of given invoice.
        It can either be a in a list or in a form view, if there is only
        one picking to show.
        """
        self.ensure_one()
        form_view_name = "stock.view_picking_form"
        xmlid = "stock.action_picking_tree_all"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        if len(self.picking_ids) > 1:
            action["domain"] = "[('id', 'in', %s)]" % self.picking_ids.ids
        else:
            form_view = self.env.ref(form_view_name)
            action["views"] = [(form_view.id, "form")]
            action["res_id"] = self.picking_ids.id
        return action

    def get_customer_order(self, customer_bc):
        """
        Get BC client dans BC original
        """
        so = self.env["sale.order"].search([("name", "=", customer_bc)])
        return so.sale_order_partner

    def get_all_order_line(self, val):
        product_type = val.mapped('product_id').mapped('product_type')
        for el in val:
            print(el)

    def get_all_type(self, val):
        product_type = val.mapped('product_id').mapped('product_type')
        list_type = list(set(product_type))
        try:
            list_type.index(False)
            list_type.remove(False)
        except ValueError:
            pass
        list_type.sort()
        return list_type

    def get_total_price_type(self, val, type):
        sub_total_price = 0
        for el in val:
            if el.product_id.product_type == type:
                sub_total_price += el.price_subtotal
        return sub_total_price

    def total_amount_ex(self, freight, amount_total):
        return freight + amount_total

    def get_delivery_order_id(self, id):
        """
        get BL id
        """
        id_bl = []

        bc = self.env["sale.order"].search([("name", "=", id)])

        bl = self.env["stock.picking"].search([("origin", "=", bc.name)])

        for i in bl:
            id_bl.append(i.id)

        return id_bl

    def get_bl_name(self, id):
        """
        get BL name
        """
        bl_name = self.env["stock.picking"].search([("id", "=", id)])
        return bl_name.name

    def get_bl_qty_done(self, id_bl, id_product):
        """
        get product quantity done on stock.move
        """
        bl_id = self.env["stock.picking"].search([("id", "=", id_bl)])
        move_line_id = bl_id.move_ids_without_package.filtered(lambda x: x.product_id.id == id_product)[0]
        return move_line_id.quantity_done

    def get_bl_subtotal(self, qty, price):
        """
        get subtotal
        """
        return qty * price

    def get_bank(self, bank_id, currency_id):
        list_info = []
        get_len = len(bank_id) - 1
        count = 0
        for i in bank_id:
            serial_bank = self.env["bank.company.line"].search(
                [("res_currency_id", "=", currency_id), ("bank_id", "=", i.id)]
            )
            if serial_bank:
                list_info.append(serial_bank.bank_id.bank)
            if count < get_len:
                list_info.append(serial_bank.account_registration)
                list_info.append(" ,")
                count += 1
            else:
                list_info.append(serial_bank.account_registration)

        values = "".join([str(item) for item in list_info])
        return values

    def action_invoice_sent(self):
        res = super(AccountMoveInherit, self).action_invoice_sent()
        template = self.env["mail.template"].browse(
            res["context"]["default_template_id"]
        )
        partner_type = {
            "ex": "tnx_account.invoice_ex",
            "ls": "tnx_account.invoice_ls",
            "vl": "tnx_account.invoice_vl",
        }
        template.report_template = self.env.ref(
            partner_type.get(self.partner_id.partner_type, "tnx_account.invoice_ex")
        )
        return res

    def get_right_number(self, val):
        val = round(val, 2)
        val_string = str(val)
        val_split = val_string.split('.')
        if len(val_split) == 1:
            return '{:,}'.format(int(val)).replace(',', ' ')
        if int(val_split[1]) > 0:
            return '{:,}'.format(val).replace(',', ' ')
        else:
            return '{:,}'.format(int(val)).replace(',', ' ')

    def format_number_for_amount(self, num):
        formatted = "{:,.2f}".format(num).replace(",", " ")
        return formatted

    def get_type_false_number(self):
        product_type_false = self.invoice_line_ids.mapped('product_id').filtered(lambda p: p.product_type == False)
        return len(product_type_false)
