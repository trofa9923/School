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
{
    'name': 'School - PH',
    'version': '13.0.1.0',
    'depends': ['mail'],
    'author': 'BI',
    'website': '',
    'category': 'School',
    'data': ['security/bi_school_group_security.xml',
             'security/ir.model.access.csv',
             # 'data/bi_school_class_date_end_data.xml',
             'data/bi_school_schedule_data.xml',
             'wizard/bi_school_class_date_wizard_view.xml',
             'views/bi_school_view.xml',
             'views/bi_school_class_view.xml',
             'views/bi_school_students_view.xml',
             'views/bi_school_teacher_view.xml',
             'views/bi_school_config_view.xml',
             'views/bi_school_menu.xml'
             ],
    'auto_install': False,
}
