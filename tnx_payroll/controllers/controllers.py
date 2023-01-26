# -*- coding: utf-8 -*-
# from odoo import http


# class TnxPayroll(http.Controller):
#     @http.route('/tnx_payroll/tnx_payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_payroll/tnx_payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_payroll.listing', {
#             'root': '/tnx_payroll/tnx_payroll',
#             'objects': http.request.env['tnx_payroll.tnx_payroll'].search([]),
#         })

#     @http.route('/tnx_payroll/tnx_payroll/objects/<model("tnx_payroll.tnx_payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_payroll.object', {
#             'object': obj
#         })
