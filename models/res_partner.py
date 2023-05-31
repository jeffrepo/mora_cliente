# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
from datetime import datetime, date, timedelta
import pytz
import logging

class Partner(models.Model):
    _inherit = "res.partner"

    penalidad_id = fields.Many2one('mora_cliente.penalidad',string='Penalidad')

    def calcular_interes_mora(self):
        for cliente in self:
            timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
            fecha_hoy = datetime.now().astimezone(timezone).date()
            #Facturas mora, representa las facturas con mora generadas hoy, para que no genere de nuevo mora el dia que se le da click al boton. solo una vez
            facturas_mora = self.env['account.move'].search([('partner_id','=', cliente.id),('move_type','=','out_invoice'),('journal_id','=', cliente.penalidad_id.diario_id.id),('invoice_date','=', fecha_hoy)],order='invoice_date desc')
            # logging.warning(facturas_mora)
            # logging.warning('facturas_mora')
            # logging.warning(fecha_hoy)
            lineas_factura_mora = []
            lineas_factura = []
            if len(facturas_mora) == 0 and cliente.unreconciled_aml_ids and cliente.penalidad_id and cliente.penalidad_id.prioidad == 1:
                linea_factura_mora = []
                tipo_cargo = cliente.penalidad_id.tipo_cargo
                importe = cliente.penalidad_id.importe
                for factura in cliente.unreconciled_aml_ids:
                    if factura.move_id.journal_id.id != cliente.penalidad_id.diario_id.id and factura.move_id.move_type == "out_invoice":
                        mora_total = self.obtener_mora_facturas(fecha_hoy,factura,tipo_cargo,importe)
                        if mora_total > 0:
                            logging.warning('obtener_mora_facturas')
                            linea_factura_dic = {
                                'product_id': cliente.penalidad_id.producto_id.id,
                                'name': str(cliente.penalidad_id.producto_id.name) +' '+str(factura.move_id.name),
                                'quantity': 1,
                                'price_unit': mora_total,
                            }
                            lineas_factura.append(linea_factura_dic)
                        else:
                            logging.warning('No hay facturas anteriores por mora de esta factura')
                            dias_sumar = 0
                            dias_vencimiento_permitidos = cliente.penalidad_id.dias_vencimiento_permitidos
                            if dias_vencimiento_permitidos > 0:
                                dias_sumar += dias_vencimiento_permitidos
                            nueva_fecha = factura.move_id.invoice_date_due + timedelta(days=dias_sumar)
                            logging.warning(factura.invoice_date)
                            logging.warning(nueva_fecha)
                            logging.warning(fecha_hoy)
                            if fecha_hoy > nueva_fecha:
                                mora_total = 0
                                dias = (fecha_hoy - nueva_fecha).days +1
                                logging.warning(dias)
                                logging.warning('si hay mora')
                                mora = 0
                                if tipo_cargo == 'porcentaje':
                                    valor_mora = factura.move_id.amount_total*(importe/100)
                                    mora_total = valor_mora * dias
                                    logging.warning('porcentaje')
                                    logging.warning(mora_total)
                                else:
                                    logging.warning('fijo')
                                    mora_total = dias * importe
                                linea_factura_dic = {
                                    'product_id': cliente.penalidad_id.producto_id.id,
                                    'name': str(cliente.penalidad_id.producto_id.name) +' '+str(factura.move_id.name),
                                    'quantity': 1,
                                    'price_unit': mora_total,
                                    'factura_origen_mora_id': factura.move_id.id,
                                }
                                lineas_factura.append(linea_factura_dic)
                        # lineas_factura_mora = self.env['account.move.line'].search([('factura_origen_mora_id','=',factura.id),('invoice_date','=',fecha_hoy)],order='date desc')
                        # logging.warning('lineas_facturas_mora')
                        # logging.warning(lineas_factura_mora)

                factura_dic = {
                    'move_type': 'out_invoice',
                    'partner_id': cliente.id,
                    'journal_id': cliente.penalidad_id.diario_id.id,
                    'invoice_date': fecha_hoy,
                }
                factura_id = self.env['account.move'].create(factura_dic)
                # factura_id.write({ 'invoice_line_ids': [[6, 0, []]] })
                for linea in lineas_factura:
                    linea['move_id'] = factura_id.id
                    linea_factura_id = self.env['account.move.line'].create(linea)


                logging.warning(facturas_mora)
            logging.warning('test')
        return True

    #obtener mora si hay facturas ya generadas, entonces no calcula desde la fecha inicio de la primera factura, si no que la ultima factura
    def obtener_mora_facturas(self,fecha_hoy, factura, tipo_cargo, importe):
        for f in self:
            mora_total = 0
            test_factura = self.env['account.move.line'].search([('factura_origen_mora_id','=',factura.move_id.id)],order='date desc')
            logging.warning(test_factura)
            logging.warning('obtener_mora_facturas')
            lineas_factura_mora = self.env['account.move.line'].search([('factura_origen_mora_id','=',factura.move_id.id),('move_id.invoice_date','<',fecha_hoy),('move_id.state','=','posted')],order='date desc')
            logging.warning(lineas_factura_mora)
            if len(lineas_factura_mora)>0:

                logging.warning(lineas_factura_mora.move_id.invoice_date)
                if fecha_hoy > lineas_factura_mora[0].move_id.invoice_date:

                    dias = (fecha_hoy - lineas_factura_mora[0].move_id.invoice_date).days
                    if tipo_cargo == 'porcentaje':
                        valor_mora = factura.move_id.amount_total*(importe/100)
                        mora_total = valor_mora * dias
                        logging.warning('porcentaje mora factura')
                        logging.warning(mora_total)
                    else:
                        logging.warning(' mora factura')
                        mora_total = dias * importe
            return mora_total
