from odoo import models, fields, api

class Tipo_Cedula_Model(models.Model):
    _name = 'm.cedula'
    _description = 'Modulo Tipo Cedula'
    _rec_name = 'partner_id'

    ced = fields.Selection([('juridica', 'Cedula Juridica'), ('fisica', 'Cedula Fisica')], string="Tipo Cedula")

