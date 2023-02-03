# -*- coding: utf-8 -*-
# from odoo import http


# class TnxEmployee(http.Controller):
#     @http.route('/tnx_employee/tnx_employee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tnx_employee/tnx_employee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tnx_employee.listing', {
#             'root': '/tnx_employee/tnx_employee',
#             'objects': http.request.env['tnx_employee.tnx_employee'].search([]),
#         })

#     @http.route('/tnx_employee/tnx_employee/objects/<model("tnx_employee.tnx_employee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tnx_employee.object', {
#             'object': obj
#         })
