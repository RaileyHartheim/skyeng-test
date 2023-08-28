import os
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UploadedFileForm
from .models import Review, UploadedFile


def index(request):
    """ Страница по умолчанию. """

    return render(request, 'reviews/index.html')


@login_required
def upload_file(request):
    """ Представление для загрузки файла. """

    form = UploadedFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        uploaded_file = form.save(commit=False)
        if not uploaded_file.file.name.endswith('.py'):
            form.add_error('file', 'Файл должен иметь расширение .py')
            return render(
                request, 'reviews/upload_form.html', {'form': form})
        uploaded_file.owner = request.user
        uploaded_file.status = 'new'
        uploaded_file.save()
        return redirect('reviews:files_list')
    return render(request, 'reviews/upload_form.html', {'form': form})


@login_required
def edit_file(request, file_id):
    """ Представление для редактирования файла. """

    file = get_object_or_404(UploadedFile, id=file_id)
    if file.owner != request.user:
        return redirect('reviews:index')
    form = UploadedFileForm(
        request.POST or None,
        files=request.FILES or None,
        instance=file
    )
    if form.is_valid():
        if not file.file.name.endswith('.py'):
            form.add_error('file', 'Файл должен быть с расширением .py')
        else:
            form.save(commit=False)
            file.status = 'reloaded'
            form.save()
            return redirect('reviews:file_detail', file_id=file_id)
    context = {
        'form': form,
        'post': file,
        'is_edit': True
    }
    return render(request, 'reviews/upload_form.html', context)


@login_required
def delete_file(request, file_id):
    """ Представление для удаления файла. """

    file = get_object_or_404(UploadedFile, pk=file_id)
    if file.owner != request.user:
        return redirect('reviews:index')
    if os.path.exists(f'media/uploaded_files/{file.filename}'):
        os.remove(f'media/uploaded_files/{file.filename}')
    file.status = 'deleted'
    if Review.objects.filter(file=file_id).exists:
        review = Review.objects.get(file=file_id)
        review.status = 'file-deleted'
    file.save()
    return redirect('reviews:files_list')


@login_required
def get_files_list(request):
    """ Представление для списка загруженных пользователем файлов. """

    uploaded_files = UploadedFile.objects.filter(owner=request.user).order_by("-upload_time")
    files_count = uploaded_files.count()
    paginator = Paginator(uploaded_files, per_page=25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'files_count': files_count
    }
    return render(request, 'reviews/files_list.html', context)


@login_required
def get_file_detail(request, file_id):
    """ Представление для подробной информации о файле. """

    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    review = Review.objects.filter(file=file_id).first()
    context = {
        'uploaded_file': uploaded_file,
        'review': review
    }
    return render(request, 'reviews/file_detail.html', context)
