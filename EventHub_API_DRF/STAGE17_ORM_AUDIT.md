# Stage 17 — ORM Audit

## 1. Current Models & Relationships

Source files:

- `api/models.py`
- `accounts/models.py`

Current models found:

- `Event` — `api.models.Event`
- `Category` — `api.models.Category`
- `Session` — `api.models.Session`
- `Registration` — `api.models.Registration`
- `User` — `accounts.models.User`

Event relationships:

| Relationship | Model field location | Type | Direction from `Event` | `related_name` | ORM optimization tool |
| --- | --- | --- | --- | --- | --- |
| `Event -> organizer` | `Event.organizer` | `ForeignKey` to `settings.AUTH_USER_MODEL` | forward FK | `organized_events` on `User` | `select_related("organizer")` only if code reads `event.organizer` fields |
| `Event -> category` | `Event.category` | `ForeignKey` to `Category` | forward FK | `events` on `Category` | `select_related("category")` only if code reads `event.category` fields |
| `Event -> sessions` | `Session.event` | reverse `ForeignKey` from `Session` to `Event` | reverse FK / one-to-many | `sessions` on `Event` | `prefetch_related("sessions")` |
| `Event -> registrations` | `Registration.event` | reverse `ForeignKey` from `Registration` to `Event` | reverse FK / one-to-many | `registrations` on `Event` | `prefetch_related("registrations")` only if events serialize or iterate registrations |

Additional `Registration` relationship:

| Relationship | Model field location | Type | Direction from `Registration` | `related_name` | ORM optimization tool |
| --- | --- | --- | --- | --- | --- |
| `Registration -> attendee` | `Registration.attendee` | `ForeignKey` to `settings.AUTH_USER_MODEL` | forward FK | `registrations` on `User` | `select_related("attendee")` only when registration output needs attendee fields |

Important detail: `Event.__str__()` returns `title`, so printing an `Event` itself does not load `organizer`, `category`, `sessions`, or `registrations`. `Registration.__str__()` uses both `attendee` and `event`, so bulk display of registrations can create FK-related extra queries, but this is not currently part of `GET /api/events/`.

## 2. Current EventSerializer

Source: `api/serializers.py`

Current serializers:

- `CategorySerializer` exists, but it is not used inside `EventSerializer`.
- `SessionSerializer` serializes `id`, `title`, `description`, `starts_at`.
- `EventSerializer` defines one explicit nested field:

```python
class EventSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Event
        fields = "__all__"
```

Current `EventSerializer` behavior:

- `sessions` is a nested reverse relationship. DRF will read `event.sessions.all()` for each serialized event unless sessions are prefetched.
- `organizer` is not nested. Because `fields = "__all__"` and no explicit field is declared, DRF represents it as a primary key related field. It can use `event.organizer_id`; it does not need to fetch the `User` object for normal serialization.
- `category` is not nested. DRF represents it as a primary key related field and can use `event.category_id`; it does not need to fetch the `Category` object for normal serialization.
- `registrations` is not present in the serializer output.
- No `SerializerMethodField` is present.
- No serializer code currently computes `registrations.count()`, `sessions.count()`, organizer names, category names, or other related-object properties.

Conclusion: the real serializer-driven N+1 candidate in the current `EventSerializer` is `sessions`, not `organizer`, `category`, or `registrations`.

## 3. Current EventViewSet / get_queryset()

Source: `api/views.py`

`EventViewSet`:

- `serializer_class = EventSerializer`
- `pagination_class = EventPagination`
- filter backends:
  - `DjangoFilterBackend`
  - `SearchFilter`
  - `OrderingFilter`
- `filterset_fields = ["category", "is_published"]`
- `search_fields = ["title", "description"]`
- `ordering_fields = ["starts_at", "title"]`

Current dynamic access rules in `get_queryset()`:

| Action | User type | Queryset |
| --- | --- | --- |
| `list`, `retrieve` | guest | `Event.objects.filter(is_published=True)` |
| `list`, `retrieve` | attendee | `Event.objects.filter(is_published=True)` |
| `list`, `retrieve` | organizer | `Event.objects.filter(organizer=user)` |
| `register` | attendee permission required by `get_permissions()` | `Event.objects.filter(is_published=True)` |
| `update`, `partial_update`, `destroy` | organizer owner flow | `Event.objects.filter(organizer=user)` |
| fallback | any | `Event.objects.none()` |

Current custom action:

```python
@action(detail=True, methods=["post", "delete"])
def register(self, request, pk=None):
    event = self.get_object()
```

`register` calls service-layer functions:

- `register_for_event(user=request.user, event=event)`
- `cancel_registration(user=request.user, event=event)`

Current pagination:

- `EventPagination.page_size = 2`
- `page_size_query_param = "page_size"`
- `max_page_size = 100`

This matters for N+1 measurement: by default `GET /api/events/` will show only 2 events per page, so the N+1 pattern is easier to demonstrate with `?page_size=10` or another value greater than the number of test events.

Optimization compatibility note: adding `.prefetch_related("sessions")` to the event querysets must preserve each branch's filtering rules. It should be applied after choosing the base queryset, not by replacing the role/action conditions.

## 4. Existing ORM Optimizations

Search results across the project:

- `select_related()` — not used.
- `prefetch_related()` — not used.
- `Prefetch()` — not used.
- `annotate()` — not used.
- `Count()` — not used.
- `Django Debug Toolbar` — not installed in `INSTALLED_APPS`.
- `django-debug-toolbar` package — not present in `.venv/bin/pip freeze`.
- SQL query counting tests/tools — no `assertNumQueries`, `CaptureQueriesContext`, or `connection.queries` usage found.

Existing transaction/concurrency ORM usage:

- `api/services.py` uses `transaction.atomic()`.
- `api/services.py` uses `Event.objects.select_for_update().get(pk=event.pk)` inside `register_for_event()`.

`select_for_update()` is not an eager-loading optimization. It is a locking/concurrency tool and should be treated separately from Stage 17 read-query optimization.

## 5. Potential N+1 Problems

### Problem 1: Nested sessions in EventSerializer

- location: `api/serializers.py`
- class: `EventSerializer`
- code area: `sessions = SessionSerializer(many=True, read_only=True)`
- relationship: `Event -> sessions`
- relationship type: reverse `ForeignKey`; `Session.event` owns the FK, `related_name="sessions"`
- reason: serializing a list of events asks DRF to serialize `sessions` for each `Event`. Without prefetching, each event instance can trigger a separate query for its sessions.
- expected query pattern without prefetch:
  - 1 query for the event page/list
  - N queries for `sessions`, one per serialized event
  - plus the normal pagination count query on paginated list endpoints
- recommended ORM tool: `prefetch_related("sessions")`
- best place to add later: the `EventViewSet.get_queryset()` branch or shared base queryset used by `list` and `retrieve`, after the access-control queryset has been selected.

This is the strongest Stage 17 demo in the current codebase.

### Problem 2: Object permission may load organizer on write actions

- location: `api/permissions.py`
- class: `IsEventOwner`
- code area: `return obj.organizer == request.user`
- relationship: `Event -> organizer`
- relationship type: forward `ForeignKey`
- reason: comparing `obj.organizer` can load the organizer object if it was not already selected. This is not a list-endpoint N+1 problem, because object permissions run against a single object for update/partial_update/destroy.
- expected query pattern without select:
  - 1 query to fetch the target event
  - possibly 1 extra query to fetch `organizer`
- recommended ORM tool: either compare `obj.organizer_id == request.user.id` in permission code, or use `select_related("organizer")` for write-action querysets. This is not the first Stage 17 optimization because the current serializer N+1 is clearer and affects list output.
- best place to add later if choosing eager loading: write-action branch in `EventViewSet.get_queryset()`.

### Problem 3: Registration service count is an extra query, but not N+1 for events list

- location: `api/services.py`
- function: `register_for_event`
- code area: `registrations_count = locked_event.registrations.count()`
- relationship: `Event -> registrations`
- relationship type: reverse `ForeignKey`; `Registration.event` owns the FK, `related_name="registrations"`
- reason: registration capacity validation runs a count query for the one locked event. This is expected for the current custom action.
- expected query pattern:
  - `get_object()` fetches the event for the register action.
  - service fetches and locks the same event with `select_for_update()`.
  - service checks existing registration with `.exists()`.
  - service counts registrations with `.count()`.
  - service creates a registration when valid.
- recommended ORM tool: not `prefetch_related("registrations")` for `GET /api/events/`. For the custom action, the count is intentional and per single event, not an event-list N+1 pattern.

## 6. select_related Candidates

### `select_related("organizer")`

Current status: not needed for `GET /api/events/` serialization.

Reason: `EventSerializer` currently outputs `organizer` as a primary key field, so DRF can read `organizer_id` directly. There is no nested organizer serializer and no organizer username/email field in the event output.

Possible future use:

- If `EventSerializer` later exposes organizer details such as username/email.
- If write-object permission remains `obj.organizer == request.user` and the project chooses eager loading over changing the permission comparison.

### `select_related("category")`

Current status: not needed for `GET /api/events/` serialization.

Reason: `EventSerializer` currently outputs `category` as a primary key field, so DRF can read `category_id` directly. `CategorySerializer` exists but is not nested into `EventSerializer`.

Possible future use:

- If `EventSerializer` later exposes category details such as name/slug.
- If a custom field or method starts reading `event.category`.

## 7. prefetch_related Candidates

### `prefetch_related("sessions")`

Current status: recommended first real optimization after measuring.

Reason: `EventSerializer` currently serializes nested sessions for every event. This is a direct reverse-FK N+1 candidate.

Best endpoint for demonstration:

- `GET /api/events/?page_size=10`

Why this endpoint:

- It uses `EventSerializer`.
- It returns multiple events.
- It includes nested `sessions`.
- It is paginated, so query-count changes are easy to compare while keeping the response size controlled.

Expected before/after shape:

- Before: event list query + one sessions query per event in the page.
- After: event list query + one combined sessions prefetch query for all events in the page.

### `prefetch_related("registrations")`

Current status: not recommended for `GET /api/events/` right now.

Reason: `EventSerializer` does not serialize registrations, registration counts, or attendee details. Prefetching registrations on the event list would add memory and SQL work without serving current response data.

Possible future use:

- If event output later includes nested registrations.
- If event output later includes registration counts and the project chooses prefetch/count-in-Python for teaching purposes.
- If an endpoint is added for event registration lists.

## 8. Registration Analysis

`Registration` is currently used in:

- `api/models.py` as a model with `event`, `attendee`, and `created_at`.
- `api/services.py` in `register_for_event()`.
- `api/services.py` in `cancel_registration()`.

`Registration` is not currently used in:

- `EventSerializer`
- `SessionSerializer`
- `GET /api/events/` response body
- `GET /api/events/{id}/` response body

Can `Registration` create N+1 now?

- For `GET /api/events/`: no, because the serializer does not access `event.registrations`.
- For `GET /api/events/{id}/`: no, for the same reason.
- For `POST /api/events/{id}/register/`: no list-style N+1. The action works with one event.

Current register action query considerations:

- `EventViewSet.register()` calls `self.get_object()`.
- `register_for_event()` then fetches and locks the same event again using `select_for_update()`.
- It checks duplicate registration with `.exists()`.
- It counts registrations with `locked_event.registrations.count()`.

This is relevant for service-layer query count learning, but it is not the first ORM optimization target for Stage 17 because it is not caused by list serialization.

## 9. How to Measure Queries

Recommended lightweight approach for this project before adding Debug Toolbar:

1. Create controlled test data:
   - several published events;
   - each event has 2-3 sessions;
   - use `page_size` large enough to include several events on one page.

2. Measure `GET /api/events/?page_size=10` as guest:
   - this follows the guest branch: `Event.objects.filter(is_published=True)`;
   - this avoids organizer-only visibility while demonstrating nested session loading.

3. Use Django test utilities:
   - `django.test.utils.CaptureQueriesContext`
   - `django.db.connection`
   - DRF `APIClient`

4. Expected current query pattern for a paginated list:
   - one count query for pagination;
   - one event-page query;
   - one sessions query per event on that page.

5. Repeat after exactly one optimization and compare query counts.

Optional later tool:

- Add Django Debug Toolbar only as a separate learning step if desired.
- It is not currently installed or configured, so adding it should be treated as its own Stage 17 exercise, not mixed with the first ORM code change.

## 10. Recommended Stage 17 Learning Sequence

Step 1 -> Measure current query count for `GET /api/events/?page_size=10`.

Use guest access and controlled published events with sessions. Record the exact SQL count and identify the repeated `Session` queries.

Step 2 -> Reproduce and explain the N+1.

Confirm that the number of session queries grows with the number of events in the page. Example pattern: 5 events in response means 5 extra session queries.

Step 3 -> Add only one optimization: prefetch sessions.

Apply `prefetch_related("sessions")` only to the event queryset used for read responses that serialize nested sessions. Preserve all existing dynamic access rules.

Step 4 -> Measure `GET /api/events/?page_size=10` again.

Expected result: repeated per-event session queries collapse into one prefetch query.

Step 5 -> Measure `GET /api/events/{id}/`.

Decide whether prefetching sessions is useful for retrieve too. For a single event, it may not reduce query count meaningfully, but it can keep serializer behavior consistent.

Step 6 -> Check that `organizer` and `category` still do not need `select_related()`.

Do this by confirming the response still contains ids only and no SQL reads from `accounts_user` or `api_category` are triggered by serialization.

Step 7 -> Separately inspect write actions.

Measure update/delete object-permission behavior if desired. Decide whether to optimize `obj.organizer` access or change the permission comparison. Do not mix this with the sessions prefetch exercise.

Step 8 -> Separately inspect `register`.

Measure `POST /api/events/{id}/register/` and document the intentional queries: get object, lock event, duplicate check, count registrations, create registration. Do not use `prefetch_related("registrations")` for the event list unless registrations become part of the event response.

## 11. Exact First Change Recommended

Do not change application code first.

The first change after studying this report should be a query-count measurement test or temporary measurement script for:

```text
GET /api/events/?page_size=10
```

The measurement should create multiple published events with sessions and record the current query count before adding any `select_related()` or `prefetch_related()`.
