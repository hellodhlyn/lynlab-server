# Generated by Django 2.0.1 on 2018-01-06 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20161002_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='url',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, default='', verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='post',
            name='series',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts', to='blog.Series'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.TextField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='posthitaddress',
            name='address',
            field=models.TextField(default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='postlikeaddress',
            name='address',
            field=models.TextField(default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='series',
            name='name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='tag',
            name='url',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='tagtranslations',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
    ]
