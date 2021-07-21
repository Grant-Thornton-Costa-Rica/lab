# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class productTemplate(models.Model):
    _inherit = 'product.template'

    product_code_type_id = fields.Many2one('product.code.type', string='Tipo de código',store=True,)
    cabys_code_id = fields.Many2one('cabys.code', string='Código Cabys',store=True,)

    is_other_charge = fields.Boolean(default=False)
    other_charge_doc_type = fields.Char()
    dont_delete = fields.Boolean(default=False)
        
    @api.onchange('type')
    def _onchange_type(self):
        if self.type == 'service':
            uom_id = self.env["uom.uom"].search([("is_services","=",True)], limit=1, order='id').id
            self.update({
              'uom_id':uom_id,
              'uom_po_id':uom_id
            })
            return {
                   'domain':{'uom_id': [('is_services','=',True)],'uom_po_id':[('is_services','=',True)]},
                   }
        else:
            uom_id = self.env["uom.uom"].search([], limit=1, order='id').id
            self.update({
              'uom_id':uom_id,
              'uom_po_id':uom_id
            })
            return {
                   'domain':{'uom_id': [('is_services','=',False)],'uom_po_id':[('is_services','=',False)]},
                   }

    def unlink(self):
        for record in self:
            if record.dont_delete:
                raise ValidationError('Este registro no se puede borrar ya que pertenece a la configuración básica de factura electrónica')
        return super(productTemplate, self).unlink()






    