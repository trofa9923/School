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
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolScheduleConfig(models.Model):
    _name = "bi.school.sched.config"
    _description = "Schedule Configuration"
    _inherit = ['mail.thread']

    SCHEDULE = [('monday', 'Monday'),
                ('tuesday', 'Tuesday'),
                ('wednesday', 'Wednesday'),
                ('thursday', 'Thursday'),
                ('friday', 'Friday'),
                ('saturday', 'Saturday'),
                ('sunday', 'Sunday')]

    name = fields.Selection(SCHEDULE, track_visibility="onchange")


class SchoolYearLevelConfig(models.Model):
    _name = "bi.school.year_level.config"
    _description = "Year Level Configuration"
    _inherit = ['mail.thread']

    name = fields.Char(string="Year Name", track_visibility="onchange")


class SchoolSubjectsConfig(models.Model):
    _name = "bi.school.subject.config"
    _description = "Subject Configuration"
    _inherit = ['mail.thread']

    name = fields.Char(string="Subject Name", track_visibility="onchange")
    year_level_id = fields.Many2one('bi.school.year_level.config', string="Year Level", track_visibility='onchange')

