# -*- coding: utf-8 -*-

# Copyright (C) 2007-2014, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import, division, print_function, unicode_literals
from django.db import transaction
from django.utils.translation import ugettext as _
from fluo import forms
from .models import TermsOfService, UserAgreement, UserAgreementOption


class UserAgreementForm(forms.Form):
    def __init__(self, request, tos, id='tos_%s', widget=forms.CheckboxInput, attrs=None, *args, **kwargs):
        self.tos = tos
        self.id = id
        super(UserAgreementForm, self).__init__(*args, **kwargs)

        # accept general TermsOfService
        tos_id = id.replace('_%s', '')
        self.fields[tos_id] = forms.BooleanField(
            required=True,
            label=_('I have read and agree to the Terms of Service'),
            widget=widget(attrs=attrs),
            error_messages={
                'required': _("You must agree to the Terms of Service to register"),
            },
        )

        # accept each TermsOfService Option
        for option in tos.options.all():
            self.fields[id % option.key] = forms.BooleanField(
                required=option.required,
                label=option.translate().label,
                widget=widget(attrs=attrs),
                error_messages={
                    'required': _("You must agree to the Terms of Service to register"),
                },
            )

    @transaction.atomic
    def save(self, request, user=None, *args, **kwargs):
        agreement = UserAgreement.objects.create(
            user=request.user if user is None else user,
            tos=TermsOfService.objects.current,
        )
        id = self.id
        for option in self.tos.options.all():
            UserAgreementOption.objects.create(
                parent=agreement,
                option=option,
                value=self.cleaned_data.get(id % option.key),
            )
        return agreement
