# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2020 Taliform Inc
#
# Author: Benjamin Cerdena Jr <benjamin@taliform.com>
# V13 Porting: Martin Perez <martin@taliform.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##############################################################################
from odoo import api, models, fields
from odoo.exceptions import ValidationError

class DateEnded(models.TransientModel):
    _name = 'tf.school.date_end.wizard'

    date_end = fields.Date('Date End')


    def action_date(self):
        item = self.env['tf.school'].browse(self._context.get('active_ids', [])) # To check the active_ids
        if self.date_end == fields.Date.context_today(self):
            vals = {
                'date_end': self.date_end,
                'state': 'done'
            }
            res = item.write(vals)
            return res
        else:
            vals = {
                'date_end': self.date_end
            }
            res = item.write(vals)
            return res

