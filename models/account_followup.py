# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import timedelta


class Followup(models.Model):
    _inherit = 'account_followup'

    def calcular_interes_mora(self):
        return True
