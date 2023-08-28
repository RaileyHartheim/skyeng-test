import subprocess


def check_py_code(filename):
    """
    Функция, которая проверяет код на соответствие PEP8 и возвращает отчет.
    """
    checker = subprocess.run(
        ['flake8', f'media/uploaded_files/{filename}'],
        capture_output=True,
        text=True
    )

    if checker.returncode == 0:
        return 'Ошибок не выявлено.'
    errors = ''
    result = checker.stdout
    for line in result.split('\n'):
        parts = line.split(':', 1)
        if len(parts) >= 2:
            errors += parts[1]
            errors += '\n'
    return errors
