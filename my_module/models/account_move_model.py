from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
log = logging.getLogger(__name__)

class accountMoveModel(models.Model):
    _inherit = 'account.move'
    _description = 'Modulo Account'

    metodo_pago = fields.Selection([('efectivo', 'Efectivo'), ('credito', 'Tarjeta Credito'), ('debito', 'Tarjeta Debito')], string="Metodo Pago")

    def action_post(self):
        log.info(" action_post: --------------------- " + str(self) + " ----------------------")
        if self.state == 'draft':
            self._check_cabys(self.invoice_line_ids, True)
        return super(accountMoveModel, self).action_post()

    def _check_cabys(self, lineas, obj = False):
        for rec in lineas:
            log.info("_check_cabys: --------------------- " + str(lineas) + " ----------------------")
            if obj:
                cabys = rec.codigo_cabys
            else:
                cabys = (rec[2]['codigo_cabys'])
            if cabys:
                if not cabys.isdigit():
                    raise ValidationError("Debe ingresar solo numeros en Codigo Cabys")
            else:
                raise ValidationError("No existe el registro del Codigo Cabys")

    @api.model
    def create(self, vals):
        log.info("create: --------------------- " + str(vals) + " ----------------------")
        self._check_cabys(vals['invoice_line_ids'])
        return super(accountMoveModel, self).create(vals)

    def write(self, vals):
        res = super(accountMoveModel, self).write(vals)
        for rec in res:
            log.info("write: --------------------- " + rec.id + " ---------------------")
            cabys = self._check_cabys(vals['line_ids'])
        return res

