# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class saleCondition(models.Model):
    _name = 'sale.condition'
    _description = 'Sales conditions'
    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código', size = 2 )
    active = fields.Boolean(string='Activo',default = True)

    @api.constrains('code')
    def _constrains_code(self):
        for record in self:
            if re.search('^\d+$',record.code):
                if len(record.code) < 2:
                    raise ValidationError("EL código debe contener 2 caracteres")
            else:
                raise ValidationError("EL código debe contener solo números")



    