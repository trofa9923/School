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
import base64

from odoo import models, fields, api, _
from odoo.modules.module import get_module_resource
from odoo.exceptions import ValidationError

class BISchoolStudent(models.Model):
    _name = "bi.school.student"
    _description = "School Students"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [
        ('student_no_uniq', 'unique(student_no)', "Student Number already exists !"),
    ]

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    student_no = fields.Char('Student No.')
    name = fields.Char('Name')
    last_name = fields.Char('Last Name', track_visibility='onchange', index=True)
    first_name = fields.Char('First Name', track_visibility='onchange', index=True)
    middle_name = fields.Char('Middle Name', track_visibility='onchange', index=True)
    suffix_name = fields.Char('Suffix Name', track_visibility='onchange', index=True)
    home_street = fields.Char('Home Street', track_visibility='onchange')
    home_street2 = fields.Char('Home Street 2', track_visibility='onchange')
    home_city = fields.Char('Home City', track_visibility='onchange')
    home_state_id = fields.Many2one('res.country.state', 'Home State', domain="[('country_id','=',country_id)]",
                                    track_visibility='onchange')
    home_zip = fields.Char('Home Zip', track_visibility='onchange')
    home_phone = fields.Char('Phone No.')
    mobile_phone = fields.Char('Mobile No.')
    personal_email = fields.Char('Personal Email')
    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], default="male", tracking=True)
    place_of_birth = fields.Char('Place of Birth')
    country_of_birth = fields.Many2one('res.country', string="Country of Birth")
    birthday = fields.Date('Date of Birth')
    father_name = fields.Char("Father's Name", track_visibility='onchange')
    mother_name = fields.Char("Mother's Name", track_visibility='onchange')
    emergency_contact = fields.Char("Emergency Contact")
    emergency_phone = fields.Char("Emergency Phone")
    user_id = fields.Many2one('res.users', string="Related User")
    adviser_id = fields.Many2one('bi.school.teacher', string="Adviser")
    adviser_subject_id = fields.Many2one('bi.school.subject.config', string="Adviser Subject")
    year_level_id = fields.Many2one('bi.school.year_level.config', string="Year Level", track_visibility='onchange')
    section = fields.Char()
    image_1920 = fields.Image(default=_default_image)
    active = fields.Boolean(default=True)

    @api.onchange('last_name', 'first_name', 'middle_name', 'name')
    def _onchange_employee_name(self):
        for rec in self:
            last_name = rec.last_name.strip() if rec.last_name else ''
            first_name = rec.first_name.strip() + ' ' if rec.first_name else ''
            middle_name = rec.middle_name.strip() + ' ' if rec.middle_name else ''
            rec.name = first_name + middle_name + last_name


