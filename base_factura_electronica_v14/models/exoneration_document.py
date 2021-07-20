# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import re

class exonerationDocument(models.Model):
    _name = 'exoneration.document'
    _description = 'exoneration document'

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

    