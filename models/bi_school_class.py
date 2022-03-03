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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BISchoolClass(models.Model):
    _name = "bi.school.class"
    _description = "School Classes"
    _inherit = ['mail.thread']

    STATE = [('draft', 'Draft'),
             ('cancelled', 'Cancelled'),
             ('in_progress', 'In Progress'),
             ('done', 'Done')]


    name = fields.Char(string='Name', track_visibility="onchange", copy=False,
                   index=True, default=lambda self: _('New'))
    description = fields.Char('Description', track_visibility="onchange")
    state = fields.Selection(STATE, string='State', default='draft', track_visibility="onchange", copy=False)
    teacher_id = fields.Many2one('bi.school.teacher', string="Teacher", track_visibility="onchange")
    schedule_ids = fields.Many2many('bi.school.schedule.config', track_visibility="onchange")
    time_start = fields.Float('Time Start', track_visibility="onchange")
    time_end = fields.Float('Time End', track_visibility="onchange")
    date_start = fields.Date('Date Started', track_visibility="onchange")
    date_end = fields.Date('Date Ended', track_visibility="onchange")
    student_ids = fields.Many2many('bi.school.student', string='Students', required=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('class_number') or _('New')
        res = super(BISchoolClass, self).create(vals)
        return res

    def _check_conflicts(self):
        # Search classes that are in progress
        class_ids = self.search([('state', '=', 'in_progress')])
        # Filter classes that have a schedule conflict
        class_ids = class_ids.filtered(
            lambda class_id: class_id.time_start <= self.time_start <= class_id.time_end
                             or class_id.time_start <= self.time_end <= class_id.time_end
        )
        # Filter classes on the same day by instersecting schedule intersect
        class_ids = class_ids.filtered(lambda class_id: self.schedule_ids & class_id.schedule_ids)

        # Check conflicting schedule with the same teacher
        teacher_conflict_ids = class_ids.filtered(lambda class_id: self.teacher_id == class_id.teacher_id)
        if teacher_conflict_ids:
            raise ValidationError("Teacher: %s has a conflicting schedule with the following classes: %s"
                                  % (self.teacher_id.name, ", ".join(teacher_conflict_ids.mapped('name'))))

        # Check conflicting schedule with the same student
        for student_id in self.student_ids:
            # Filter conflicting classes where student exists
            student_conflict_ids = class_ids.filtered(lambda class_id: student_id in class_id.student_ids)
            if student_conflict_ids:
                raise ValidationError("Student: %s has a conflicting schedule with the following classes: %s"
                                      % (student_id.name, ", ".join(student_conflict_ids.mapped('name'))))

    def action_date_started(self):
        self._check_conflicts()
        self.write({
            'date_start': fields.Date.context_today(self),
            'state': 'in_progress'
        })

    def action_date_ended(self):
        self.write({'state': 'done'})

    def action_reset_to_draft(self):
        self.write({'date_start': '',
                    'date_end': '',
                    'state': 'draft'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

    @api.model
    def update_class_end_date(self):
        self.search([
            ('state', '=', 'in_progress'),
            ('date_end', '=', fields.Date.context_today(self))
        ]).action_date_ended()