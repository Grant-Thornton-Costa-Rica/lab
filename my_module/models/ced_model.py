from odoo.exceptions import UserError
from odoo import models, fields, api, _

class Tipo_Cedula_Model(models.Model):
    _inherit = 'res.company'
    _description = 'Modulo Tipo Cedula'

    ced = fields.Selection([('juridica', 'Cedula Juridica'), ('fisica', 'Cedula Fisica')], string="Tipo Cedula")
    _sql_constraints = [
        ('check_vat_len', 'check(length(vat)<=11)', 'Debe ingresar al menos 10 digitos')
    ]
    

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



