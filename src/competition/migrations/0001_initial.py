# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Avatar'
        db.create_table('competition_avatar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image_height', self.gf('django.db.models.fields.IntegerField')()),
            ('image_width', self.gf('django.db.models.fields.IntegerField')()),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('thumbnail_height', self.gf('django.db.models.fields.IntegerField')()),
            ('thumbnail_width', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('competition', ['Avatar'])

        # Adding model 'Competition'
        db.create_table('competition_competition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('avatar', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['competition.Avatar'], unique=True, null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_running', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost_per_person', self.gf('django.db.models.fields.FloatField')()),
            ('min_num_team_members', self.gf('django.db.models.fields.IntegerField')()),
            ('max_num_team_members', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('competition', ['Competition'])

        # Adding M2M table for field questions on 'Competition'
        db.create_table('competition_competition_questions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('competition', models.ForeignKey(orm['competition.competition'], null=False)),
            ('registrationquestion', models.ForeignKey(orm['competition.registrationquestion'], null=False))
        ))
        db.create_unique('competition_competition_questions', ['competition_id', 'registrationquestion_id'])

        # Adding model 'Game'
        db.create_table('competition_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Competition'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('competition', ['Game'])

        # Adding model 'Team'
        db.create_table('competition_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Competition'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('avatar', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['competition.Avatar'], unique=True, null=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_paid', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('eligible_to_win', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('competition', ['Team'])

        # Adding unique constraint on 'Team', fields ['competition', 'slug']
        db.create_unique('competition_team', ['competition_id', 'slug'])

        # Adding M2M table for field members on 'Team'
        db.create_table('competition_team_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm['competition.team'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('competition_team_members', ['team_id', 'user_id'])

        # Adding model 'Invitation'
        db.create_table('competition_invitation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Team'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_invitations', to=orm['auth.User'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='received_invitations', to=orm['auth.User'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('sent', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('response', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('competition', ['Invitation'])

        # Adding model 'OrganizerRole'
        db.create_table('competition_organizerrole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('competition', ['OrganizerRole'])

        # Adding model 'Organizer'
        db.create_table('competition_organizer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Competition'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('competition', ['Organizer'])

        # Adding M2M table for field role on 'Organizer'
        db.create_table('competition_organizer_role', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organizer', models.ForeignKey(orm['competition.organizer'], null=False)),
            ('organizerrole', models.ForeignKey(orm['competition.organizerrole'], null=False))
        ))
        db.create_unique('competition_organizer_role', ['organizer_id', 'organizerrole_id'])

        # Adding model 'Registration'
        db.create_table('competition_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Competition'])),
            ('signup_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('competition', ['Registration'])

        # Adding model 'RegistrationQuestion'
        db.create_table('competition_registrationquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('question', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('competition', ['RegistrationQuestion'])

        # Adding model 'RegistrationQuestionChoice'
        db.create_table('competition_registrationquestionchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='question_choice_set', to=orm['competition.RegistrationQuestion'])),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('competition', ['RegistrationQuestionChoice'])

        # Adding model 'RegistrationQuestionResponse'
        db.create_table('competition_registrationquestionresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='response_set', to=orm['competition.RegistrationQuestion'])),
            ('registration', self.gf('django.db.models.fields.related.ForeignKey')(related_name='response_set', to=orm['competition.Registration'])),
            ('text_response', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('agreed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('competition', ['RegistrationQuestionResponse'])

        # Adding M2M table for field choices on 'RegistrationQuestionResponse'
        db.create_table('competition_registrationquestionresponse_choices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registrationquestionresponse', models.ForeignKey(orm['competition.registrationquestionresponse'], null=False)),
            ('registrationquestionchoice', models.ForeignKey(orm['competition.registrationquestionchoice'], null=False))
        ))
        db.create_unique('competition_registrationquestionresponse_choices', ['registrationquestionresponse_id', 'registrationquestionchoice_id'])

        # Adding model 'Score'
        db.create_table('competition_score', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Game'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Team'])),
            ('score', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('competition', ['Score'])


    def backwards(self, orm):
        # Removing unique constraint on 'Team', fields ['competition', 'slug']
        db.delete_unique('competition_team', ['competition_id', 'slug'])

        # Deleting model 'Avatar'
        db.delete_table('competition_avatar')

        # Deleting model 'Competition'
        db.delete_table('competition_competition')

        # Removing M2M table for field questions on 'Competition'
        db.delete_table('competition_competition_questions')

        # Deleting model 'Game'
        db.delete_table('competition_game')

        # Deleting model 'Team'
        db.delete_table('competition_team')

        # Removing M2M table for field members on 'Team'
        db.delete_table('competition_team_members')

        # Deleting model 'Invitation'
        db.delete_table('competition_invitation')

        # Deleting model 'OrganizerRole'
        db.delete_table('competition_organizerrole')

        # Deleting model 'Organizer'
        db.delete_table('competition_organizer')

        # Removing M2M table for field role on 'Organizer'
        db.delete_table('competition_organizer_role')

        # Deleting model 'Registration'
        db.delete_table('competition_registration')

        # Deleting model 'RegistrationQuestion'
        db.delete_table('competition_registrationquestion')

        # Deleting model 'RegistrationQuestionChoice'
        db.delete_table('competition_registrationquestionchoice')

        # Deleting model 'RegistrationQuestionResponse'
        db.delete_table('competition_registrationquestionresponse')

        # Removing M2M table for field choices on 'RegistrationQuestionResponse'
        db.delete_table('competition_registrationquestionresponse_choices')

        # Deleting model 'Score'
        db.delete_table('competition_score')


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
            'cost_per_person': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_running': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_num_team_members': ('django.db.models.fields.IntegerField', [], {}),
            'min_num_team_members': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['competition.RegistrationQuestion']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'competition.game': {
            'Meta': {'object_name': 'Game'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Competition']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
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
        'competition.score': {
            'Meta': {'object_name': 'Score'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Team']"})
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
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