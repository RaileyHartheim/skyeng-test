import os

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UploadedFile(models.Model):
    """ Модель для загруженного файла. """

    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('reloaded', 'Заново загружен'),
        ('deleted', 'Удален'),
        ('reviewed', 'Проверен'),
        ('reviewed-sent', 'Проверен (отчет отправлен)')
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Загрузивший файл')
    file = models.FileField(
        upload_to='uploaded_files/',
        null=False,
        blank=False,
        verbose_name='Загружаемый файл',
        help_text='Загрузите файл с расширением .py')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name='Статус файла')
    upload_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время загрузки')
    review_sent = models.BooleanField(
        verbose_name='Отправлен ли отчет',
        default=False)

    def __str__(self) -> str:
        return f'{self.file.name} - загружено {self.owner}'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def display_file_text(self):
        if self.status != 'deleted':
            with open(self.file.path) as fp:
                return fp.read().replace('\n', '<br>')
        return 'Этот файл удален.'


class Review(models.Model):
    """ Модель для отчета по проверке. """

    STATUS_CHOICES = (
        ('created', 'Создан'),
        ('sent-success', 'Отправлен'),
        ('sent-failure', 'Не отправлен из-за ошибки'),
        ('file-deleted', 'Файл удален')
    )

    file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        verbose_name='Проверяемый файл')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Загрузивший файл')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name='Статус проверки')
    review_text = models.TextField(
        blank=True,
        null=True,
        verbose_name='Содержимое отчета по проверке')
    review_errors = models.TextField(
        blank=True,
        null=True,
        verbose_name='Ошибки при отправке')
    check_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания отчета')

    def __str__(self) -> str:
        return f'{self.file.name} - загружено {self.owner}'

    class Meta:
        verbose_name = 'Отчет по проверке'
        verbose_name_plural = 'Отчеты по проверке'
