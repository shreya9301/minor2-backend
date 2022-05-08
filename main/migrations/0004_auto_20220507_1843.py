# Generated by Django 3.2.5 on 2022-05-07 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_doctor_doctor_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescription',
            old_name='prescription',
            new_name='prescription_medicine',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='patient_img',
        ),
        migrations.AddField(
            model_name='prescription',
            name='prescription_img',
            field=models.ImageField(default='a', upload_to=''),
            preserve_default=False,
        ),
    ]
