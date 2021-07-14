# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class resCompany(models.Model):
    _inherit = 'res.company'
    api_url = fields.Char(string='Servicio Web Url',default='https://bmservice-dev.azurewebsites.net/BMService.svc?singleWsdl')
    user = fields.Char(string='Usuario')
    password = fields.Char(string='Contraseña')
    branch_office = fields.Char(string='Sucursal',default='1')
    terminal = fields.Char(string='Terminal',default='1')

    activity_code_ids = fields.One2many(
        string="Actividades economicas",
        comodel_name="activity.code",
        inverse_name="company_id",
    )

    identification_type_id = fields.Many2one('identification.type', string='Tipo identificación',domain="[('active','=',True)]")
    canton_id = fields.Many2one('res.country.canton', string='Cantón')
    district_id = fields.Many2one('res.country.district', string='Distrito')
    neighborhood_id = fields.Many2one('res.country.neighborhood', string='Barrio')
    country_code = fields.Char(compute='_compute_country_code', string='country code')

    @api.depends('country_id')
    def _compute_country_code(self):
        self.country_code = self.country_id.code

    @api.constrains('branch_office')
    def _constrains_branch_office(self):
        for record in self:
            if not re.search('^\d+$',record.branch_office):
                raise ValidationError("La sucursal debe contener solo números")
        
    @api.constrains('terminal')
    def _constrains_terminal(self):
        for record in self:
            if not re.search('^\d+$',record.terminal):
                raise ValidationError("La terminal debe contener solo números")
        



    