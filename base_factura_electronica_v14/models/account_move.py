# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime,timezone
import threading
import pytz
import re
import logging
log = logging.getLogger(__name__)

class accountMove(models.Model):
    _inherit = 'account.move'

    numeric_key = fields.Char(string='Clave númerica',copy=False)
    consecutive = fields.Char(string='Número Consecutivo',copy=False)
    document_type_id = fields.Many2one('document.type', string='Tipo comprobante',domain=lambda self: self._document_type_domain(),default=lambda self: self.default_document_type())
    activity_code_id = fields.Many2one('activity.code', string='Actividad económica',default=lambda self: self.default_activity_code())
    payment_method_id = fields.Many2one('payment.method', string='Método de pago',)
    reference_document_id = fields.Many2one('reference.document', string='Tipo documento referencia')
    reference_code_id = fields.Many2one('reference.code', string='Código referencia')
    related_document = fields.Many2one('account.invoice', string='Documento referencia')
    xml_invoice_fname = fields.Char(string='',copy=False)
    xml_invoice = fields.Binary(string='Comprobante XML',copy=False)
    pdf_invoice_fname = fields.Char(string='',copy=False)
    pdf_invoice = fields.Binary(string='Comprobante PDF',copy=False)
    xml_mh_fname = fields.Char(string='',copy=False)
    xml_mh = fields.Binary(string='Aceptación Ministerio Hacienda',copy=False)
    is_debit_note = fields.Boolean(string='Nota débito')
    situation = fields.Selection([
        ('1', 'Normal'),
        ('2', 'Contingencia'),
        ('3', 'Sin Internet'),
    ], string='Emisión comprobante',default='1')
    invoice_state = fields.Selection([
        ('draft', 'borrador'),
        ('in_progress', 'En curso'),
        ('queue', 'En cola'),
        ('error','Error'),
        ('invalid', 'XML inválido'),
        ('processing','Procesando'),
        ('accepted','Aceptada'),
        ('rejected','Rechazada'),
        ('response_unhandled','Respuesta no controlada'),
        ('unauthorized','No autorizado'),
        ('internal','Registro interno'),
    ], string='Situación',default="draft",copy=False)
    date_issued = fields.Char(string='Fecha emisión',readonly=True)
    total_taxed_service = fields.Float(digits=(15, 2),compute='_compute_total_taxed_and_untaxed_service',string='Total servicio gravados',)
    total_without_taxed_service = fields.Float(digits=(15, 2),compute='_compute_total_taxed_and_untaxed_service',string='Total servicio exentos',)
    total_taxed_goods = fields.Float(digits=(15, 2),compute='_compute_total_taxed_and_untaxed_goods',string='Total mercancias gravadas',)
    total_without_taxed_goods = fields.Float(digits=(15, 2),compute='_compute_total_taxed_and_untaxed_goods',string='Total mercancias exentos',)
    total_exonerate_service = fields.Float(digits=(15, 2),compute='_compute_total_exonerate_goods_service',string='Total servicios exonerados',)
    total_exonerate_goods = fields.Float(digits=(15, 2),compute='_compute_total_exonerate_goods_service',string='Total bienes exonerados',)
    total_exonerate = fields.Float(digits=(15, 2),compute='_compute_total_exonerate_goods_service',string='Total Exonerado',)
    total_sale = fields.Float(digits=(15, 2),compute='_compute_total_sale',string='Total venta',)
    total_discount = fields.Float(digits=(15, 2),compute='_compute_total_discount',string='Total descuento',)
    total_taxes_without_exoneration = fields.Float(digits=(15, 2),compute='_compute_total_taxes_without_exoneration',string='Total impuesto sin exoneración',)
    total_taxed = fields.Float(digits=(15, 2),compute='_compute_total_taxed',string='Total impuesto',)
    document_code = fields.Char(compute='_compute_document_code',)
    total_other_charges = fields.Float(digits=(15, 2),compute='_onchange_total_other_charges',)
    exits_third_party_other_charger = fields.Boolean(compute='_compute_exits_third_party_other_charger', string='')
    
    @api.depends('invoice_line_ids')
    def _compute_exits_third_party_other_charger(self):
        self.exits_third_party_other_charger = False
        filter_list = filter(lambda line: line.product_id.is_other_charge == True, self.invoice_line_ids)
        for line in filter_list:
            if line.product_id.other_charge_doc_type == '04':
                self.exits_third_party_other_charger = True
                return

    @api.onchange('total_other_charges')
    def _onchange_total_other_charges(self):
        for record in self:
            other_charges = filter(lambda line: line.product_id.is_other_charge == True, record.invoice_line_ids)
            total = 0
            for other in other_charges:
                total = total + other.price_subtotal
            record.total_other_charges = total
            
    @api.onchange('related_document')
    def _onchange_related_document(self):
        if self.related_document:
            self.invoice_line_ids = False
            document = False
            if self.type == 'out_invoice':
                if 'default_is_debit_note' in self._context.keys():
                    debit_note = self._context['default_is_debit_note']
                    if debit_note:
                        document = self.env['document.type'].search([('code','=','02')])
                        self.related_document.partner_id.document_type_id = document
            elif self.type == 'out_refund':
                document = self.env['document.type'].search([('code','=','03')])
                self.related_document.partner_id.document_type_id = document

            lines=[]
            for line in self.related_document.invoice_line_ids:
                lines.append( 
                (0,0,{
                'product_id':line.product_id,
                'name':line.name,
                'third_party_id':line.third_party_id,
                'account_id':line.account_id,
                'quantity':line.quantity,
                'uom_id':line.uom_id,
                'price_unit':line.price_unit,
                'invoice_line_tax_ids':[(6,0,line.invoice_line_tax_ids.ids)]  
                }) 
                )

            return {'value':{
              'partner_id':self.related_document.partner_id,
              'invoice_line_ids':lines,
            }}
    
    def default_document_type(self):
        if 'default_is_debit_note' in self._context.keys():
            debit_note = self._context['default_is_debit_note']
            if debit_note:
                return self.env['document.type'].search([('code','=','02')]).id
        if 'type' in self._context.keys():
            invoice_type = self._context['type']
            if invoice_type == 'out_refund':
                return self.env['document.type'].search([('code','=','03')]).id
            elif invoice_type == 'out_invoice':
                return self.env['document.type'].search([('code','=','01')]).id
            elif invoice_type == 'in_invoice':
                return self.env['document.type'].search([('code','=','99')]).id

    def _document_type_domain(self):
        domain = []

        if 'default_is_debit_note' in self._context.keys():
            debit_note = self._context['default_is_debit_note']
            if debit_note:
                return [('code','in',['02'])]

        if 'type' in self._context.keys():
            invoice_type = self._context['type']
            if invoice_type == 'out_refund':
                domain = [('code','in',['03'])]
            elif invoice_type == 'out_invoice':
                domain = [('code','in',['01','04','09'])]
            elif invoice_type == 'in_invoice':
                domain = [('code','in',['99','08'])]

        return domain          

    @api.depends('total_taxes_without_exoneration','total_exonerate')
    def _compute_total_taxed(self):
        for record in self:
            total_exonerate = 0
            lines = filter(lambda line: line.product_id.is_other_charge == False, record.invoice_line_ids)
            for line in lines:
                total_exonerate = total_exonerate + line.exonerate_amount
            record.total_taxed = record.total_taxes_without_exoneration - total_exonerate

    @api.depends('invoice_line_ids')
    def _compute_total_exonerate_goods_service(self):
        for record in self:
            total_exonerate_service = 0
            total_exonerate_goods = 0
            lines = filter(lambda line: line.product_id.is_other_charge == False, record.invoice_line_ids)
            for line in lines:
                if line.product_id.type == 'service':
                    if line.invoice_line_tax_ids:
                        total_exonerate_service = total_exonerate_service + line.total_exonerate_amount
                else:
                    if line.invoice_line_tax_ids:
                        total_exonerate_goods = total_exonerate_goods + line.total_exonerate_amount

            record.total_exonerate_goods = total_exonerate_goods
            record.total_exonerate_service = total_exonerate_service
            record.total_exonerate = total_exonerate_goods + total_exonerate_service

    def default_activity_code(self):
        default = self.env['activity.code'].search([('sequence','=',0),('company_id','=',self.env.user.company_id.id)])
        return default.id

    @api.onchange('partner_id')
    def _onchange_partner_id_default_values(self):
        for record in self:
            if record.partner_id:
                record.payment_method_id = record.partner_id.payment_method_id.id
                if record.type == 'in_invoice':
                    document = record.env['document.type'].search([('code','=','99')])
                    record.document_type_id = document
                elif record.type == 'out_refund':
                    document = record.env['document.type'].search([('code','=','03')])
                    record.document_type_id = document
                else:
                    if record.partner_id.document_type_id:
                        record.document_type_id = record.partner_id.document_type_id.id

    @api.depends('document_type_id')
    def _compute_document_code(self):
        self.document_code = self.document_type_id.code
        
    @api.depends('invoice_line_ids')
    def _compute_total_taxed_and_untaxed_service(self):
        for record in self:
            total_taxed_service = 0
            total_without_taxed_service = 0
            lines = filter(lambda line: line.product_id.is_other_charge == False, record.invoice_line_ids)
            for line in lines:
                if line.product_id.type == 'service':
                    for tax in line.invoice_line_tax_ids:
                        if tax.has_exoneration:
                            total_taxed_service = total_taxed_service + (1-tax.exoneration_percentage/tax.amount) * line.total_amount
                        else:
                            total_taxed_service = total_taxed_service + line.total_amount
                    if  not line.invoice_line_tax_ids:
                        total_without_taxed_service = total_without_taxed_service + line.total_amount

            record.total_taxed_service = total_taxed_service
            record.total_without_taxed_service = total_without_taxed_service

    @api.depends('invoice_line_ids')
    def _compute_total_taxed_and_untaxed_goods(self):
        for record in self:
            total_taxed_goods = 0
            total_without_taxed_goods = 0
            lines = filter(lambda line: line.product_id.is_other_charge == False, record.invoice_line_ids)
            for line in lines:
                if line.product_id.type != 'service':
                    for tax in line.invoice_line_tax_ids:
                        if tax.has_exoneration:
                            total_taxed_goods = total_taxed_goods + (1-tax.exoneration_percentage/tax.amount) * line.total_amount
                        else:
                            total_taxed_goods = total_taxed_goods + line.total_amount

                    if  not line.invoice_line_tax_ids:
                        total_without_taxed_goods = total_without_taxed_goods + line.total_amount

            record.total_taxed_goods = total_taxed_goods
            record.total_without_taxed_goods = total_without_taxed_goods

    @api.depends('total_taxed_service','total_taxed_goods','total_without_taxed_service','total_without_taxed_goods')
    def _compute_total_sale(self):
        for record in self:
            total_taxed = record.total_taxed_service + record.total_taxed_goods
            total_without_taxed = record.total_without_taxed_service + record.total_without_taxed_goods
            total_exonerate = record.total_exonerate_goods + record.total_exonerate_service
            record.total_sale = total_taxed + total_without_taxed + total_exonerate

    @api.depends('invoice_line_ids')
    def _compute_total_discount(self):
        for record in self:
            total_discount = 0
            lines = filter(lambda line: line.product_id.is_other_charge == False, record.invoice_line_ids)
            for line in lines:
                total_discount = total_discount + line.discount_amount
            record.total_discount = total_discount

    @api.depends('invoice_line_ids')
    def _compute_total_taxes_without_exoneration(self):
        for record in self:
            total_taxes = 0
            lines = filter(lambda line: line.product_id.is_other_charge == False, record.invoice_line_ids)
            for line in lines:
                 total_taxes = total_taxes + line.total_tax_amount
            record.total_taxes_without_exoneration = total_taxes
            
    def action_invoice_open(self):
        if self.state == 'draft':
            self.invoice_validation()
            self.partner_validation()
            self.tax_validation()
            self.uom_validation()
            self.product_validation()
            self.services_validation()
            self.other_chargers_validation()
            date = datetime.now(tz=pytz.timezone('America/Costa_Rica')).strftime("%Y-%m-%dT%H:%M:%S")
            invoice_state = 'queue'
            if self.document_type_id.code == '99':
                invoice_state = 'internal'
            self.update({
                'date_issued': date,
                'invoice_state':invoice_state,
            })
        super(accountMove, self).action_invoice_open()

    def partner_validation(self):
        if self.document_type_id.code != "04":
            if not self.partner_id.email:
                raise ValidationError("Configure el campo 'correo electrónico' del cliente")
            if not self.partner_id.identification_type_id:
                  raise ValidationError("Configure el campo 'Tipo identificación' del cliente")
            if not self.partner_id.vat:
                raise ValidationError("Configure el campo 'identificación' del cliente")

        if self.document_type_id.code == "08":
            msg = ''
            if not self.partner_id.state_id:
                msg += 'La "Provincia" del proveedor es requerida \n'
            if not self.partner_id.canton_id:
                msg += 'El "Cantón" del proveedor es requerida \n'
            if not self.partner_id.district_id:
                 msg += 'El "Distrito" del proveedor es requerida \n'
            if not self.partner_id.street:
                 msg += 'Las "Otras señas" del proveedor son requeridas \n'
            if msg:
                 raise ValidationError(msg)

        if self.partner_id.phone:
                if not re.search('^[0-9]*$',self.partner_id.phone):
                    raise ValidationError('El teléfono del cliente solo debe contener numeros')

        if self.partner_id.fax_number:
                if not re.search('^[0-9]*$',self.partner_id.fax_number):
                    raise ValidationError('El fax del cliente solo debe contener numeros')

            
    def invoice_validation(self):
        if self.document_type_id.code == "02" or self.document_type_id.code == "03":
            if not self.related_document.consecutive:
                raise ValidationError("El documento de referencia al cual le está aplicando la nota aún no se le ha asignado un consecutivo de comprobante electrónico, por favor inténtelo de nuevo más tarde.")

        if self.payment_term_id:
            if not self.payment_term_id.sale_condition_id:
                raise ValidationError("Configure el campo 'Condición de venta' es requerido para el plazo de pago '{}'".format(self.payment_term_id.name))


    def tax_validation(self):
        for record in self.invoice_line_ids:
            for tax in record.invoice_line_tax_ids:
                if not tax.tax_code_id:
                   raise ValidationError("Configure el campo 'Código Impuesto' es requerido para el impuesto '{}'".format(tax.name))
                if not tax.tax_rate_id:
                   raise ValidationError("Configure el campo 'Tarifa Impuesto' es requerido para el impuesto '{}'".format(tax.name))

    def uom_validation(self):
        for record in self.invoice_line_ids:
            if record.uom_id:
                if not record.uom_id.code:
                    raise ValidationError("Configure el campo 'Código' es requerido para la unidad de medida '{}'".format(record.uom_id.name))

    def product_validation(self):
        for record in self.invoice_line_ids:
            if record.product_id and not record.product_id.is_other_charge:
                if not record.product_id.cabys_code_id :
                    raise ValidationError("Configure el campo 'Código cabys' es requerido para el producto '{}'".format(record.product_id.name))

    def services_validation(self):
        for record in self.invoice_line_ids:
            if record.product_id.type == "service":
                if record.uom_id.code not in ['Sp','Os','Spe','St']:
                    raise ValidationError("El servicio llamado '{}' tiene una unidad de medida que no corresponde para un servicio.".format(record.product_id.name))

    def other_chargers_validation(self):
        for record in self.invoice_line_ids:
            if record.product_id.other_charge_doc_type == '04':
                if not record.third_party_id:
                     raise ValidationError("Porfavor agregue un tercero para las lineas 'Otros Cargos: Cobro de un tercero'")

    @api.returns('self')
    def refund(self, date_invoice=None, date=None, description=None, journal_id=None,reference_document_id=None,reference_code_id=None,related_document=None,payment_method_id=None,payment_term_id=None):
        new_invoices = self.browse()
        for invoice in self:
            # create the new invoice
            values = self._prepare_refund(invoice, date_invoice=date_invoice, date=date,
                                    description=description, journal_id=journal_id)
            doc_id = False
            doc_type = self.env["document.type"].search([("code","=","03")])
            if doc_type:
                doc_id = doc_type.id

            values.update({
                'reference_document_id':reference_document_id,
                'reference_code_id':reference_code_id,
                'related_document':related_document,
                'payment_method_id':payment_method_id,
                'payment_term_id':payment_term_id,
                'document_type_id':doc_id,
            })
            
            refund_invoice = self.create(values)
            if invoice.type == 'out_invoice':
                message = ("This customer invoice credit note has been created from: <a href=# data-oe-model=account.invoice data-oe-id=%d>%s</a><br>Reason: %s") % (invoice.id, invoice.number, description)
            else:
                message = ("This vendor bill credit note has been created from: <a href=# data-oe-model=account.invoice data-oe-id=%d>%s</a><br>Reason: %s") % (invoice.id, invoice.number, description)

            refund_invoice.message_post(body=message)
            new_invoices += refund_invoice
        return new_invoices

    def add_debit_note(self):
        return {
                'type': 'ir.actions.act_window',
                'name': 'Nota Débito',
                'res_model': 'account.debit.note',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'target': 'new',
                'context': {
                    'id':self.id,
                    'doc_ref':self.name,
                 }
             }  

    def resend_document(self):
        if self.invoice_state == 'invalid' or self.invoice_state == 'error' or self.invoice_state == 'unauthorized':
            inv_json = self.env['util.web.services'].convert_account_invoice_to_json(self)
            self.env['util.web.services'].send_invoice_to_web_services(self,inv_json,"account.invoice")

    
  
