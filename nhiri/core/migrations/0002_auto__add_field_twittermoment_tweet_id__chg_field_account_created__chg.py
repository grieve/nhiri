# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TwitterMoment.tweet_id'
        db.add_column(u'core_twittermoment', 'tweet_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)


        # Changing field 'Account.created'
        db.alter_column(u'core_account', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Account.refreshed'
        db.alter_column(u'core_account', 'refreshed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):
        # Deleting field 'TwitterMoment.tweet_id'
        db.delete_column(u'core_twittermoment', 'tweet_id')


        # Changing field 'Account.created'
        db.alter_column(u'core_account', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Account.refreshed'
        db.alter_column(u'core_account', 'refreshed', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'core.account': {
            'Meta': {'object_name': 'Account'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refreshed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'retweet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['core']