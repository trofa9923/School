# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2022
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
import pytz

from odoo import models, fields

_tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]


def _tz_get(self):
    return _tzs


_FORMATS = [
    ('format1', 'FirstName MI. LastName'),
    ('format2', 'FirstName MiddleName LastName'),
    ('format3', 'LastName, FirstName MiddleName'),
    ('format4', 'LastName, FirstName MI.'),
    ('user_defined', 'User-Defined')
]


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    name_format = fields.Selection(_FORMATS, 'Name Format', related='company_id.name_format', readonly=False)
    tz = fields.Selection(_tz_get, string='Timezone', related='company_id.tz', default='Asia/Manila', readonly=False)


class ResCompany(models.Model):
    _inherit = 'res.company'

    name_format = fields.Selection(_FORMATS, 'Name Format', default='user_defined')
    tz = fields.Selection(_tz_get, string='Timezone', default='Asia/Manila')
