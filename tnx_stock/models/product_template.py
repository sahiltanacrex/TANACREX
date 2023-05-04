from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_right_number(self, val):
        val_string = str(val)
        val_split = val_string.split('.')
        if len(val_split) == 1:
            return '{:,}'.format(int(val)).replace(',', ' ')
        if int(val_split[1]) > 0:
            return '{:,}'.format(val).replace(',', ' ')
        else:
            return '{:,}'.format(int(val)).replace(',', ' ')
    
    def format_number_for_weight(self, num):
        formatted = "{:,.2f}".format(num).replace(",", " ")
        return formatted