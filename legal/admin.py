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
from django.conf import settings
from fluo import admin
from fluo import forms
from .models import TermsOfService, TermsOfServiceTranslation, UserAgreement


LANG = len(settings.LANGUAGES)


class TermsOfServiceTranslationInlineForm(forms.ModelForm):
    pass
class TermsOfServiceTranslationInline(admin.StackedInline):
    form = TermsOfServiceTranslationInlineForm
    model = TermsOfServiceTranslation
    extra = 0
    max_num = LANG
class TermsOfServiceAdminForm(forms.ModelForm):
    pass
class TermsOfServiceAdmin(admin.ModelAdmin):
    form = TermsOfServiceAdminForm
    inlines = (TermsOfServiceTranslationInline,)
admin.site.register(TermsOfService, TermsOfServiceAdmin)


class UserAgreementAdminForm(forms.ModelForm):
    pass
class UserAgreementAdmin(admin.ModelAdmin):
    form = UserAgreementAdminForm
    related_search_fields = {
        'tos': ('pk', 'version',),
        'user': ('pk', 'username', 'first_name', 'last_name', 'email',),
    }

admin.site.register(UserAgreement, UserAgreementAdmin)
