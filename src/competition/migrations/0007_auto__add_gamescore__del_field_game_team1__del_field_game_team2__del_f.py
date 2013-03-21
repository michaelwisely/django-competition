# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameScore'
        db.create_table('competition_gamescore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Game'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Team'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('extra_data', self.gf('django.db.models.fields.TextField')(default='null', null=True)),
        ))
        db.send_create_signal('competition', ['GameScore'])

        # Deleting field 'Game.team1'
        db.delete_column('competition_game', 'team1_id')

        # Deleting field 'Game.team2'
        db.delete_column('competition_game', 'team2_id')

        # Deleting field 'Game.team2_score'
        db.delete_column('competition_game', 'team2_score')

        # Deleting field 'Game.team1_score'
        db.delete_column('competition_game', 'team1_score')

        # Adding field 'Game.status'
        db.add_column('competition_game', 'status',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


        # Changing field 'Game.start_time'
        db.alter_column('competition_game', 'start_time', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Game.end_time'
        db.alter_column('competition_game', 'end_time', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Deleting model 'GameScore'
        db.delete_table('competition_gamescore')

        # Adding field 'Game.team1'
        db.add_column('competition_game', 'team1',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['competition.Team']),
                      keep_default=False)

        # Adding field 'Game.team2'
        db.add_column('competition_game', 'team2',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['competition.Team']),
                      keep_default=False)

        # Adding field 'Game.team2_score'
        db.add_column('competition_game', 'team2_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Game.team1_score'
        db.add_column('competition_game', 'team1_score',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Deleting field 'Game.status'
        db.delete_column('competition_game', 'status')


        # User chose to not deal with backwards NULL issues for 'Game.start_time'
        raise RuntimeError("Cannot reverse this migration. 'Game.start_time' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Game.end_time'
        raise RuntimeError("Cannot reverse this migration. 'Game.end_time' and its values cannot be restored.")

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
        'competition.avatar': {
            'Meta': {'object_name': 'Avatar'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_height': ('django.db.models.fields.IntegerField', [], {}),
            'image_width': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'thumbnail_height': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {})
        },
        'competition.competition': {
            'Meta': {'ordering': "['-is_running', '-is_open', '-start_time']", 'object_name': 'Competition'},
            'avatar': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['competition.Avatar']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_running': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_num_team_members': ('django.db.models.fields.IntegerField', [], {}),
            'min_num_team_members': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'payment_option': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['competition.RegistrationQuestion']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'competition.game': {
            'Meta': {'object_name': 'Game'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Competition']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'extra_data': ('django.db.models.fields.TextField', [], {'default': "'null'", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['competition.Team']", 'through': "orm['competition.GameScore']", 'symmetrical': 'False'})
        },
        'competition.gamescore': {
            'Meta': {'object_name': 'GameScore'},
            'extra_data': ('django.db.models.fields.TextField', [], {'default': "'null'", 'null': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Team']"})
        },
        'competition.invitation': {
            'Meta': {'ordering': "['-sent']", 'object_name': 'Invitation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'received_invitations'", 'to': "orm['auth.User']"}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_invitations'", 'to': "orm['auth.User']"}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Team']"})
        },
        'competition.organizer': {
            'Meta': {'object_name': 'Organizer'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['competition.OrganizerRole']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'competition.organizerrole': {
            'Meta': {'object_name': 'OrganizerRole'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'competition.registration': {
            'Meta': {'object_name': 'Registration'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signup_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'competition.registrationquestion': {
            'Meta': {'object_name': 'RegistrationQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'competition.registrationquestionchoice': {
            'Meta': {'object_name': 'RegistrationQuestionChoice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_choice_set'", 'to': "orm['competition.RegistrationQuestion']"})
        },
        'competition.registrationquestionresponse': {
            'Meta': {'object_name': 'RegistrationQuestionResponse'},
            'agreed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'response_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['competition.RegistrationQuestionChoice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'response_set'", 'to': "orm['competition.RegistrationQuestion']"}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'response_set'", 'to': "orm['competition.Registration']"}),
            'text_response': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'competition.team': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('competition', 'slug'),)", 'object_name': 'Team'},
            'avatar': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['competition.Avatar']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Competition']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'eligible_to_win': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'time_paid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['competition']