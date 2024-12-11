# Generated by Django 4.2.7 on 2024-10-20 16:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Declaration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Введён'), (2, 'В работе'), (3, 'Завершен'), (4, 'Отклонен'), (5, 'Удален')], default=1, verbose_name='Статус')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2024, 10, 20, 16, 17, 13, 145960, tzinfo=datetime.timezone.utc), verbose_name='Дата создания')),
                ('date_formation', models.DateTimeField(blank=True, null=True, verbose_name='Дата формирования')),
                ('date_complete', models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')),
                ('date', models.DateField(blank=True, null=True)),
                ('moderator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='moderator', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Декларация',
                'verbose_name_plural': 'Декларации',
                'db_table': 'declarations',
                'ordering': ('-date_formation',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Название')),
                ('status', models.IntegerField(choices=[(1, 'Действует'), (2, 'Удалена')], default=1, verbose_name='Статус')),
                ('image', models.ImageField(blank=True, default='default.png', upload_to='')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.IntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'Вещь',
                'verbose_name_plural': 'Вещи',
                'db_table': 'items',
            },
        ),
        migrations.CreateModel(
            name='ItemDeclaration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(blank=True, null=True)),
                ('declaration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.declaration')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.item')),
            ],
            options={
                'verbose_name': 'м-м',
                'verbose_name_plural': 'м-м',
                'db_table': 'item_declaration',
                'unique_together': {('item', 'declaration')},
            },
        ),
    ]
