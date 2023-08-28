# Generated by Django 4.1.10 on 2023-08-26 13:30

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
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(help_text='Загрузите файл с расширением .py', upload_to='uploaded_files/', verbose_name='Загружаемый файл')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('reloaded', 'Заново загружен'), ('deleted', 'Удален'), ('reviewed', 'Проверен'), ('reviewed-sent', 'Проверен (отчет отправлен)')], max_length=20, verbose_name='Статус файла')),
                ('upload_time', models.DateTimeField(auto_now_add=True, verbose_name='Время загрузки')),
                ('review_sent', models.BooleanField(default=False, verbose_name='Отправлен ли отчет')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Загрузивший файл')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('created', 'Создан'), ('sent-success', 'Отправлен'), ('sent-failure', 'Не отправлен из-за ошибки'), ('file-deleted', 'Файл удален')], max_length=20, verbose_name='Статус проверки')),
                ('review_text', models.TextField(blank=True, null=True, verbose_name='Содержимое отчета по проверке')),
                ('review_errors', models.TextField(blank=True, null=True, verbose_name='Ошибки при отправке')),
                ('check_time', models.DateTimeField(auto_now_add=True, verbose_name='Время создания отчета')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.uploadedfile', verbose_name='Проверяемый файл')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Загрузивший файл')),
            ],
            options={
                'verbose_name': 'Отчет по проверке',
                'verbose_name_plural': 'Отчеты по проверке',
            },
        ),
    ]