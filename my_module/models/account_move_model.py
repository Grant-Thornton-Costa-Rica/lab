from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
log = logging.getLogger(__name__)

class accountMoveModel(models.Model):
    _inherit = 'account.move'
    _description = 'Modulo Account'

    metodo_pago = fields.Selection([('efectivo', 'Efectivo'), ('credito', 'Tarjeta Credito'), ('debito', 'Tarjeta Debito')], string="Metodo Pago")

    def action_post(self):
        log.info("--------------------- " + str(self) + " ----------------------")
        if self.state == 'draft':
            self._check_cabys(self.invoice_line_ids, True)
        return super(accountMoveModel, self).action_post()

    def _check_cabys(self, lineas, obj = False):
        for rec in range(lineas):
            test = (lineas.codigo_cabys)
            log.info("--------------------- " + str(test) + " ----------------------")
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
        self._check_cabys(vals['invoice_line_ids'])
        return super(accountMoveModel, self).create(vals)

    def write(self, vals):
        for rec in self:
            linea = self._check_cabys(vals['line_ids'])
            if linea:
                linea
                return super(accountMoveModel, self).write(vals)

# --------------------- [[1, 4, {'price_unit': 336.75, 'credit': 336.75, 'amount_currency': -336.75, 'product_uom_id': False, 'product_id': False, 'tax_ids': [[6, False, []]], 'tax_base_amount': 2245, 'tax_tag_ids': [[6, False, []]], 'analytic_account_id': False, 'analytic_tag_ids': [[6, False, []]]}], [1, 5, {'price_unit': -2581.75, 'debit': 2581.75, 'amount_currency': 2581.75, 'date_maturity': '2021-08-31', 'product_uom_id': False, 'product_id': False, 'tax_ids': [[6, False, []]], 'tax_repartition_line_id': False, 'tax_tag_ids': [[6, False, []]], 'analytic_account_id': False, 'analytic_tag_ids': [[6, False, []]]}], [1, 6, {'tax_ids': [[6, False, [1]]], 'tax_repartition_line_id': False, 'tax_tag_ids': [[6, False, []]], 'analytic_account_id': False, 'analytic_tag_ids': [[6, False, []]]}], [1, 7, {'tax_ids': [[6, False, [1]]], 'tax_repartition_line_id': False, 'tax_tag_ids': [[6, False, []]], 'analytic_account_id': False, 'analytic_tag_ids': [[6, False, []]]}], [1, 8, {'tax_ids': [[6, False, [1]]], 'tax_repartition_line_id': False, 'tax_tag_ids': [[6, False, []]], 'analytic_account_id': False, 'analytic_tag_ids': [[6, False, []]]}], [0, 'virtual_824', {'account_id': 21, 'sequence': 11, 'name': '[E-COM08] Storage Box', 'quantity': 1, 'price_unit': 79, 'discount': 0, 'debit': 0, 'credit': 79, 'amount_currency': -79, 'date_maturity': False, 'currency_id': 2, 'partner_id': 14, 'product_uom_id': 1, 'product_id': 18, 'tax_ids': [[6, False, [1]]], 'tax_base_amount': 0, 'tax_exigible': True, 'tax_repartition_line_id': False, 'tax_tag_ids': [[6, False, []]], 'analytic_account_id': False, 'analytic_tag_ids': [[6, False, []]], 'recompute_tax_line': False, 'display_type': False, 'is_rounding_line': False, 'exclude_from_invoice_tab': False, 'codigo_cabys': '2325364'}]] ----------------------
