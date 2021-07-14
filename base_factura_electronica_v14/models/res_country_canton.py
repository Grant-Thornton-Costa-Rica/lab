from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class resCountryCanton(models.Model):
    _name = 'res.country.canton'
    _description = 'description'

    name = fields.Char(string='Nombre')
    code = fields.Char(string='Codigo')
    state_id = fields.Many2one('res.country.state', string='Provincia')

    @api.constrains('code')
    def _constrains_code(self):
        for record in self:
            if re.search('^\d+$',record.code):
                if len(record.code) < 2:
                    raise ValidationError("EL código debe contener 2 caracteres")
            else:
                raise ValidationError("EL código debe contener solo números")
        

    