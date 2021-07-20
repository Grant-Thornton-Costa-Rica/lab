# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import re

class referenceDocument(models.Model):
    _name = 'reference.document'
    _description = 'reference document'
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

    