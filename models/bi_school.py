# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2022.
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
from datetime import date
from odoo import api, fields, models


class BiSchools(models.Model):
    _name = 'bi.school'
    _description = "Schools"
    _inherit = ['mail.thread']

    _LEVEL = [
        ('elementary', "Elementary"),
        ('secondary', "Secondary"),
        ('tertiary', "Tertiary"),
    ]

    name = fields.Char("School Name", store=True, copy=False, required=True)
    street_number = fields.Integer("Street #", track_visibility='onchange')
    address_1 = fields.Char("Address", track_visibility='onchange')
    address_2 = fields.Char("Address 2", track_visibility='onchange')
    city = fields.Char("City", track_visibility='onchange')
    loc_state = fields.Char("State", track_visibility='onchange')
    phone = fields.Char('Phone', track_visibility='onchange')
    email = fields.Char('Email', track_visibility='onchange')
    level = fields.Selection(_LEVEL, "Level", default='elementary', copy=False, track_visibility='onchange')
    image_medium = fields.Binary("School Logo", attachment=True,
                                 help="Medium-sized photo of the employee. It is automatically "
                                      "resized as a 128x128px image, with aspect ratio preserved. "
                                      "Use this field in form views or some kanban views.")
    student_ids = fields.One2many('bi.school.student', 'school_id', "Students")
    students_count = fields.Integer("Student Count", compute='get_student_count', store=True, copy=False)

    @api.depends('student_ids')
    def get_student_count(self):
        for rec in self:
            rec.students_count = len(rec.student_ids)

    def get_student_count_svr_act(self):
        bi_school_obj = self.pool.get('tf.schools')
        for id in self:
            school_id = bi_school_obj.browse([id])
            bi_school_obj.write({'students_count': len(school_id.student_ids)})

    def open_student_list(self):
        self.ensure_one()
        return {
            'name': 'Student list of %s' % self.name,
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'bi.school.student',
            'view_id': self.env.ref('bi_school.bi_school_tree_view').id,
            'context': {'default_school_id': self.id},
            'domain': [('school_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'target': 'current'
        }
