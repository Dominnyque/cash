# Generated by Django 4.2.4 on 2023-12-16 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_alter_category_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='leads.category'),
        ),
    ]
