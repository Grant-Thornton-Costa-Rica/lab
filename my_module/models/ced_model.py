from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _

class Tipo_Cedula_Model(models.Model):
    _inherit = 'res.company'
    _description = 'Modulo Tipo Cedula'

    ced = fields.Selection([('juridica', 'Cedula Juridica'), ('fisica', 'Cedula Fisica')], string="Tipo Cedula")    

@api.onchange('vat')
def _onchange_ced(self):
    for rec in self:
        if len(rec.vat) <= 9:
            rec.ced = 'Cedula Fisica'
        elif len(rec.vat) > 9:
            rec.ced = 'Cedula Juridica'

@api.constrains('vat','ced')
def _constrains_fieldname(self):
    for rec in self:
        if len(rec.vat) >= 9 and rec.ced == 'juridica':
            raise UserError(_('La Cedula Fisica tiene que ser de 9 digitos'))
        elif len(rec.vat) < 11 and rec.ced == 'fisica':
            raise UserError(_('La Cedula Juridica tiene que ser de 11 digitos'))

def _check_len_vat(self, cr, uid, ids, context=None):
    for rec in self.browse(cr, uid, ids, context=context):
        if len(rec.vat) < 9:
            return True
            print('Menor a 9')
    return False

_constraints = [
    (_check_len_vat, 'La longitud debe ser igual o mayor a 9 digitos', ['vat'])
]

@api.constrains('vat')
def _check_vat_len(self):
    for rec in self:
        if len(rec.vat) != 11:
            raise ValidationError(_('Must be 11 Characters'))



