# Generated by Django 5.1.7 on 2025-04-10 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('duracao', models.IntegerField(help_text='Duração do serviço em minutos')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8)),
                ('qtde_slots', models.IntegerField(default=1, help_text='Quantidade de slots disponíveis para o serviço')),
                ('imagem_url', models.URLField(blank=True, help_text='URL da imagem do serviço', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Serviço',
                'verbose_name_plural': 'Serviços',
            },
        ),
    ]
