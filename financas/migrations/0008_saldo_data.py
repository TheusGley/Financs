# Generated by Django 4.2.3 on 2023-08-02 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financas', '0007_despesa_dp_rc_receita_dp_rc'),
    ]

    operations = [
        migrations.AddField(
            model_name='saldo',
            name='data',
            field=models.DateTimeField(auto_now_add=True, default='2023-08-03'),
            preserve_default=False,
        ),
    ]
