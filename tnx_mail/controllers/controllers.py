# -*- coding: utf-8 -*-
# from odoo import http


# class TnxMail(http.Controller):
#     @http.route('/tnx_mail/tnx_mail', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_mail/tnx_mail/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_mail.listing', {
#             'root': '/tnx_mail/tnx_mail',
#             'objects': http.request.env['tnx_mail.tnx_mail'].search([]),
#         })

#     @http.route('/tnx_mail/tnx_mail/objects/<model("tnx_mail.tnx_mail"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_mail.object', {
#             'object': obj
#         })
