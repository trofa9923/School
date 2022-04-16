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
from datetime import date

from odoo import models, fields, api, _
from odoo.modules.module import get_module_resource
from odoo.exceptions import ValidationError


class BISchoolStudent(models.Model):
    _name = "bi.school.student"
    _description = "School Students"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [
        ('student_no_uniq', 'unique(student_no)', "Student ID Number already exists !"),
    ]

    _STATE = [
        ('application', "Application"),
        ('active', "Active"),
        ('graduate', "Graduated"),
        ('dropout', "Dropout")
    ]

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    student_no = fields.Char('Student ID No.')
    name = fields.Char('Name', compute="_compute_name", store=True)
    last_name = fields.Char('Last Name', track_visibility='onchange', index=True)
    first_name = fields.Char('First Name', track_visibility='onchange', index=True)
    middle_name = fields.Char('Middle Name', track_visibility='onchange', index=True)
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
        ('female', 'Female')
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
    school_id = fields.Many2one('bi.school', "School", track_visibility='onchange')
    active = fields.Boolean(default=True)

    @api.depends('last_name', 'first_name', 'middle_name')
    def _compute_name(self):
        for rec in self:
            rec.name = "%s, %s %s" % (rec.last_name, rec.first_name, rec.middle_name)

    @api.depends('birthday')
    def _get_age(self):
        today = date.today()
        for rec in self:
            born = fields.Date.from_string(rec.birthday)
            if born:
                rec.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                rec.age = 0.0

    def action_application(self):
        self.write({'state': 'application'})

    def action_activate(self):
        sequence_obj = self.env['ir.sequence'].sudo()
        for rec in self:
            if not rec.id_number:
                rec.write({
                    'state': 'active',
                    'id_number': sequence_obj.next_by_code('tf.school')
                })
            else:
                rec.state = 'active'

    def action_graduate(self):
        self.write({'state': 'graduate', 'date_graduation': fields.Date.today()})

    def action_dropout(self):
        self.write({'state': 'dropout'})

    def unlink(self):
        if self.filtered(lambda student_id: student_id.state != 'application'):
            raise ValidationError('You may not delete a previously enrolled student.')
        return super(BISchoolStudent, self).unlink()



