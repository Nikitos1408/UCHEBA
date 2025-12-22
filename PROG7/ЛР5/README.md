# Настройка виртуального окружения
1. Создайте в данном каталоге виртуально окружение Python:
   `python -m venv environment`
2. Активируйте данное окружение:
    - Windows CMD: `environment/bin/activate.bat`
    - Windows PowerShell: `environment/bin/activate.ps1` 
    - Bash Shell: `source environment/bin/activate`
    - Csh Sell: `source environment/bin/activate.csh`
    - Fish Shell`source environment/bin/activate.fish`
3. Установите зависимости:
    `pip install -r requirements.txt`

# Super-user и админ-интерфейс
1. Админ-интерфейс: http://127.0.0.1:8000/admin/
2. Учётная запись:
    - Login: admin
    - Password: changeit


FYI: https://djangowaves.com/tips-tricks/how-to-reset-the-django-admin-password/