from django.shortcuts import render


def event_list(request):
    context = {
        "page_title": "All Events",
        "events_count": 0,
    }

    return render(request, "events/event_list.html", context)


def event_about(request):
    return render(request, "events/event_about.html")


def event_detail(request, slug):
    return render(
        request,
        "events/event_detail.html",
        {"slug": slug},
    )
