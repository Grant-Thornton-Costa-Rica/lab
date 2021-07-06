from odoo import models, fields, api

class Tipo_Cedula_Model(models.Model):
    _name = 'm.cedula'
    _inherit = 'res.company'
    _description = 'Modulo Tipo Cedula'

    ced = fields.Selection([('juridica', 'Cedula Juridica'), ('fisica', 'Cedula Fisica')], string="Tipo Cedula")
    category_ids = fields.Many2many(
      'res.company.category', 'cedula_category_rel',
      'cedula_id', 'category_id',
      string='Tags')
     

