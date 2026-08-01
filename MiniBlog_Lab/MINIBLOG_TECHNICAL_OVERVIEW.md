# MiniBlog Lab: technical overview before Stage 9

Дата анализа: 2026-08-01.

Цель документа: зафиксировать фактическое состояние Django-проекта перед переходом от Function-Based Views к Class-Based Views и Generic Views в Stage 9. Код проекта не менялся, кроме создания этого отчета.

## 1. Краткое резюме

Проект содержит Django project `config` и два Django apps: `core` и `posts`.

Фактическое состояние `posts`:

- модель `Post` реализована в `posts/models.py`;
- `Post` зарегистрирован в админке через `PostAdmin` в `posts/admin.py`;
- `PostForm` как `forms.ModelForm` реализован в `posts/forms.py`;
- `posts/urls.py` содержит `app_name = 'posts'`, но `urlpatterns = []`;
- `posts/views.py` не содержит ни одной view, только docstring;
- шаблонов `posts/templates/...` в проекте нет;
- маршруты списка, просмотра, создания, редактирования и удаления постов не реализованы;
- текущих FBV для `posts` нет;
- текущих CBV для `posts` нет;
- `PostForm` сейчас нигде не используется;
- `commit=False` нигде в коде не используется;
- `instance=` нигде в коде не используется;
- `redirect()`, `reverse()` и `reverse_lazy()` в фактическом коде не используются;
- `{% url %}` используется только в `core/templates/core/base.html` для `core:home`, `core:about`, `core:contacts`.

Важно: в учебных документах `docs/` есть примеры и планируемые имена вроде `posts:post_list` и `posts:post_detail`, но это не текущая реализация. В отчете они не считаются существующим кодом.

Проверка `./.venv/bin/python manage.py check` выполнена: Django сообщает `System check identified no issues (0 silenced)`.

## 2. Структура проекта

Корневая структура без `.venv`, `.git`, `__pycache__`:

```text
MiniBlog_Lab/
├── manage.py
├── db.sqlite3
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   └── templates/
│       └── core/
│           ├── base.html
│           ├── home.html
│           ├── about.html
│           ├── contacts.html
│           └── request_demo.html
├── posts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_initial.py
│       └── 0002_post_views_count.py
└── docs/
    ├── DJANGO_GUIDE.md
    └── Программа_самообучения_Django_MiniBlog_Lab_Stage_1-12.md
```

Django apps подключены в `config/settings.py`:

- `core.apps.CoreConfig`;
- `posts.apps.PostsConfig`.

Настройки шаблонов в `config/settings.py`:

- `TEMPLATES[0]['DIRS'] = []`;
- `TEMPLATES[0]['APP_DIRS'] = True`;
- шаблоны ищутся внутри app-директорий `templates/`;
- глобальной директории `templates/` в корне проекта нет;
- директории `posts/templates/` сейчас нет.

## 3. Таблица существующих маршрутов

Главный URLconf: `config/urls.py`.

| Полный URL | URLconf | View | URL name | Статус |
|---|---|---|---|---|
| `/admin/` | `config/urls.py` | Django admin | стандартные admin names | реализовано |
| `/` | `core/urls.py` | `core.views.home` | `core:home` | реализовано |
| `/about/` | `core/urls.py` | `core.views.about` | `core:about` | реализовано |
| `/contacts/` | `core/urls.py` | `core.views.contact` | `core:contacts` | реализовано |
| `/request-demo/` | `core/urls.py` | `core.views.request_demo` | `core:request_demo` | реализовано |
| `/posts/` | `posts/urls.py` | нет | нет | include есть, но маршрутов внутри нет |

`config/urls.py`:

- `path("admin/", admin.site.urls)`;
- `path("", include("core.urls"))`;
- `path("posts/", include("posts.urls"))`.

Замечание: в `config/urls.py` есть лишний импорт `from xml.etree.ElementInclude import include`, затем он перекрывается корректным импортом `from django.urls import path, include`. Это не ломает текущий запуск, но выглядит как технический шум.

`posts/urls.py`:

- импортирует `path`;
- импортирует `views` из `posts`;
- задает `app_name = 'posts'`;
- содержит пустой `urlpatterns = []`.

Следствие: имена `posts:post_list`, `posts:post_detail`, `posts:post_create`, `posts:post_update`, `posts:post_delete` сейчас не существуют.

## 4. Подробный разбор views

### Views приложения `posts`

В `posts/views.py` нет существующих view.

Файл содержит только:

```python
"""Views for the posts application."""
```

Таблица CRUD views для `posts`:

| Имя | Тип | URL | HTTP-методы | Модель | Форма | Шаблон | Context | Redirect | Ответственность |
|---|---|---|---|---|---|---|---|---|---|
| список постов | не реализовано | не реализовано | не реализовано | `Post` есть, но view нет | нет | нет | нет | нет | не реализовано |
| просмотр поста | не реализовано | не реализовано | не реализовано | `Post` есть, но view нет | нет | нет | нет | нет | не реализовано |
| создание поста | не реализовано | не реализовано | не реализовано | `Post` есть, но view нет | `PostForm` существует, но не используется | нет | нет | нет | не реализовано |
| редактирование поста | не реализовано | не реализовано | не реализовано | `Post` есть, но view нет | `PostForm` существует, но не используется | нет | нет | нет | не реализовано |
| удаление поста | не реализовано | не реализовано | не реализовано | `Post` есть, но view нет | нет | нет | нет | нет | не реализовано |

### Views приложения `core`

Хотя Stage 9 касается `posts`, эти views существуют в проекте и являются текущими рабочими view.

| Имя | Тип | URL | Разрешенные HTTP-методы | Модель | Форма | Шаблон | Context | Redirect | Ответственность |
|---|---|---|---|---|---|---|---|---|---|
| `home` | FBV | `/` | явно не ограничены; любые методы попадут в render | нет | нет | `core/home.html` | `page_title`, `student_name` | нет | главная страница |
| `about` | FBV | `/about/` | явно не ограничены; любые методы попадут в render | нет | нет | `core/about.html` | нет | нет | страница "О проекте" |
| `contact` | FBV | `/contacts/` | явно не ограничены; любые методы попадут в render | нет | нет | `core/contacts.html` | нет | нет | страница контактов |
| `request_demo` | FBV | `/request-demo/` | явно не ограничены; `POST` обрабатывается как отправка формы, все не-`POST` получают пустую форму | нет | `DemoRequestForm` | `core/request_demo.html` | `form`, `result` | нет | демонстрация обычной формы |

В проекте нет CBV ни в `core`, ни в `posts`.

## 5. Формы и валидация

### `posts.forms.PostForm`

Файл: `posts/forms.py`.

Класс:

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'is_published',
        ]
```

Фактические свойства:

- тип: `forms.ModelForm`;
- модель: `posts.models.Post`;
- поля: `title`, `content`, `is_published`;
- пользовательских `clean_*` или `clean()` методов нет;
- widgets, labels, help_texts не заданы;
- форма не используется ни в одной view;
- через эту форму сейчас не реализовано ни создание, ни редактирование.

### Создание и редактирование через `ModelForm`

Не реализовано.

В проекте нет кода вида:

- `form = PostForm(request.POST)`;
- `form.save()`;
- `form.save(commit=False)`;
- `PostForm(instance=post)`;
- `PostForm(request.POST, instance=post)`.

### `commit=False`

`commit=False` в фактическом коде проекта не используется.

### `instance`

`instance=` в фактическом коде проекта не используется.

### `core.forms.DemoRequestForm`

Существует обычная `forms.Form`, не связанная с `Post`.

Поля:

- `student`;
- `email`;
- `course`;
- `subscribe`;
- `notes`;
- `password`.

Есть потенциальная ошибка: `clean` объявлен как `@property def clean(self)`, а не как обычный метод `def clean(self)`. Внутри также используется `super().clean` без вызова `()`. Это относится к `core`, а не к `posts`, но может помешать корректной валидации `/request-demo/`.

## 6. Шаблоны и контекст

### Шаблоны `posts`

Не реализованы.

В проекте нет:

- `posts/templates/posts/post_list.html`;
- `posts/templates/posts/post_detail.html`;
- `posts/templates/posts/post_form.html`;
- `posts/templates/posts/post_confirm_delete.html`;
- любых других шаблонов в `posts/templates/`.

Следствие для generic views:

- `ListView` по умолчанию будет искать `posts/post_list.html`;
- `DetailView` по умолчанию будет искать `posts/post_detail.html`;
- `CreateView` и `UpdateView` по умолчанию будут искать `posts/post_form.html`;
- `DeleteView` по умолчанию будет искать `posts/post_confirm_delete.html`;
- ни один из этих шаблонов сейчас отсутствует.

### `core/templates/core/base.html`

Содержит базовую HTML-структуру и навигацию:

- `{% url 'core:home' %}`;
- `{% url 'core:about' %}`;
- `{% url 'core:contacts' %}`.

Ссылок на `posts` нет.

### `core/templates/core/home.html`

Расширяет `core/base.html`.

Ожидает context:

- `page_title`;
- `student_name`.

Эти переменные передаются из `core.views.home`.

### `core/templates/core/about.html`

Расширяет `core/base.html`.

Ожидает context:

- `page_title`;
- `some_info`.

`core.views.about` context не передает, поэтому эти значения сейчас будут пустыми в шаблоне.

### `core/templates/core/contacts.html`

Расширяет `core/base.html`.

Ожидает context:

- `page_title`;
- `contacts_info`.

`core.views.contact` context не передает, поэтому эти значения сейчас будут пустыми в шаблоне.

### `core/templates/core/request_demo.html`

Не расширяет `core/base.html`.

Ожидает context:

- `form`;
- `result`.

Эти переменные передаются из `core.views.request_demo`.

## 7. Полный жизненный цикл CRUD

### 1. Как пользователь открывает список постов

Не реализовано.

Фактически:

- `config/urls.py` подключает `posts.urls` под префиксом `/posts/`;
- `posts/urls.py` пустой;
- URL `/posts/` не связан ни с одной view;
- шаблона списка постов нет;
- URL name для списка постов нет.

### 2. Как пользователь открывает один пост

Не реализовано.

Фактически:

- маршрута вида `/posts/<pk>/` нет;
- view для получения одного `Post` нет;
- шаблона detail-страницы нет;
- URL name для detail-страницы нет.

### 3. Как пользователь создает пост

Не реализовано.

Фактически:

- `PostForm` существует;
- route для создания отсутствует;
- view для `GET` пустой формы отсутствует;
- view для `POST` с `PostForm(request.POST)` отсутствует;
- вызова `form.save()` нет;
- redirect после успешного создания не задан;
- шаблона формы поста нет.

### 4. Как пользователь редактирует пост

Не реализовано.

Фактически:

- route для редактирования отсутствует;
- view для получения существующего `Post` отсутствует;
- `PostForm(instance=post)` не используется;
- `PostForm(request.POST, instance=post)` не используется;
- redirect после успешного редактирования не задан;
- шаблона формы поста нет.

### 5. Реализовано ли удаление

Удаление не реализовано.

Фактически:

- route для удаления отсутствует;
- view удаления отсутствует;
- confirm template отсутствует;
- redirect после удаления не задан.

### 6. HTTP-методы на каждом этапе

Для CRUD постов HTTP-методы не реализованы, потому что нет маршрутов и views.

Ожидаемая схема для будущей реализации, не текущий код:

- список: обычно `GET`;
- detail: обычно `GET`;
- create: обычно `GET` для формы и `POST` для отправки;
- update: обычно `GET` для формы и `POST` для отправки;
- delete: обычно `GET` для подтверждения и `POST` для удаления.

### 7. Какие шаблоны рендерятся

Для CRUD постов никакие шаблоны не рендерятся.

### 8. Куда происходит перенаправление после успешной отправки формы

Для CRUD постов redirect не реализован.

В `core.views.request_demo` redirect тоже нет: после успешной отправки `POST` та же страница `core/request_demo.html` рендерится с `result = form.cleaned_data`.

## 8. Найденные несоответствия и риски

### Критичные для Stage 9

1. `posts/urls.py` пустой.

   Нельзя перевести существующие post routes на CBV, потому что текущих post routes нет. Сначала нужно определить URL names и URL patterns.

2. `posts/views.py` пустой.

   Нет существующих FBV для списка, detail, create, update или delete. Формулировка "переход от FBV к CBV" фактически не соответствует текущему состоянию `posts`: переносить нечего, можно только создать новые CBV или сначала восстановить FBV как учебный шаг.

3. Шаблоны `posts` отсутствуют.

   Generic views без явного `template_name` будут падать с `TemplateDoesNotExist`, если добавить CBV без шаблонов.

4. `PostForm` не используется.

   Для `CreateView`/`UpdateView` можно использовать `form_class = PostForm`, но текущего поведения формы в view нет, поэтому нечего сохранять как совместимость.

5. URL names для `posts` отсутствуют.

   Нужно выбрать стабильные имена перед правкой шаблонов. Учебные документы упоминают `posts:post_list` и `posts:post_detail`, но фактического кода с этими именами нет.

6. У `Post` нет `get_absolute_url()`.

   Для `CreateView` и `UpdateView` понадобится `success_url`, `get_success_url()` или `get_absolute_url()` на модели. Сейчас ни один вариант не реализован.

7. Удаление не подготовлено.

   Для `DeleteView` нужны route, view, confirm template и success redirect. В текущем проекте нет ни одной из этих частей.

### Некритичные, но заметные

1. `config/urls.py` содержит лишний импорт `include` из `xml.etree.ElementInclude`.

   Он перекрыт правильным импортом из `django.urls`, поэтому текущий `manage.py check` не падает.

2. `core/templates/core/about.html` и `core/templates/core/contacts.html` ожидают context-переменные, которые views не передают.

   Это не ломает рендеринг, но вывод будет пустым.

3. `core.forms.DemoRequestForm.clean` написан как property.

   Это не относится к `posts`, но для обучения формам лучше исправить отдельно в будущем.

4. `posts/tests.py` пустой.

   Нет тестов, которые помогли бы безопасно подтвердить переход на CBV.

5. В `posts.models.Post` нет `Meta.ordering`.

   Для `ListView` нужно явно решить порядок сортировки: через `ordering`, `get_queryset()` или `Meta.ordering`.

## 9. Рекомендованный порядок Stage 9

Так как post CRUD сейчас не реализован, безопасный порядок Stage 9 лучше строить не как механический рефакторинг существующих post FBV, а как поэтапное введение CBV с минимальным количеством движущихся частей.

1. Сначала зафиксировать целевые URL names и шаблоны для `posts`.

   Рекомендуемые имена, согласованные с учебными материалами:

   - `posts:post_list`;
   - `posts:post_detail`;
   - `posts:post_create`;
   - `posts:post_update`;
   - `posts:post_delete`.

   Нужно учитывать, что `core/base.html` сейчас не содержит ссылок на `posts`. Если добавлять навигацию, она должна ссылаться только на реально созданные URL names.

2. Первой FBV заменить на базовый `View`.

   В текущем `posts` нет FBV. Если наставнику важно именно показать переход FBV -> `View`, лучше сначала учебно реализовать простую FBV списка или detail, а затем заменить ее на базовый `django.views.View`.

   Самый безопасный кандидат для демонстрации базового `View`: список постов, потому что он требует только `GET`, модель `Post` и шаблон списка. Но если цель строго "заменить существующую FBV", такой FBV сейчас нет.

3. Первой заменить на `ListView`.

   Лучший первый generic CBV: список постов.

   Причины:

   - не нужна форма;
   - не нужен redirect;
   - можно проверить ORM-запрос и template context;
   - стандартный context `object_list`/`post_list` хорошо показывает отличие generic views.

   Перед этим нужен шаблон `posts/post_list.html` или явный `template_name`.

4. Затем использовать `DetailView`.

   После списка логично добавить detail-страницу:

   - route с `pk`;
   - `DetailView` для `Post`;
   - шаблон `posts/post_detail.html`;
   - ссылки из списка через `{% url 'posts:post_detail' post.pk %}`.

   Нужно решить, показывать все посты или только `is_published=True`. Текущий код этого поведения не задает.

5. Позже перевести создание на `CreateView`.

   Для `CreateView` уже есть `PostForm`.

   Нужно заранее определить:

   - `form_class = PostForm` или `fields = [...]`;
   - `template_name` или стандартный `posts/post_form.html`;
   - `success_url`/`get_success_url()`;
   - redirect после успешного создания, например на detail или list.

   Так как текущего `commit=False` нет, вводить его нужно только если появится дополнительная логика перед сохранением.

6. Затем перевести редактирование на `UpdateView`.

   Для `UpdateView` можно переиспользовать `PostForm`.

   Нужно учитывать:

   - `instance` при generic `UpdateView` создается самим Django через объект view;
   - вручную писать `PostForm(instance=post)` не потребуется, если используется `UpdateView`;
   - шаблон можно переиспользовать с `CreateView`, если UI одинаковый.

7. Готов ли проект к `DeleteView`.

   Сейчас проект не готов к `DeleteView`.

   Перед добавлением нужны:

   - route удаления;
   - confirm template, обычно `posts/post_confirm_delete.html`;
   - `success_url`, чаще всего на `posts:post_list`;
   - ссылки или кнопки удаления в detail/list шаблонах;
   - понимание, должен ли delete быть доступен всем пользователям, потому что авторизация в проекте для `posts` сейчас не реализована.

8. Зависимости URL и шаблонов, которые нужно учитывать.

   - `config/urls.py` уже подключает `posts.urls` под `/posts/`.
   - `posts/urls.py` уже содержит `app_name = 'posts'`.
   - Любой `{% url 'posts:...' %}` в шаблонах начнет работать только после добавления соответствующего `path(..., name='...')`.
   - Generic views имеют стандартные имена шаблонов; либо нужно создать эти шаблоны, либо явно задать `template_name`.
   - Для `CreateView`, `UpdateView`, `DeleteView` нужен стабильный redirect через `success_url`, `reverse_lazy()` или `get_success_url()`.

## 10. Список файлов, которые наставнику нужно увидеть в первую очередь

1. `posts/views.py`

   Главный факт: views для постов отсутствуют.

2. `posts/urls.py`

   Главный факт: `app_name = 'posts'` есть, но `urlpatterns = []`.

3. `posts/models.py`

   Модель `Post` содержит поля `title`, `content`, `created_at`, `updated_at`, `is_published`, `views_count` и `__str__`.

4. `posts/forms.py`

   `PostForm` уже есть как `ModelForm` по полям `title`, `content`, `is_published`, но пока нигде не используется.

5. `posts/admin.py`

   `Post` зарегистрирован в админке через `PostAdmin`.

6. `config/urls.py`

   `posts.urls` подключен под `/posts/`, но внутри app URLconf маршрутов нет.

7. `config/settings.py`

   Важно проверить `INSTALLED_APPS` и `TEMPLATES`: app templates включены через `APP_DIRS=True`, глобальных template dirs нет.

8. `core/templates/core/base.html`

   Сейчас навигация содержит только ссылки на `core`, ссылок на `posts` нет.

9. `core/views.py` и `core/urls.py`

   Нужны для понимания текущих работающих FBV и стиля проекта.

10. `docs/DJANGO_GUIDE.md`

   Не является фактической реализацией, но содержит учебные ориентиры и примерные имена маршрутов `posts:post_list`, `posts:post_detail`.
