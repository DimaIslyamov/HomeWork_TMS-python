# MiniBlog Lab — technical overview

Дата аудита: 2026-08-22

## 1. Структура проекта

Проект состоит из Django-конфигурации `config` и двух приложений:

- `core` — общий слой проекта: `base.html`, static CSS, учебная форма `request_demo`.
- `posts` — доменная логика блога: посты, категории, теги, комментарии, CRUD, auth/ownership.

Основные директории:

- `config/settings.py`, `config/urls.py` — настройки и корневой URLconf.
- `core/templates/core/base.html` — общий layout.
- `core/static/css/main.css` — единый CSS без frontend framework.
- `posts/models.py` — модели `Category`, `Tag`, `Post`, `Comment`.
- `posts/forms.py` — `PostForm`, `CommentForm`.
- `posts/views.py` — CBV для списка, detail, create/update/delete и удаления комментария.
- `posts/templates/posts/` — шаблоны списка, detail, форм и delete-confirmation.
- `posts/templates/registration/login.html` — login template для `LoginView`.
- `posts/migrations/0001`–`0009` — история схемы до comments и tags.

Важно: в контексте задания указан PostgreSQL, но текущий `config/settings.py` настроен на SQLite (`django.db.backends.sqlite3`, `db.sqlite3`). Для учебной локальной работы это допустимо, но для production-style PostgreSQL настройку БД еще нужно привести к ожидаемой.

## 2. Модели и связи

`Category`

- `title`.
- Связь с постами через `Post.category`, `related_name="posts"`.

`Tag`

- `name`, уникальный.
- ManyToMany с постами через `Post.tags`, `related_name="posts"`.

`Post`

- `author` — `ForeignKey` на `AUTH_USER_MODEL`, `CASCADE`, `related_name="posts"`.
- `category` — nullable/blank `ForeignKey` на `Category`, `SET_NULL`.
- `tags` — `ManyToManyField(Tag, blank=True)`.
- `title`, `slug`, `content`, `created_at`, `updated_at`, `is_published`, `views_count`.
- `slug` уникальный, генерируется в `save()` при пустом значении.
- `get_absolute_url()` возвращает `posts:post_detail` по `slug`.

`Comment`

- `post` — `ForeignKey(Post, CASCADE, related_name="comments")`.
- `author` — `ForeignKey(AUTH_USER_MODEL, SET_NULL, null=True, related_name="comments")`.
- `content`, `created_at`, `updated_at`.
- При удаленном пользователе комментарий остается, UI показывает `Deleted user`.

## 3. URLs

Корневые маршруты:

- `/` — redirect на `posts:post_list` (`/posts/`), через Django `RedirectView`.
- `/admin/` — Django admin.
- `/posts/` — маршруты приложения `posts`.
- `/login/` — `LoginView`.
- `/logout/` — `LogoutView`, используется безопасно через POST-форму.

`posts.urls`:

- `/posts/` — `posts:post_list`.
- `/posts/tag/<int:tag_id>/` — `posts:post_list_by_tag`.
- `/posts/create/` — `posts:post_create`.
- `/posts/<slug:slug>/` — `posts:post_detail`.
- `/posts/<slug:slug>/update/` — `posts:post_update`.
- `/posts/<slug:slug>/delete/` — `posts:post_delete`.
- `/posts/comments/<int:pk>/delete/` — `posts:comment_delete`.

Home/About/Contacts удалены из пользовательской навигации и из `core.urls`. Старые шаблоны этих страниц удалены, потому что больше не используются.

## 4. CBV и назначение

`PostListView`

- `ListView`, `paginate_by = 5`.
- Показывает только опубликованные посты.
- Поддерживает фильтрацию по тегу через `tag_id`.
- Использует `select_related("author", "category")` и `prefetch_related("tags")`.

`PostDetailView`

- `DetailView`.
- Показывает опубликованный пост по slug.
- Добавляет `CommentForm` в context.
- Обрабатывает POST комментария только для авторизованного пользователя.
- Использует `select_related("author", "category")` и `prefetch_related("tags", "comments__author")`.

`PostCreateView`

- `LoginRequiredMixin`, `CreateView`.
- Автор поста устанавливается из `request.user`.
- После создания ведет на список постов.

`PostUpdateView`

- `LoginRequiredMixin`, `UserPassesTestMixin`, `UpdateView`.
- Редактировать может только владелец поста.
- Использует `posts/post_form.html`.

`PostDeleteView`

- `LoginRequiredMixin`, `UserPassesTestMixin`, `DeleteView`.
- Удалять может только владелец поста.
- URL переведен на slug.

`CommentDeleteView`

- `LoginRequiredMixin`, `UserPassesTestMixin`, `DeleteView`.
- Удалять комментарий может только автор комментария.
- После удаления возвращает на detail поста.

## 5. Forms

`PostForm`

- Поля: `title`, `content`, `category`, `tags`, `is_published`.
- Серверная логика формы не менялась.

`CommentForm`

- Поле: `content`.
- Автор и пост назначаются во view, не доверяются POST-данным.

`DemoRequestForm`

- Исправлен учебный баг: `clean()` больше не объявлен как `@property`, вызывает `super().clean()`.
- Значение choice для Django приведено к `django`, чтобы существующая проверка `course == "django"` реально работала.

## 6. Authentication / authorization

- Создание поста требует login.
- Редактирование и удаление поста требуют login и ownership check через `UserPassesTestMixin`.
- Добавление комментария требует login; неавторизованный POST отправляется на login через `redirect_to_login`.
- Удаление комментария требует login и ownership check.
- Logout оставлен безопасным: POST-форма с CSRF, не GET-ссылка.

## 7. Comments

Комментарии привязаны к посту через `related_name="comments"`.

В detail UI теперь выводятся:

- username автора или `Deleted user`;
- текст;
- дата создания;
- Delete только для автора комментария.

Комментарии визуально отделены карточками, форма комментария стилизована как часть общего UI.

## 8. Tags / ManyToMany

Теги реализованы через модель `Tag` и поле `Post.tags`.

Текущее состояние:

- теги доступны в форме поста;
- теги показываются на list/detail;
- теги кликабельны;
- клик ведет на `/posts/tag/<tag_id>/`;
- список постов умеет фильтроваться по тегу.

`Tag` также зарегистрирован в Django admin.

## 9. Query optimizations

Уже есть полезные оптимизации:

- list: `select_related("author", "category")`;
- list: `prefetch_related("tags")`;
- detail: `select_related("author", "category")`;
- detail: `prefetch_related("tags", "comments__author")`.

Это закрывает основные N+1 на авторах, категориях, тегах и авторах комментариев.

Потенциальное улучшение позже: заменить `comments__author` на явный `Prefetch` с сортировкой комментариев, если понадобится стабильный порядок и отдельный queryset.

## 10. Templates

Текущее состояние после cleanup:

- `base.html` содержит простую навигацию.
- Для anonymous: `Posts`, `Login`.
- Для authenticated: `Posts`, `Create post`, username, POST `Logout`.
- `post_list.html` показывает title, excerpt, author, category, tags, date, status, View, owner Edit/Delete.
- `post_detail.html` показывает title, author, category, tags, dates, content, owner actions, comments и comment form.
- `post_form.html`, `post_confirm_delete.html`, `comment_confirm_delete.html`, `login.html` используют общий визуальный стиль.
- CSS находится в `core/static/css/main.css`; Bootstrap/Tailwind/JS framework не подключались.

## 11. Найденные проблемы

Исправленные:

- `/` вел на отдельную Home page, хотя текущая стадия проекта должна открывать список постов.
- Навигация содержала устаревшие Home/About/Contacts.
- Были ссылки на slug-based detail route через `pk` в form/delete templates.
- `post_delete` использовал `pk` в пользовательском URL, хотя остальной CRUD уже slug-based.
- В list у владельца `Edit` ранее мог вести не туда в старом состоянии шаблона; сейчас явно ведет на `posts:post_update` со slug.
- `config/urls.py` содержал ошибочный лишний импорт `include` из `xml.etree.ElementInclude`.
- `Tag` не был зарегистрирован в admin.
- `DemoRequestForm.clean` был оформлен как property и ломал POST-валидацию.

Оставшиеся потенциальные проблемы:

- `settings.py` использует SQLite, хотя в заданном контексте указан PostgreSQL.
- Нет automated tests.
- Detail view показывает только опубликованные посты; из-за этого draft-пост после редактирования/создания может быть недоступен по detail URL. Это может быть осознанной учебной логикой, но перед тестами стоит явно определить правило для drafts.
- Нет отдельной страницы профиля/личных draft-постов, поэтому неопубликованные посты трудно найти через UI.
- Slug generation не обрабатывает случай, когда `slugify(title)` вернул пустую строку для полностью не-латинского/символьного заголовка. Для учебного проекта это терпимо, но перед production-style этапом стоит добавить fallback.
- В migrations есть data migration для slug, но PostgreSQL окружение еще не проверялось.

## 12. Что исправлено

- Root `/` теперь делает Django redirect на `/posts/`.
- Home/About/Contacts убраны из navigation и URLconf.
- Удалены неиспользуемые `home`, `about`, `contact` views.
- Удалены неиспользуемые templates `home.html`, `about.html`, `contacts.html`.
- Навигация упрощена под anonymous/authenticated состояния.
- Logout оставлен POST + CSRF.
- Post delete route переведен с `pk` на `slug`.
- Исправлены reverse-ссылки, которые передавали `pk` в slug-based routes.
- Улучшен list/detail UI для категорий, тегов, статусов, actions и комментариев.
- Унифицированы стили форм, delete confirmation, comments, tags и login.
- `Tag` добавлен в admin.
- Исправлен `DemoRequestForm.clean`.
- Создан этот отчет `TECHNICAL_OVERVIEW.md`.

## 13. Что рекомендуется сделать позже

- Добавить automated tests для моделей, URL reverse, permissions, CRUD, comments, tags и pagination.
- Явно решить продуктовую логику drafts: кто может видеть draft detail, где владелец видит свои drafts.
- Перевести настройки БД на PostgreSQL через env-переменные или отдельный local settings слой.
- Добавить fallback для пустого slug.
- Добавить `Meta.ordering` для `Comment` или явный `Prefetch` с сортировкой.
- Добавить admin-настройки для `Tag`, `Category`, возможно `prepopulated_fields` или readonly slug strategy для `Post`.
- Проверить UI в браузере с реальными данными после появления тестовых fixtures.

## 14. Готовность к Stage 17 — Automated tests

Проект готов переходить к Stage 17 — Tests.

Причины:

- `python3 manage.py check` проходит без ошибок.
- `python3 manage.py makemigrations --check --dry-run` показывает `No changes detected`.
- URL/reverse для основных routes проверены.
- Основные slug/ownership/navigation несогласованности исправлены.
- Существующих тестов пока нет: `python3 manage.py test` находит 0 tests.

Рекомендуемый первый набор тестов:

- `Post.get_absolute_url()` возвращает slug URL.
- `/` возвращает redirect на `/posts/`.
- anonymous видит list/detail опубликованных постов.
- anonymous не может create/update/delete/comment.
- owner может update/delete свой пост.
- non-owner не может update/delete чужой пост.
- authenticated user может добавить комментарий.
- author комментария может удалить комментарий.
- tag filter возвращает посты нужного тега.
- pagination работает при количестве постов больше `paginate_by`.
