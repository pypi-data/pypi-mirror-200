#
# This file is part of pretix (Community Edition).
#
# Copyright (C) 2014-2020 Raphael Michel and contributors
# Copyright (C) 2020-2021 rami.io GmbH and contributors
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation in version 3 of the License.
#
# ADDITIONAL TERMS APPLY: Pursuant to Section 7 of the GNU Affero General Public License, additional terms are
# applicable granting you additional permissions and placing additional restrictions on your usage of this software.
# Please refer to the pretix LICENSE file to obtain the full terms applicable to this work. If you did not receive
# this file, see <https://pretix.eu/about/en/license>.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.
#
from datetime import timedelta

from django.conf import settings
from django.db.models import Max, Q
from django.dispatch import receiver
from django.utils.timezone import now

from pretix.base.models.auth import StaffSession

from ..signals import periodic_task


@receiver(signal=periodic_task)
def close_inactive_staff_sessions(sender, **kwargs):
    StaffSession.objects.annotate(last_used=Max('logs__datetime')).filter(
        Q(last_used__lte=now() - timedelta(seconds=settings.PRETIX_SESSION_TIMEOUT_RELATIVE)) & Q(date_end__isnull=True)
    ).update(
        date_end=now()
    )
