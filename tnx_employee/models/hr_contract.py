from odoo import fields, models, api


class HrContractInherit(models.Model):
    _inherit = "hr.contract"
    contrat_categorie = fields.Selection(
        [('cdi', 'CDI'),
         ('cdd', 'CDD'),
         ('stagiaire', 'Stagiaire'),
         ('temporaire', 'Temporaire')
         ], string='Categorie de contrat', default="cdi",
        required=True, )
    hour_per_week = fields.Float(
        string="Nombre d'heures travaillé par semaine", related="resource_calendar_id.full_time_required_hours",
        required=True)
    base_salary = fields.Monetary('Salaire de base')
    hourly_salary = fields.Monetary('Salaire horaire ', compute='_get_hourly_salary')
    bonus = fields.Monetary('Prime')
    production_bonus_participant = fields.Monetary('Prime de production participant')
    allow_transport = fields.Monetary('Indemnité de transport')
    allow_family = fields.Monetary('Allocations familiales')
    wage = fields.Monetary('Wage', required=True, tracking=True, help="Employee's monthly gross wage.",
                           compute='_compute_base_salary')

    def _compute_base_salary(self):
        for record in self:
            record.wage = record.base_salary

    @api.depends('hour_per_week')
    def _get_hourly_salary(self):
        for rec in self:
            if rec.hour_per_week:
                rec.hourly_salary = rec.base_salary / ((rec.hour_per_week * 52) / 12)
            else:
                rec.hourly_salary = 0
