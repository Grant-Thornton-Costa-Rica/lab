from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _

class companyModel(models.Model):
    _inherit = 'res.company'
    _description = 'Modulo Tipo Cedula'

    ced = fields.Selection([('juridica', 'Cedula Juridica'), ('fisica', 'Cedula Fisica')], string="Tipo Cedula")    

@api.onchange('vat')
def _onchange_ced(self):
    for rec in self:
        if rec.vat:
            if len(rec.vat) <= 9:
                rec.ced = 'fisica'
            elif len(rec.vat) > 9:
                rec.ced = 'juridica'

def _check_vat(self):
    for rec in self:
        if rec.vat:
            if len(rec.vat) >= 9 and rec.ced == 'juridica':
                raise ValidationError('La Cedula Fisica tiene que ser de 9 digitos')
            elif len(rec.vat) < 11 and rec.ced == 'fisica':
                raise ValidationError('La Cedula Juridica tiene que ser de 11 digitos')



