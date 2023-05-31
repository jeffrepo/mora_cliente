# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
from datetime import datetime, date, timedelta
import pytz
import logging

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    factura_origen_mora_id = fields.Many2one('account.move',string='Factura origen mora id')
