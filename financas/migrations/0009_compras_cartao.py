# Generated by Django 4.2.3 on 2023-08-30 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financas', '0008_saldo_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compras_cartao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data', models.DateField()),
                ('cartao_credito', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='financas.cartao_credito')),
            ],
        ),
    ]
