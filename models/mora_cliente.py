# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command


class MoraCliente(models.Model):
    _name = "mora_cliente.penalidad"

    name = fields.Char('Nombre')
    prioidad = fields.Integer('Prioridad')
    dias_vencimiento_permitidos = fields.Integer('Dias de vencimiento permitidos')
    tipo_cargo = fields.Selection(selection=[('importe_fijo', 'Importe fijo'),('porcentaje', 'Porcentaje'),], string='Tipo de cargo')
    importe = fields.Float('Importe', digits=(16, 6))
    penalidad = fields.Float('Penalidad Máxima')
    producto_id = fields.Many2one('product.product','Producto')
    diario_id = fields.Many2one('account.journal','Diario', required=True)
