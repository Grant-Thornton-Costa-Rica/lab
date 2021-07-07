from odoo.exceptions import UserError
from odoo import models, fields, api, _

class Tipo_Cedula_Model(models.Model):
    _inherit = 'res.company'
    _description = 'Modulo Tipo Cedula'

    ced = fields.Selection([('juridica', 'Cedula Juridica'), ('fisica', 'Cedula Fisica')], string="Tipo Cedula")

@api.onchange('vat')
def _onchange_ced(self):
    for rec in self:
        if rec.vat <= 9:
            rec.ced = 'Cedula Fisica'
        elif rec.vat > 9:
            rec.ced = 'Cedula Juridica'


