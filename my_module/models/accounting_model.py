from odoo import models, fields, api

class accountMoveModel(models.Model):
    _inherit = 'account.move'
    _description = 'Modulo Account'

    metodo_pago = fields.Selection([('efectivo', 'Efectivo'), ('credito', 'Tarjeta Credito'), ('debito', 'Tarjeta Debito')], string="Metodo Pago")

    def action_invoice_open(self):
        if self.state == 'draft':
            self._check_cabys()
        super(accountMoveModel, self).action_invoice_open()

    def _check_cabys(self):
        for rec in self.invoice_line_ids:
            if rec.codigo_cabys and isinstance(rec.codigo_cabys, int):
                raise ValidationError("Debe ingresar solo numeros en Codigo Cabys")
