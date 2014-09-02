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

from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Option'
        db.create_table(u'legal_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ordering', self.gf('fluo.db.models.fields.OrderField')(default=0, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')()),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('label', self.gf('django.db.models.fields.TextField')()),
            ('error_message', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
        ))
        db.send_create_signal(u'legal', ['Option'])

        # Adding unique constraint on 'Option', fields ['ordering', 'key']
        db.create_unique(u'legal_option', ['ordering', 'key'])

        # Adding model 'OptionTranslation'
        db.create_table(u'legal_optiontranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'translations', to=orm['legal.Option'])),
            ('label', self.gf('django.db.models.fields.TextField')()),
            ('error_message', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
        ))
        db.send_create_signal(u'legal', ['OptionTranslation'])

        # Adding unique constraint on 'OptionTranslation', fields ['parent', 'language']
        db.create_unique(u'legal_optiontranslation', ['parent_id', 'language'])

        # Adding model 'TermsOfService'
        db.create_table(u'legal_termsofservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('fluo.db.models.fields.StatusField')(default=u'draft')),
            ('version', self.gf('django.db.models.fields.DecimalField')(unique=True, max_digits=5, decimal_places=2, db_index=True)),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('human_title', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('human_text', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
        ))
        db.send_create_signal(u'legal', ['TermsOfService'])

        # Adding M2M table for field options on 'TermsOfService'
        m2m_table_name = db.shorten_name(u'legal_termsofservice_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('termsofservice', models.ForeignKey(orm[u'legal.termsofservice'], null=False)),
            ('option', models.ForeignKey(orm[u'legal.option'], null=False))
        ))
        db.create_unique(m2m_table_name, ['termsofservice_id', 'option_id'])

        # Adding model 'TermsOfServiceTranslation'
        db.create_table(u'legal_termsofservicetranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'translations', to=orm['legal.TermsOfService'])),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('human_title', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('human_text', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
        ))
        db.send_create_signal(u'legal', ['TermsOfServiceTranslation'])

        # Adding unique constraint on 'TermsOfServiceTranslation', fields ['language', 'parent']
        db.create_unique(u'legal_termsofservicetranslation', ['language', 'parent_id'])

        # Adding unique constraint on 'TermsOfServiceTranslation', fields ['human_title', 'human_text']
        db.create_unique(u'legal_termsofservicetranslation', ['human_title', 'human_text'])

        # Adding model 'UserAgreement'
        db.create_table(u'legal_useragreement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('fluo.db.models.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('last_modified_at', self.gf('fluo.db.models.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('tos', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'terms', to=orm['legal.TermsOfService'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'user_agreement', to=orm['accounts.User'])),
        ))
        db.send_create_signal(u'legal', ['UserAgreement'])

        # Adding unique constraint on 'UserAgreement', fields ['user', 'tos']
        db.create_unique(u'legal_useragreement', ['user_id', 'tos_id'])

        # Adding model 'UserAgreementOption'
        db.create_table(u'legal_useragreementoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'options', to=orm['legal.UserAgreement'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'user_agreements', to=orm['legal.Option'])),
            ('value', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'legal', ['UserAgreementOption'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserAgreement', fields ['user', 'tos']
        db.delete_unique(u'legal_useragreement', ['user_id', 'tos_id'])

        # Removing unique constraint on 'TermsOfServiceTranslation', fields ['human_title', 'human_text']
        db.delete_unique(u'legal_termsofservicetranslation', ['human_title', 'human_text'])

        # Removing unique constraint on 'TermsOfServiceTranslation', fields ['language', 'parent']
        db.delete_unique(u'legal_termsofservicetranslation', ['language', 'parent_id'])

        # Removing unique constraint on 'OptionTranslation', fields ['parent', 'language']
        db.delete_unique(u'legal_optiontranslation', ['parent_id', 'language'])

        # Removing unique constraint on 'Option', fields ['ordering', 'key']
        db.delete_unique(u'legal_option', ['ordering', 'key'])

        # Deleting model 'Option'
        db.delete_table(u'legal_option')

        # Deleting model 'OptionTranslation'
        db.delete_table(u'legal_optiontranslation')

        # Deleting model 'TermsOfService'
        db.delete_table(u'legal_termsofservice')

        # Removing M2M table for field options on 'TermsOfService'
        db.delete_table(db.shorten_name(u'legal_termsofservice_options'))

        # Deleting model 'TermsOfServiceTranslation'
        db.delete_table(u'legal_termsofservicetranslation')

        # Deleting model 'UserAgreement'
        db.delete_table(u'legal_useragreement')

        # Deleting model 'UserAgreementOption'
        db.delete_table(u'legal_useragreementoption')


    models = {
        u'accounts.user': {
            'Meta': {'ordering': "(u'id',)", 'object_name': 'User'},
            'avatar_image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'avatar_type': ('django.db.models.fields.CharField', [], {'default': "u'auto'", 'max_length': '10'}),
            'blog_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'preferred_language': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'profile': ('fluo.db.models.fields.JSONField', [], {'default': '{}'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'site_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'legal.option': {
            'Meta': {'ordering': "(u'ordering',)", 'unique_together': "((u'ordering', u'key'),)", 'object_name': 'Option'},
            'error_message': ('django.db.models.fields.TextField', [], {'default': False, 'blank':True}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {}),
            'ordering': ('fluo.db.models.fields.OrderField', [], {'default': '0', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {})
        },
        u'legal.optiontranslation': {
            'Meta': {'unique_together': "((u'parent', u'language'),)", 'object_name': 'OptionTranslation'},
            'error_message': ('django.db.models.fields.TextField', [], {'default': False, 'blank':True}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'translations'", 'to': u"orm['legal.Option']"})
        },
        u'legal.termsofservice': {
            'Meta': {'ordering': "(u'-date_begin', u'version')", 'object_name': 'TermsOfService'},
            'date_begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'human_text': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'human_title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['legal.Option']", 'null': 'True', 'blank': 'True'}),
            'status': ('fluo.db.models.fields.StatusField', [], {'default': "u'draft'"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'version': ('django.db.models.fields.DecimalField', [], {'unique': 'True', 'max_digits': '5', 'decimal_places': '2', 'db_index': 'True'})
        },
        u'legal.termsofservicetranslation': {
            'Meta': {'unique_together': "((u'language', u'parent'), (u'human_title', u'human_text'))", 'object_name': 'TermsOfServiceTranslation'},
            'human_text': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'human_title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'translations'", 'to': u"orm['legal.TermsOfService']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        },
        u'legal.useragreement': {
            'Meta': {'ordering': "[u'-created_at']", 'unique_together': "((u'user', u'tos'),)", 'object_name': 'UserAgreement'},
            'created_at': ('fluo.db.models.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_at': ('fluo.db.models.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'tos': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'terms'", 'to': u"orm['legal.TermsOfService']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'user_agreement'", 'to': u"orm['accounts.User']"})
        },
        u'legal.useragreementoption': {
            'Meta': {'object_name': 'UserAgreementOption'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'user_agreements'", 'to': u"orm['legal.Option']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'options'", 'to': u"orm['legal.UserAgreement']"}),
            'value': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['legal']
