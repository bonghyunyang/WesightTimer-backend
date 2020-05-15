# Generated by Django 3.0.6 on 2020-05-15 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'gender',
            },
        ),
        migrations.CreateModel(
            name='GenderType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'gender_types',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.CharField(max_length=50, null=True)),
                ('number', models.CharField(max_length=50, null=True)),
                ('expire_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'payments',
            },
        ),
        migrations.CreateModel(
            name='PaymentStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'payment_status',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'subscription_types',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('unique_name', models.CharField(max_length=50, null=True)),
                ('teacher_bio', models.TextField()),
                ('signup_date', models.DateTimeField(auto_now_add=True)),
                ('facebook', models.CharField(max_length=45, null=True)),
                ('twitter', models.CharField(max_length=45, null=True)),
                ('linked_in', models.CharField(max_length=45, null=True)),
                ('email', models.CharField(max_length=45, null=True)),
                ('facebook_messenger', models.CharField(max_length=45, null=True)),
                ('teacher_img', models.CharField(max_length=200, null=True)),
                ('gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Gender')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Location')),
            ],
            options={
                'db_table': 'teachers',
            },
        ),
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'time_zones',
            },
        ),
        migrations.CreateModel(
            name='UserIntroduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.CharField(max_length=1000, null=True)),
                ('tagline', models.CharField(max_length=200, null=True)),
                ('introduction', models.CharField(max_length=2000, null=True)),
                ('profile_image', models.CharField(max_length=200, null=True)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Location')),
                ('time_zone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.TimeZone')),
            ],
            options={
                'db_table': 'user_introductions',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('full_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=200)),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Payment')),
                ('payment_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.PaymentStatus')),
                ('user_introduction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.UserIntroduction')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='TeacherReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=200)),
                ('write_date', models.DateTimeField(auto_now_add=True)),
                ('teacher_rating', models.IntegerField()),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Teacher')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
            options={
                'db_table': 'teacher_reviews',
            },
        ),
        migrations.CreateModel(
            name='TeacherFollow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Teacher')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
            options={
                'db_table': 'teacher_follows',
            },
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_1', models.CharField(max_length=100, null=True)),
                ('status_2', models.DateTimeField(auto_now_add=True)),
                ('cycle', models.CharField(max_length=50)),
                ('started', models.DateTimeField(auto_now_add=True, null=True)),
                ('next_bill', models.DateTimeField(auto_now=True, null=True)),
                ('biling', models.CharField(max_length=50, null=True)),
                ('next_cycle', models.CharField(max_length=50, null=True)),
                ('subscribe_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.SubscriptionType')),
            ],
            options={
                'db_table': 'subscriptions',
            },
        ),
        migrations.CreateModel(
            name='PlayHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('play_count', models.IntegerField()),
                ('content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Content')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
            options={
                'db_table': 'play_histories',
            },
        ),
        migrations.CreateModel(
            name='MyCourseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Course')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
            options={
                'db_table': 'my_course_groups',
            },
        ),
        migrations.CreateModel(
            name='CampaignCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.CharField(max_length=50, null=True)),
                ('subscription_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Subscription')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
            options={
                'db_table': 'campaign_courses',
            },
        ),
    ]
