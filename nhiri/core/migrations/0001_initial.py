# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'core_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('refreshed', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'core', ['Account'])

        # Adding model 'TwitterAccount'
        db.create_table(u'core_twitteraccount', (
            (u'account_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Account'], unique=True, primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('followers', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('following', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('tweet_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('access_token_key', self.gf('django.db.models.fields.TextField')(default='')),
            ('access_token_secret', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'core', ['TwitterAccount'])

        # Adding model 'Moment'
        db.create_table(u'core_moment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('kind', self.gf('django.db.models.fields.CharField')(default='text', max_length=10)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Account'])),
        ))
        db.send_create_signal(u'core', ['Moment'])

        # Adding model 'TwitterMoment'
        db.create_table(u'core_twittermoment', (
            (u'moment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Moment'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('retweet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('original_author', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
        ))
        db.send_create_signal(u'core', ['TwitterMoment'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'core_account')

        # Deleting model 'TwitterAccount'
        db.delete_table(u'core_twitteraccount')

        # Deleting model 'Moment'
        db.delete_table(u'core_moment')

        # Deleting model 'TwitterMoment'
        db.delete_table(u'core_twittermoment')


    models = {
        u'core.account': {
            'Meta': {'object_name': 'Account'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refreshed': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'core.moment': {
            'Meta': {'object_name': 'Moment'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '10'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'core.twitteraccount': {
            'Meta': {'object_name': 'TwitterAccount', '_ormbases': [u'core.Account']},
            'access_token_key': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'access_token_secret': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'account_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Account']", 'unique': 'True', 'primary_key': 'True'}),
            'followers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'tweet_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'core.twittermoment': {
            'Meta': {'object_name': 'TwitterMoment', '_ormbases': [u'core.Moment']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'moment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Moment']", 'unique': 'True', 'primary_key': 'True'}),
            'original_author': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'retweet': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['core']