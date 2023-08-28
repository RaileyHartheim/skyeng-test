import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Review, UploadedFile
from .utils import check_py_code


logger = logging.getLogger(__name__)


@shared_task
def check_files():
    files = UploadedFile.objects.filter(status__in=['new', 'reloaded'])
    for file in files:
        try:
            logger.info(f'Начата проверка {file.filename}')
            report = check_py_code(file.filename)

            review, created = Review.objects.get_or_create(
                file=file,
                owner=file.owner,
                status='created')
            review.review_text = report
            review.save()
            file.status = 'reviewed'
            file.save()
            logger.info(f'Проверка {file.filename} окончена')
        except Exception as exc:
            logger.error(f' При проверке {file.filename} произошла ошибка: {str(exc)}')


@shared_task
def send_review():
    reviews = Review.objects.filter(status__in=['created', 'sent-failure'])

    for review in reviews:
        owner_email = review.owner.email
        subject = 'Отчет по проверке загруженного файла'
        message = f"""
            Ваш файл {review.file.filename} был проверен. Проверка выявила следующее:\n
            {review.review_text}
            """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[owner_email])
            review.status = 'sent-success'
            logger.info(f'Отчет по проверке {review.file.filename} успешно отправлен.')
        except Exception as exc:
            review.status = 'sent-failure'
            review.review_errors = str(exc)
            logger.error(f' Не удалось отправить отчет по проверке {review.file.filename}: {str(exc)}')
        review.save()
