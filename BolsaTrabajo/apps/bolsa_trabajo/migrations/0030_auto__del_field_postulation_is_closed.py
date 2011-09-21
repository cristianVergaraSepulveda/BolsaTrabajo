# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Postulation.is_closed'
        db.delete_column('bolsa_trabajo_postulation', 'is_closed')


    def backwards(self, orm):
        
        # Adding field 'Postulation.is_closed'
        db.add_column('bolsa_trabajo_postulation', 'is_closed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bolsa_trabajo.enterprise': {
            'Meta': {'object_name': 'Enterprise', '_ormbases': ['auth.User']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'has_unread_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'rut': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'bolsa_trabajo.enterprisecomment': {
            'Meta': {'object_name': 'EnterpriseComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enterprise': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ent'", 'to': "orm['bolsa_trabajo.Enterprise']"}),
            'has_replies': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.EnterpriseComment']", 'null': 'True'})
        },
        'bolsa_trabajo.offer': {
            'Meta': {'object_name': 'Offer'},
            'available_slots': ('django.db.models.fields.IntegerField', [], {}),
            'closure_reason': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2011, 10, 5)'}),
            'enterprise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Enterprise']"}),
            'has_unread_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bolsa_trabajo.OfferLevel']", 'symmetrical': 'False'}),
            'liquid_salary': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolsa_trabajo.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'bolsa_trabajo.offercomment': {
            'Meta': {'ordering': "('creation_date',)", 'object_name': 'OfferComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'has_replies': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Offer']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.OfferComment']", 'null': 'True', 'blank': 'True'})
        },
        'bolsa_trabajo.offerlevel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'OfferLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum_salary': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'bolsa_trabajo.offermessage': {
            'Meta': {'object_name': 'OfferMessage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.OfferMessageRing']"})
        },
        'bolsa_trabajo.offermessagering': {
            'Meta': {'object_name': 'OfferMessageRing'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Offer']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Student']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unread_messages': ('django.db.models.fields.IntegerField', [], {})
        },
        'bolsa_trabajo.postulation': {
            'Meta': {'unique_together': "(('offer', 'student'),)", 'object_name': 'Postulation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Offer']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Student']"})
        },
        'bolsa_trabajo.student': {
            'Meta': {'object_name': 'Student', '_ormbases': ['auth.User']},
            'has_cv': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.StudentLevel']"}),
            'resume': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolsa_trabajo.Tag']", 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'bolsa_trabajo.studentlevel': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'StudentLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {})
        },
        'bolsa_trabajo.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'bolsa_trabajo.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'block_public_access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolsa_trabajo.Tag']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'validated_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'bolsa_trabajo.workregistry': {
            'Meta': {'object_name': 'WorkRegistry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postulation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Postulation']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bolsa_trabajo']
