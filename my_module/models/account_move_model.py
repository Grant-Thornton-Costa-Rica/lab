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
            self._check_cabys()
        super(accountMoveModel, self).action_post()

    def _check_cabys(self):
        for rec in self.invoice_line_ids:
            if rec.codigo_cabys:
                if not isinstance(rec.codigo_cabys, int):
                    raise ValidationError("Debe ingresar solo numeros en Codigo Cabys")
            else:
                raise ValidationError("No existe el registro del Codigo Cabys")

    @api.model
    def create(self, vals):
        self._check_cabys()
        return super(accountMoveModel, self).create(vals)

    def write(self, vals):
        log.info('Entrando al metodo write')
        self._check_cabys()
        res = super(accountMoveModel, self).write(vals)
        return res
        log.info('Saliendo del metodo write')

