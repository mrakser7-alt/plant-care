# Деплой на PythonAnywhere (бесплатный план)

Замени в инструкции `MYUSER` на твой логин PythonAnywhere, а `MYGHUSER` — на твой GitHub-логин.

---

## Шаг 1. Залить код на GitHub

Открой обычный терминал/PowerShell в папке проекта (`c:\Users\Mercedes\Desktop\джанго`).

1. Зайди на https://github.com/new → создай **приватный или публичный** репозиторий `plant-care` (без README/gitignore — они уже есть).
2. Скопируй адрес репозитория и выполни:

```bash
git remote add origin https://github.com/MYGHUSER/plant-care.git
git push -u origin main
```

Если просят логин/пароль — введи GitHub-логин и **Personal Access Token** (не пароль). Токен создаётся тут: https://github.com/settings/tokens → Generate new token (classic) → галка `repo` → Generate.

---

## Шаг 2. Зарегистрироваться на PythonAnywhere

1. Открой https://www.pythonanywhere.com/registration/register/beginner/ — план **Beginner (бесплатно, без карты)**.
2. Придумай логин `MYUSER` (это будет в адресе сайта: `MYUSER.pythonanywhere.com`) и пароль.
3. Подтверди email.

---

## Шаг 3. Залить код через Bash-консоль PythonAnywhere

На странице PythonAnywhere нажми **Consoles → Bash**. Внутри консоли:

```bash
cd ~
git clone https://github.com/MYGHUSER/plant-care.git
cd plant-care
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Шаг 4. Настроить окружение и базу

В той же консоли (всё ещё `cd ~/plant-care`, venv активирован):

```bash
# Сгенерировать новый SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Скопируй получившийся ключ (длинная строка). Он понадобится на следующем шаге.

Создай файл `.env` в корне проекта (через `nano .env` или через Files в веб-интерфейсе):

```
DJANGO_SECRET_KEY=ВСТАВЬ_СЮДА_КЛЮЧ
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=MYUSER.pythonanywhere.com
```

Применить миграции и собрать статику:

```bash
export $(cat .env | xargs)
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser   # придумай логин/пароль для админки
```

---

## Шаг 5. Создать Web app

В шапке PythonAnywhere: **Web → Add a new web app**.

1. Next (домен `MYUSER.pythonanywhere.com`).
2. Выбрать **Manual configuration** (НЕ «Django»).
3. Выбрать **Python 3.12**.
4. Next → Web-app создан.

На странице Web заполни секции:

### Code
- **Source code**: `/home/MYUSER/plant-care`
- **Working directory**: `/home/MYUSER/plant-care`
- **WSGI configuration file**: кликни по ссылке — откроется редактор. **Удали всё содержимое** и вставь:

```python
import os
import sys
from pathlib import Path

project_home = '/home/MYUSER/plant-care'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Загрузить .env
env_file = Path(project_home) / '.env'
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())

os.environ['DJANGO_SETTINGS_MODULE'] = 'plantcare.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Замени `MYUSER` на свой логин. **Save**.

### Virtualenv
Введи: `/home/MYUSER/plant-care/venv`

### Static files
Добавь две записи (кнопка **Enter URL / Directory**):

| URL | Directory |
|---|---|
| `/static/` | `/home/MYUSER/plant-care/staticfiles` |
| `/media/` | `/home/MYUSER/plant-care/media` |

---

## Шаг 6. Запустить

Наверху страницы Web нажми **большую зелёную кнопку Reload**.

Открой `https://MYUSER.pythonanywhere.com/` — должен открыться сайт. Залогинься своим суперюзером, добавь растение.

Админка: `https://MYUSER.pythonanywhere.com/admin/`

---

## Когда обновляешь код

Дома:
```bash
git add -A
git commit -m "изменения"
git push
```

На PythonAnywhere в Bash:
```bash
cd ~/plant-care
git pull
source venv/bin/activate
python manage.py migrate            # если меняли модели
python manage.py collectstatic --noinput
```
Потом на странице Web — **Reload**.

---

## Частые ошибки

- **DisallowedHost** → в `.env` проверь, что `DJANGO_ALLOWED_HOSTS` содержит ровно `MYUSER.pythonanywhere.com`.
- **Static files 404 (нет стилей)** → ты не собрал статику (`python manage.py collectstatic`) или не прописал `/static/` в Web → Static files.
- **Фото загружаются, но не показываются** → нет маппинга `/media/` в Web → Static files.
- **Ошибка 500** → в Web → Log files открой **Error log**, смотри последние строки.
- **На бесплатном плане сайт "засыпает"** — нет, это только у Render. PythonAnywhere держит сайт постоянно, но есть лимит 100 секунд CPU в день и сайт принудительно выключается через 3 месяца если не зайти в аккаунт.
