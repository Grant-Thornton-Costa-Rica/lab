# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
class activityCode(models.Model):
    _name = 'activity.code'
    _description = 'Economic activity code'
    _rec_name = 'display_name'
    _order = "sequence,id"

    display_name = fields.Char(compute='_compute_display_name',)
    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código', size = 6)
    sequence = fields.Integer(string='Secuencia',default=0,)
    active = fields.Boolean(string='Activo', default = True)
    company_id = fields.Many2one(
        string="Compañia",
        comodel_name="res.company",
        ondelete="set null",
        default=lambda self: self.env['res.company']._company_default_get('activity.code')
    )
   
    
    @api.depends('code','name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '{}-{}'.format(record.code,record.name)
       
    @api.constrains('code')
    def _constrains_code(self):
        for record in self:
            if re.search('^\d+$',record.code):
                if len(record.code) < 6:
                    raise ValidationError("EL código de la actividad económica debe contener 6 caracteres")
            else:
                raise ValidationError("EL código de la actividad económica debe contener solo números")