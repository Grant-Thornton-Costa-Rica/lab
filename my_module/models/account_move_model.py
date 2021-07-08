from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
log = logging.getLogger(__name__)

class accountMoveModel(models.Model):
    _inherit = 'account.move'
    _description = 'Modulo Account'

    metodo_pago = fields.Selection([('efectivo', 'Efectivo'), ('credito', 'Tarjeta Credito'), ('debito', 'Tarjeta Debito')], string="Metodo Pago")

    def action_post(self):
        if self.state == 'draft':
            self._check_cabys(vals['invoice_line_ids'])
        super(accountMoveModel, self).action_post()

    def _check_cabys(self, lineas):
        for rec in lineas:
            cabys = (rec[2]['codigo_cabys'])
            if cabys:
                if cabys.isdigit():
                    raise ValidationError("Debe ingresar solo numeros en Codigo Cabys")
            else:
                raise ValidationError("No existe el registro del Codigo Cabys")

    @api.model
    def create(self, vals):
        self._check_cabys(vals['invoice_line_ids'])
        return super(accountMoveModel, self).create(vals)

    @api.model
    def write(self, vals):
        self._check_cabys(vals['invoice_line_ids'])
        res = super(accountMoveModel, self).write(vals)
        return res

