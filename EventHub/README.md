# EventHub

EventHub is a Django web application for creating, publishing, managing, and joining events.

The project was built as a learning and portfolio project to practice Django architecture, ORM, authentication, permissions, forms, service-layer logic, testing, PostgreSQL integration, and generic relations.

## Features

### Public events

* Browse published events
* View event details
* Search events by title and description
* Filter events by category
* Pagination
* View organizer and category information

### Authentication

* Login and logout
* Authentication-based access control
* Organizer-only actions
* Backend permission checks for direct URL access

### Event management

Authenticated users can:

* Create events
* Edit their own events
* Delete their own events
* Save events as drafts
* Publish events
* View their own events in the organizer dashboard
* Filter dashboard events by published/draft status

### Event registrations

Users can:

* Join published events
* Leave events
* View events they are registered for

Registration business logic is separated into a service layer.

Organizers cannot register for their own events.

### Sessions

Event organizers can manage sessions related to their events using Django formsets.

Each session belongs to a specific event.

### Announcements

Organizers can:

* View announcements for their events
* Create announcements
* Update announcements
* Delete announcements

Ownership is validated through:

```text
Announcement -> Event -> Organizer
```

### Event materials

Events support polymorphic materials through Django ContentTypes and `GenericForeignKey`.

Supported material types:

* Text
* File
* Image
* Video

Material forms use explicit field allowlists instead of exposing all model fields.

## Tech Stack

* Python
* Django
* PostgreSQL
* Django ORM
* python-dotenv
* HTML / Django Templates
* CSS
* Git / GitHub

## Project Structure

```text
EventHub/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── events/
│   ├── migrations/
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   ├── test_forms.py
│   │   ├── test_services.py
│   │   └── test_permissions.py
│   │
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
│
├── templates/
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## Main Models

The project contains the following main domain models:

* `Category`
* `Event`
* `Session`
* `Announcement`
* `EventMaterial`
* `Text`
* `File`
* `Image`
* `Video`

`Event` is connected to:

* an organizer through `ForeignKey`
* a category through `ForeignKey`
* participants through `ManyToManyField`
* sessions through reverse `ForeignKey`
* announcements through reverse `ForeignKey`
* materials through `EventMaterial`

## ORM Optimization

The project uses Django ORM optimization techniques where appropriate.

Examples:

```python
select_related("category", "organizer")
```

is used for single-object relations such as `ForeignKey`.

The project also explores:

* `prefetch_related()`
* `exists()`
* `count()`
* `annotate()`
* `Count`
* QuerySet laziness
* N+1 query detection

SQL query logging was used during development to identify and reproduce N+1 problems.

## Security and Permissions

Backend authorization is implemented for organizer-only actions.

Examples include:

* users cannot update another user's event
* users cannot delete another user's event
* users cannot manage sessions of another user's event
* users cannot create announcements for another user's event
* users cannot modify or delete announcements belonging to another organizer
* draft events are not publicly accessible
* registration actions work only with published events
* join and leave operations require POST requests

Organizer ownership is assigned server-side and cannot be changed through `EventForm`.

## Tests

The project contains a dedicated test package:

```text
events/tests/
```

Tests cover:

* models
* model relationships
* `__str__`
* `get_absolute_url`
* unique constraints
* protected deletion
* public views
* drafts
* search
* filtering
* pagination
* organizer permissions
* direct URL access
* forms and validation
* services
* registration
* session management
* announcements
* event materials
* authentication and authorization

Run all EventHub tests with:

```bash
python manage.py test events
```

Run Django system checks with:

```bash
python manage.py check
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd EventHub
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it.

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create `.env` in the project root.

You can copy the provided example:

```bash
cp .env.example .env
```

Required variables:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=eventhub_db
POSTGRES_USER=eventhub_user
POSTGRES_PASSWORD=change-me
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Do not commit the real `.env` file.

## PostgreSQL Setup

Create a PostgreSQL database and user matching the values from `.env`.

Example:

```sql
CREATE DATABASE eventhub_db;

CREATE USER eventhub_user
WITH PASSWORD 'your-password';

GRANT ALL PRIVILEGES
ON DATABASE eventhub_db
TO eventhub_user;
```

Depending on your PostgreSQL configuration, you may also need to grant permissions on the `public` schema.

## Database Migrations

Apply migrations:

```bash
python manage.py migrate
```

## Create an Admin User

```bash
python manage.py createsuperuser
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

## Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Architecture Notes

The project intentionally uses a combination of:

* class-based views for CRUD, list, and detail pages
* function-based views for small POST actions
* forms for input validation
* services for registration business logic
* Django mixins for authentication and authorization
* Django ContentTypes for polymorphic event materials

The architecture is intentionally kept relatively simple because the project is designed as a junior-level Django portfolio project rather than an enterprise application.

## Key Learning Topics

This project was used to practice:

* Django project structure
* models and migrations
* PostgreSQL
* Django ORM
* relationships
* authentication
* authorization
* `LoginRequiredMixin`
* `UserPassesTestMixin`
* ModelForms
* validation
* formsets
* services
* GenericForeignKey
* pagination
* search and filtering
* query optimization
* N+1 problems
* automated testing
* environment configuration
* Git repository hygiene

## Status

The core EventHub learning roadmap is complete.

The project includes:

* public catalog
* organizer dashboard
* event CRUD
* sessions
* registrations
* announcements
* polymorphic materials
* permissions
* ORM optimization
* automated tests
* environment-based configuration
* PostgreSQL integration

## License

This project was created for educational and portfolio purposes.
