# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class taxCode(models.Model):
    _name = 'tax.code'
    _description = 'tax code'

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

    