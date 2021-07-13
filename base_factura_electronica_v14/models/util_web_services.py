# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from lxml import etree
from zeep import Client,helpers
from datetime import datetime,timezone
import pytz
import logging
log = logging.getLogger(__name__)

class utilWebServices(models.Model):
    _name = 'util.web.services'
    _description = 'This class contains all the logic to sends information to web services'
    _auto = False

    def create_xml_gt(self,inv,model):

         root = etree.Element('GTComprobanteElectronico')
         if model == "pos.order" and inv['document_type_id'].code != '03' and inv['document_type_id'].code != '02':
            root = etree.Element('GTComprobanteElectronicoM')
       
         if inv['numeric_key']:
             numeric_key_node = etree.SubElement(root,'Clave')
             numeric_key_node.text = inv['numeric_key']

         activity_code_node = etree.SubElement(root,'CodigoActividad')
         activity_code_node.text = inv['activity_code_id'].code or ''

      
         if inv['consecutive']:
             numeric_key_node = etree.SubElement(root,'NumeroConsecutivo')
             numeric_key_node.text = inv['consecutive']

         document_type_node = etree.SubElement(root,'TipoComprobante')
         document_type_node.text = inv['document_type_id'].code or ''

         document_situation_node = etree.SubElement(root,'SituacionComprobante')
         document_situation_node.text = inv['situation']

         date_node = etree.SubElement(root,'FechaEmision')
         date_node.text = inv['date_issued'] or ''

         office_branch_node = etree.SubElement(root,'Sucursal')
         office_branch_node.text = inv['branch_office'] or ''
         terminal_node = etree.SubElement(root,'Terminal')
         terminal_node.text = inv['terminal'] or ''

         #Receptor
         if inv['partner_id']:
            receiver_node = etree.SubElement(root,'Receptor')
            receiver_name_node = etree.SubElement(receiver_node,'Nombre')
            receiver_name_node.text = inv['partner_id'].name or ''

            if inv['partner_id'].identification_type_id.code != '99':
                receiver_identification_node = etree.SubElement(receiver_node,'Identificacion')
                receiver_identification_type_node = etree.SubElement(receiver_identification_node,'Tipo')
                receiver_identification_type_node.text = inv['partner_id'].identification_type_id.code or ''
                receiver_identification_number_node = etree.SubElement(receiver_identification_node,'Numero')
                receiver_identification_number_node.text = inv['partner_id'].vat or ''
            else:
                receiver_foreign_identification_node = etree.SubElement(receiver_node,'IdentificacionExtranjero')
                receiver_foreign_identification_node.text = inv['partner_id'].vat
                
            #ubicacion
            if inv['partner_id'].country_id.code == 'CR' and inv['partner_id'].state_id and inv['partner_id'].canton_id:
                receiver_location_node = etree.SubElement(receiver_node,'Ubicacion')
                receiver_location_state_node = etree.SubElement(receiver_location_node,'Provincia')
                receiver_location_state_node.text = inv['partner_id'].state_id.code or ''
                
                receiver_location_canton_node = etree.SubElement(receiver_location_node,'Canton')
                receiver_location_canton_node.text = inv['partner_id'].canton_id.code or ''

                receiver_location_district_node = etree.SubElement(receiver_location_node,'Distrito')
                receiver_location_district_node.text = inv['partner_id'].district_id.code or ''
                if inv['partner_id'].neighborhood_id:
                    receiver_location_neighborhood_node = etree.SubElement(receiver_location_node,'Barrio')
                    receiver_location_neighborhood_node.text = inv['partner_id'].neighborhood_id.code or ''

                receiver_location_other_signs_node = etree.SubElement(receiver_location_node,'OtrasSenas')
                receiver_location_other_signs_node.text = '{} {}'.format(inv['partner_id'].street,inv['partner_id'].street2 or '')

            #if self.partner_id.identification_type_id.code == '99':
                #receiver_location_other_foreign_signs_node = etree.SubElement(receiver_node,'OtrasSenasExtranjero')
                #receiver_location_other_foreign_signs_node.text = self.partner_id.contact_address or ''
            
            #telefono
            if inv['partner_id'].phone:
                receiver_phone_node = etree.SubElement(receiver_node,'Telefono')
                receiver_phone_country_code_node = etree.SubElement(receiver_phone_node,'CodigoPais')
                receiver_phone_country_code_node.text = str(inv['partner_id'].country_id.phone_code) or ''
                receiver_phone_number_node = etree.SubElement(receiver_phone_node,'NumTelefono')
                receiver_phone_number_node.text = inv['partner_id'].phone or ''

            #fax
            if inv['partner_id'].fax_number:
                receiver_fax_node = etree.SubElement(receiver_node,'Fax')
                receiver_fax_country_code_node = etree.SubElement(receiver_fax_node,'CodigoPais')

                if inv['partner_id'].country_id.phone_code != 0:
                    receiver_fax_country_code_node.text = str(inv['partner_id'].country_id.phone_code) or ''
                else:
                    receiver_fax_country_code_node.text = '506'

                receiver_fax_number_node = etree.SubElement(receiver_fax_node,'NumTelefono')
                receiver_fax_number_node.text = inv['partner_id'].fax_number or ''
            
            #email
            if inv['partner_id'].email:
                receiver_email_node = etree.SubElement(receiver_node,'CorreoElectronico')
                receiver_email_node.text = inv['partner_id'].email or ''
         else:
            #when not exist a partner,the web service waits of a name and email at least 
            receiver_node = etree.SubElement(root,'Receptor')
            receiver_name_node = etree.SubElement(receiver_node,'Nombre')
            receiver_name_node.text = 'Cliente Contado'
            receiver_email_node = etree.SubElement(receiver_node,'CorreoElectronico')
            receiver_email_node.text = 'info@contado.com'

         condition_sale_node = etree.SubElement(root,'CondicionVenta')
         condition_sale_node.text = inv['payment_term_id'].sale_condition_id.code or ''
         if inv['payment_term_id'].sale_condition_id.code == '02':
            credit_term_node = etree.SubElement(root,'PlazoCredito')
            credit_term_node.text = '{}'.format(inv['payment_term_id'].payment_term_description)
         payment_method_node = etree.SubElement(root,'MedioPago')
         payment_method_node.text = inv['payment_method_id'].code or ''
         
         #lineas
         service_detail_node = etree.SubElement(root,'DetalleServicio')
         for number, line in enumerate(inv['lines'], start=1 ):

             line_node = etree.SubElement(service_detail_node,'LineaDetalle')
             line_number = etree.SubElement(line_node,'NumeroLinea')
             line_number.text = str(number)
             
             if line['product_id']:
                 line_cabys_code = etree.SubElement(line_node,'Codigo')
                 line_cabys_code.text = line['product_id'].cabys_code_id.code or ''
                 if line['product_id'].product_code_type_id:
                    line_comercial_code = etree.SubElement(line_node,'CodigoComercial')
                    line_type = etree.SubElement(line_comercial_code,'Tipo')
                    line_type.text = line['product_id'].product_code_type_id.code
                    line_code = etree.SubElement(line_comercial_code,'Codigo')
                    line_code.text = line['product_id'].default_code

             line_quantity = etree.SubElement(line_node,'Cantidad')
             line_quantity.text = '{:.2f}'.format(line['quantity']) or ''

             line_uom = etree.SubElement(line_node,'UnidadMedida')
             line_uom.text = line['uom_id'].code or ''

             line_detail = etree.SubElement(line_node,'Detalle')
             line_detail.text = line['detail'] or ''

             line_unit_price = etree.SubElement(line_node,'PrecioUnitario')
             line_unit_price.text = '{:.2f}'.format(line['price_unit']) or ''

             line_total_amount = etree.SubElement(line_node,'MontoTotal')
             line_total_amount.text = '{:.2f}'.format(line['total_amount']) or ''

             if line['discount_amount']:
                line_discount = etree.SubElement(line_node,'Descuento')
                line_amount_discount = etree.SubElement(line_discount,'MontoDescuento')
                line_amount_discount.text = '{:.2f}'.format(line['discount_amount']) or ''
                line_reason_discount = etree.SubElement(line_discount,'NaturalezaDescuento')
                line_reason_discount.text = line['discount_note'] or ''

             line_SubTotal = etree.SubElement(line_node,'SubTotal')
             line_SubTotal.text = '{:.2f}'.format(line['price_subtotal']) or ''
    
             for tax in line['tax_ids']:
                line_tax = etree.SubElement(line_node,'Impuesto')
                line_tax_code = etree.SubElement(line_tax,'Codigo')
                line_tax_code.text = tax.tax_code_id.code or ''
                line_tax_rate_code = etree.SubElement(line_tax,'CodigoTarifa')
                line_tax_rate_code.text = tax.tax_rate_id.code or ''
                line_tax_rate = etree.SubElement(line_tax,'Tarifa')
                line_tax_rate.text = '{:.2f}'.format(tax.amount) or ''
                line_tax_amount = etree.SubElement(line_tax,'Monto')
                line_tax_amount.text = '{:.2f}'.format( line['total_tax_amount'] )
                if inv['partner_id'].has_exoneration and tax.has_exoneration:
                    line_exoneration = etree.SubElement(line_tax,'Exoneracion')
                    line_exoneration_doc_type = etree.SubElement(line_exoneration,'TipoDocumento')
                    line_exoneration_doc_type.text = inv['partner_id'].exoneration_document_id.code or ''
                    line_exoneration_doc_number = etree.SubElement(line_exoneration,'NumeroDocumento')
                    line_exoneration_doc_number.text = inv['partner_id'].document_number or ''
                    line_exoneration_institute_name = etree.SubElement(line_exoneration,'NombreInstitucion')
                    line_exoneration_institute_name.text = inv['partner_id'].institute_name or ''
                    line_exoneration_issued_date = etree.SubElement(line_exoneration,'FechaEmision')
                    line_exoneration_issued_date.text = inv['partner_id'].issued_date.astimezone(tz=pytz.timezone('America/Costa_Rica')).strftime("%Y-%m-%dT%H:%M:%S") or ''
                    line_exoneration_percentage = etree.SubElement(line_exoneration,'PorcentajeExoneracion')
                    line_exoneration_percentage.text = str(tax.exoneration_percentage) or ''
                    line_exoneration_amount = etree.SubElement(line_exoneration,'MontoExoneracion')
                    line_exoneration_amount.text =  '{:.2f}'.format(line['exonerate_amount'] )
                    line_tax_net = etree.SubElement(line_node,'ImpuestoNeto')
                    tax_net = line['total_tax_amount'] - line['exonerate_amount']
                    line_tax_net.text = '{:.2f}'.format(tax_net)

             if not line['total_exonerate_amount']:
                line_total = etree.SubElement(line_node,'MontoTotalLinea')
                line_total.text = '{:.2f}'.format( line['price_subtotal'] + line['total_tax_amount'] )
             else:
                line_total = etree.SubElement(line_node,'MontoTotalLinea')
                line_total.text = '{:.2f}'.format( line['price_subtotal'] + tax_net )

         #otrosCargos
         for other in inv['other_chargers']:
            other_charges_node = etree.SubElement(root,'OtrosCargos')
            other_charges_doc_type = etree.SubElement(other_charges_node,'TipoDocumento')

            if other['product_id'].other_charge_doc_type == '04':
                other_charges_third_party_identification = etree.SubElement(other_charges_node,'NumeroIdentidadTercero')
                other_charges_third_party_identification.text = other['third_party_id'].identification
                other_charges_third_party_name = etree.SubElement(other_charges_node,'NombreTercero')
                other_charges_third_party_name.text = other['third_party_id'].name

            other_charges_doc_type.text = other['product_id'].other_charge_doc_type
            other_charges_detail = etree.SubElement(other_charges_node,'Detalle')
            other_charges_detail.text = other['detail']
            other_charges_amount = etree.SubElement(other_charges_node,'MontoCargo')
            other_charges_amount.text ='{:.2f}'.format(other['price_subtotal'])

         #ResumenFactura
         summary_bill_node = etree.SubElement(root,'ResumenFactura')
         currency_type_code_node = etree.SubElement(summary_bill_node,'CodigoTipoMoneda')
         currency_code_node = etree.SubElement(currency_type_code_node,'CodigoMoneda')
         currency_code_node.text = inv['currency_id'].name or ''
         currency_rate_node = etree.SubElement(currency_type_code_node,'TipoCambio')
         if inv['currency_id'].name == 'CRC':
            currency_rate_node.text = '1'
         else:
             currency_rate_node.text = '{:.2f}'.format( 1 / inv['currency_id'].rate )

         total_taxed_services_node = etree.SubElement(summary_bill_node,'TotalServGravados')
         total_taxed_services_node.text = '{:.2f}'.format(inv['total_taxed_service'])

         total_without_taxed_services_node = etree.SubElement(summary_bill_node,'TotalServExentos')
         total_without_taxed_services_node.text = '{:.2f}'.format(inv['total_without_taxed_service'])
         if inv['document_type_id'].code != "09":
            total_exonerated_services_node = etree.SubElement(summary_bill_node,'TotalServExonerado')
            total_exonerated_services_node.text = '{:.2f}'.format(inv['total_exonerate_service'])

         total_taxed_goods_node = etree.SubElement(summary_bill_node,'TotalMercanciasGravadas')
         total_taxed_goods_node.text = '{:.2f}'.format(inv['total_taxed_goods'])

         total_without_taxed_goods_node = etree.SubElement(summary_bill_node,'TotalMercanciasExentas')
         total_without_taxed_goods_node.text = '{:.2f}'.format(inv['total_without_taxed_goods'])
         if inv['document_type_id'].code != "09":
            total_exonerated_goods_node = etree.SubElement(summary_bill_node,'TotalMercExonerada')
            total_exonerated_goods_node.text = '{:.2f}'.format(inv['total_exonerate_goods'])

         total_taxed_node = etree.SubElement(summary_bill_node,'TotalGravado')
         total_taxed_node.text = '{:.2f}'.format(inv['total_taxed_goods'] + inv['total_taxed_service'])

         total_without_taxed_node = etree.SubElement(summary_bill_node,'TotalExento')
         total_without_taxed_node.text = '{:.2f}'.format(inv['total_without_taxed_goods'] + inv['total_without_taxed_service'])
         if inv['document_type_id'].code != "09":
            total_exonerated_node = etree.SubElement(summary_bill_node,'TotalExonerado')
            total_exonerated_node.text = '{:.2f}'.format(inv['total_exonerate'])

         total_sale_node = etree.SubElement(summary_bill_node,'TotalVenta')
         total_sale_node.text = '{:.2f}'.format(inv['total_sale'])

         total_discount_node = etree.SubElement(summary_bill_node,'TotalDescuentos')
         total_discount_node.text = '{:.2f}'.format(inv['total_discount'])

         total_net_sale_node = etree.SubElement(summary_bill_node,'TotalVentaNeta')
         total_net_sale_node.text = '{:.2f}'.format(inv['total_sale'] - inv['total_discount'])

         total_taxes_node = etree.SubElement(summary_bill_node,'TotalImpuesto')
         total_taxes_node.text = '{:.2f}'.format(inv['total_taxed'])

         #total_iva_refunded_node = etree.SubElement(summary_bill_node,'TotalIVADevuelto')
         #total_iva_refunded_node.text = ''

         total_other_charges_node = etree.SubElement(summary_bill_node,'TotalOtrosCargos')
         total_other_charges_node.text = '{:.2f}'.format(inv['total_other_charges'])

         total_bill_node = etree.SubElement(summary_bill_node,'TotalComprobante')
         total_bill_node.text =  '{:.2f}'.format( (inv['total_sale'] - inv['total_discount']) +  inv['total_taxed'] + inv['total_other_charges'] )

         #informacionReferencia
         if inv['document_type_id'].code == '02' or inv['document_type_id'].code == '03':
            referenceInformation_node = etree.SubElement(root,'InformacionReferencia')
            doc_type = etree.SubElement(referenceInformation_node,'TipoDoc')
            doc_type.text = inv['reference_document_id'].code or ''

            doc_type = etree.SubElement(referenceInformation_node,'Numero')
            doc_type.text = inv['related_document'].consecutive or ''

            doc_date_node = etree.SubElement(referenceInformation_node,'FechaEmision')
            doc_date_node.text = inv['related_document'].date_issued or ''

            doc_code_node = etree.SubElement(referenceInformation_node,'Codigo')
            doc_code_node.text = inv['reference_code_id'].code or ''

            doc_reason_node = etree.SubElement(referenceInformation_node,'Razon')
            doc_reason_node.text = inv['name'] or ''
         #Otros
         others_node = etree.SubElement(root,'Otros')
         other_text_node = etree.SubElement(others_node,'OtroTexto')
         other_text_node.text = inv['comment'] or ''

         #other_content_node = etree.SubElement(others_node,'OtroContenido')
         #other_content_node.text = ''

         pretty_xml = etree.tostring(root, encoding="unicode", pretty_print=True)
         log.info("================XMl======================= {}".format(pretty_xml))
         return pretty_xml

    def send_invoice_to_web_services(self,inv_id,inv_json,model):
            try:

                inv_id.update({
                    'invoice_state':'in_progress',
                })

                client = Client(wsdl=inv_id.company_id.api_url)
                xml = self.create_xml_gt(inv_json,model)
                response = None
                if model == "account.invoice" or inv_id.document_type_id.code == '03' or inv_id.document_type_id.code == '02':
                    response = client.service.enviarComprobante(inv_id.company_id.user,inv_id.company_id.password,xml)
                elif model == "pos.order":
                    response = client.service.enviarComprobanteM(inv_id.company_id.user,inv_id.company_id.password,xml)

                json_response = helpers.serialize_object(response)
                if json_response:

                    invoice_state = 'response_unhandled'
                    if  json_response['EstadoHacienda'] == 0:
                        invoice_state = 'processing'
                        
                    elif json_response['EstadoHacienda'] == 1:
                        invoice_state = 'accepted'
                        
                    elif json_response['EstadoHacienda'] == 3:
                        invoice_state = 'rejected'
                        

                    if json_response['codigo'] == 200 or json_response['codigo'] == 201:
                        inv_id.update({
                            'numeric_key':json_response['ClaveNumerica'],
                            'consecutive':json_response['NumeracionConsecutiva'],
                            'pdf_invoice_fname':'{0}.pdf'.format(json_response['NumeracionConsecutiva']),
                            'pdf_invoice':json_response['PDFbase64'],
                            'xml_invoice_fname':'{0}-firmado.xml'.format(json_response['NumeracionConsecutiva']),
                            'xml_invoice':json_response['XML'],
                            'xml_mh_fname':'{0}-hacienda.xml'.format(json_response['NumeracionConsecutiva']),
                            'xml_mh':json_response['XMLMensajeHacienda'],
                            'invoice_state':invoice_state,
                        })

                    elif json_response['codigo'] == 505:
                        inv_id.update({
                            'numeric_key':json_response['ClaveNumerica'],
                            'consecutive':json_response['NumeracionConsecutiva'],
                            'pdf_invoice_fname':'{0}.pdf'.format(json_response['NumeracionConsecutiva']),
                            'pdf_invoice':json_response['PDFbase64'],
                            'xml_invoice_fname':'{0}-firmado.xml'.format(json_response['NumeracionConsecutiva']),
                            'xml_invoice':json_response['XML'],
                            'xml_mh_fname':'{0}-hacienda.xml'.format(json_response['NumeracionConsecutiva']),
                            'xml_mh':json_response['XMLMensajeHacienda'],
                            'invoice_state':invoice_state,
                        })
                        message = json_response['descripcion']
                        self.log_chatter(inv_id.id,message,model)
                    elif json_response['codigo'] == 402 or json_response['codigo'] == 403:
                        inv_id.update({
                            'numeric_key':json_response['ClaveNumerica'],
                            'consecutive':json_response['NumeracionConsecutiva'],
                            'invoice_state':'invalid',
                        })
                        message = json_response['descripcion']
                        self.log_chatter(inv_id.id,message,model)
                    elif json_response['codigo'] == 506:
                        inv_id.update({
                            'numeric_key':json_response['ClaveNumerica'],
                            'consecutive':json_response['NumeracionConsecutiva'],
                            'pdf_invoice_fname':'{0}.pdf'.format(json_response['NumeracionConsecutiva']),
                            'pdf_invoice':json_response['PDFbase64'],
                            'xml_invoice_fname':'{0}-firmado.xml'.format(json_response['NumeracionConsecutiva']),
                            'xml_invoice':json_response['XML'],
                            'xml_mh_fname':'{0}-hacienda.xml'.format(json_response['NumeracionConsecutiva']),
                            'xml_mh':json_response['XMLMensajeHacienda'],
                            'invoice_state':invoice_state,
                        })
                        message = json_response['descripcion']
                        self.log_chatter(inv_id.id,message,model)
                        
                    elif json_response['codigo'] == 401:
                        inv_id.update({
                            'invoice_state':'unauthorized',
                        })
                        message = json_response['descripcion']
                        self.log_chatter(inv_id.id,message,model)

                    else:
                        inv_id.update({
                            'invoice_state':'response_unhandled',
                        })
                        message = json_response['descripcion']
                        self.log_chatter(inv_id.id,message,model)
                        
            except Exception as ex:
                inv_id.update({
                    'invoice_state':'error',
                })
                self.log_chatter(inv_id.id,str(ex),model)

    def convert_account_invoice_to_json(self,record):
        inv = {}
        inv['numeric_key'] = False
        inv['activity_code_id'] = record.activity_code_id
        inv['consecutive'] = False
        inv['document_type_id'] = record.document_type_id
        inv['situation'] = record.situation
        inv['date_issued'] = record.date_issued
        inv['branch_office'] = record.company_id.branch_office
        inv['terminal'] = record.company_id.terminal
        inv['partner_id'] = record.partner_id
        inv['payment_term_id'] = record.payment_term_id
        inv['payment_method_id'] = record.payment_method_id
        inv['currency_id'] = record.currency_id
        inv['total_taxed_service'] = record.total_taxed_service
        inv['total_exonerate_service'] = record.total_exonerate_service
        inv['total_taxed_goods'] = record.total_taxed_goods
        inv['total_without_taxed_goods'] = record.total_without_taxed_goods
        inv['total_without_taxed_service'] = record.total_without_taxed_service
        inv['total_exonerate_goods'] = record.total_exonerate_goods
        inv['total_exonerate'] = record.total_exonerate
        inv['total_sale'] = record.total_sale
        inv['total_discount'] = record.total_discount
        inv['total_taxed'] = record.total_taxed
        inv['total_other_charges'] = record.total_other_charges
        inv['reference_document_id'] = record.reference_document_id
        inv['related_document'] = record.related_document
        inv['reference_code_id'] = record.reference_code_id
        inv['name'] = record.name
        inv['comment'] = record.comment
        lines = []
        filter_lines = filter(lambda line: line.product_id.is_other_charge == False, record.invoice_line_ids)
        for line in filter_lines:
            new_line = {}
            new_line['product_id'] = line.product_id
            new_line['quantity'] = line.quantity
            new_line['uom_id'] = line.uom_id
            new_line['detail'] = line.name
            new_line['price_unit'] = line.price_unit
            new_line['total_amount'] = line.total_amount
            new_line['discount_amount'] = line.discount_amount
            new_line['discount_note'] = line.discount_note
            new_line['price_subtotal'] = line.price_subtotal
            new_line['tax_ids'] = line.invoice_line_tax_ids
            new_line['total_exonerate_amount'] = line.total_exonerate_amount
            new_line['total_tax_amount'] = line.total_tax_amount
            new_line['total_amount'] = line.total_amount
            new_line['exonerate_amount'] = line.exonerate_amount
            lines.append(new_line)
        inv['lines'] = lines

        other_chargers = []
        filter_other_chargers = filter(lambda line: line.product_id.is_other_charge == True, record.invoice_line_ids)
        for other in filter_other_chargers:
            new_other_charger = {}
            new_other_charger['product_id'] = other.product_id
            new_other_charger['detail'] = other.name
            new_other_charger['price_subtotal'] = other.price_subtotal
            new_other_charger['third_party_id'] = other.third_party_id
            other_chargers.append(new_other_charger)
        inv['other_chargers'] = other_chargers

        return inv

    def convert_pos_order_to_json(self,record):
        inv = {}
        inv['numeric_key'] = record.numeric_key
        inv['activity_code_id'] = record.config_id.activity_code_id
        inv['consecutive'] = record.consecutive
        inv['document_type_id'] = record.document_type_id
        inv['situation'] = record.situation
        inv['date_issued'] = record.date_issued or ''
        inv['branch_office'] = str(record.config_id.sequence_id.branch_office)
        inv['terminal'] =  str(record.config_id.sequence_id.terminal)
        inv['partner_id'] = record.partner_id
        inv['payment_term_id'] = self.env['account.payment.term'].search([('name','=','Immediate Payment')])
        inv['payment_method_id'] = record.payment_method_id
        inv['currency_id'] = record.pricelist_id.currency_id
        inv['total_taxed_service'] = record.total_taxed_service
        inv['total_exonerate_service'] = record.total_exonerate_service
        inv['total_taxed_goods'] = record.total_taxed_goods
        inv['total_without_taxed_goods'] = record.total_without_taxed_goods
        inv['total_without_taxed_service'] = record.total_without_taxed_service
        inv['total_exonerate_goods'] = record.total_exonerate_goods
        inv['total_exonerate'] = record.total_exonerate
        inv['total_sale'] = record.total_sale
        inv['total_discount'] = record.total_discount
        inv['total_taxed'] = record.total_taxed
        inv['total_other_charges'] = record.total_other_charges
        inv['reference_document_id'] = record.reference_document_id
        inv['related_document'] = record.related_document
        inv['reference_code_id'] = record.reference_code_id
        inv['name'] = record.reason
        inv['comment'] = record.note
        lines = []
        filter_lines = filter(lambda line: line.product_id.is_other_charge == False, record.lines)
        for line in filter_lines:
            new_line = {}
            new_line['product_id'] = line.product_id
            new_line['quantity'] = abs(line.qty)
            new_line['uom_id'] = line.product_id.uom_id
            new_line['detail'] = line.product_id.name
            new_line['price_unit'] = line.price_unit
            new_line['total_amount'] = line.total_amount
            new_line['discount_amount'] = line.discount_amount
            new_line['discount_note'] = '{}"%" descuento'.format(line.discount or '0')
            new_line['price_subtotal'] = abs(line.price_subtotal)
            new_line['tax_ids'] = line.tax_ids_after_fiscal_position
            new_line['total_exonerate_amount'] = line.total_exonerate_amount
            new_line['total_tax_amount'] = line.total_tax_amount
            new_line['total_amount'] = line.total_amount
            new_line['exonerate_amount'] = line.exonerate_amount
            lines.append(new_line)
        inv['lines'] = lines

        other_chargers = []
        filter_other_chargers = filter(lambda line: line.product_id.is_other_charge == True, record.lines)
        for other in filter_other_chargers:
            new_other_charger = {}
            new_other_charger['product_id'] = other.product_id
            new_other_charger['detail'] = other.product_id.name
            new_other_charger['price_subtotal'] = abs(other.price_subtotal)
            new_other_charger['third_party_id'] = other.third_party_id
            other_chargers.append(new_other_charger)
        inv['other_chargers'] = other_chargers

        return inv

    def cron_send_invoice(self):
        invoices = self.env["account.invoice"].search([("invoice_state","=","queue")])
        for inv in invoices:
            inv_json = self.convert_account_invoice_to_json(inv)
            self.send_invoice_to_web_services(inv,inv_json,"account.invoice")

        pos = self.env['ir.module.module'].search([('name','=','FacturaElectronicaPosV12')])
        if pos.state == 'installed':
            orders = self.env['pos.order'].search([("invoice_state","=","queue")])
            for order in orders:
                order_json = self.convert_pos_order_to_json(order)
                self.send_invoice_to_web_services(order,order_json,"pos.order")
            
    def log_chatter(self,id,message,model):
        chatter = self.env['mail.message']
        chatter.create({
                        'res_id': id,
                        'model':model,
                        'body': message,
                       })

    def cron_query_invoice(self):
        invoices = self.env["account.invoice"].search([("invoice_state","=","processing")])
        for inv in invoices:
            self.query_invoice_from_web_services(inv,"account.invoice")

        pos = self.env['ir.module.module'].search([('name','=','FacturaElectronicaPosV12')])
        if pos.state == 'installed':
            orders = self.env['pos.order'].search([("invoice_state","=","processing")])
            for order in orders:
                self.query_invoice_from_web_services(order,"pos.order")

    def query_invoice_from_web_services(self,inv_id,model):
            try:
                client = Client(wsdl=inv_id.company_id.api_url)
                response = client.service.consultarComprobante(inv_id.company_id.user,inv_id.company_id.password,inv_id.numeric_key)
                json_response = helpers.serialize_object(response)
                if json_response:

                    invoice_state = 'response_unhandled'
                    if  json_response['EstadoHacienda'] == 0:
                        invoice_state = 'processing'
                        
                    elif json_response['EstadoHacienda'] == 1:
                        invoice_state = 'accepted'
                        
                    elif json_response['EstadoHacienda'] == 3:
                        invoice_state = 'rejected'

                    if json_response['codigo'] == 200 or json_response['codigo'] == 201:
                        inv_id.update({
                            'xml_mh_fname':'{0}-hacienda.xml'.format(json_response['NumeracionConsecutiva']),
                            'xml_mh':json_response['XMLMensajeHacienda'],
                            'invoice_state':invoice_state,
                        })

                    elif json_response['codigo'] == 505:
                        inv_id.update({
                            'xml_mh_fname':'{0}-hacienda.xml'.format(json_response['NumeracionConsecutiva']),
                            'xml_mh':json_response['XMLMensajeHacienda'],
                            'invoice_state': invoice_state,
                        })
                        message = json_response['descripcion']
                        self.log_chatter(inv_id.id,message,model)
                    elif json_response['codigo'] == 402 or json_response['codigo'] == 403:
                        inv_id.update({
                            'invoice_state':'invalid',
                        })
                        message = json_response['descripcion']
                        self.log_chatter(inv_id.id,message,model)
                    elif json_response['codigo'] == 506:
                        inv_id.update({
                            'xml_mh_fname':'{0}-hacienda.xml'.format(json_response['NumeracionConsecutiva']),
                            'xml_mh':json_response['XMLMensajeHacienda'],
                            'invoice_state':invoice_state,
                        })
                        message = json_response['descripcion']
                        self.log_chatter(inv_id.id,message,model)
                    else:
                        message = json_response['descripcion']
                        self.log_chatter(inv_id.id,message,model)

                        
            except Exception as ex:
                inv_id.update({
                    'invoice_state':'error',
                })
                self.log_chatter(inv_id.id,str(ex),model)

    