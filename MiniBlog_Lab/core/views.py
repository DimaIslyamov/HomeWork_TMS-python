from django.shortcuts import render

from core.forms import DemoRequestForm


def home(request):
    context = {
        'page_title': 'Home Page',
        'student_name': 'Dima',
    }
    return render(
        request=request,
        template_name='core/home.html',
        context=context
    )


def about(request):
    return render(
        request=request,
        template_name='core/about.html'
    )


def contact(request):
    return render(
        request=request,
        template_name='core/contacts.html'
    )


def request_demo(request):
    student_name = None
    course_name = None

    if request.method == "POST":
        form = DemoRequestForm(request.POST)

        if form.is_valid():
            student_name = form.cleaned_data["student"]
            course_name = form.cleaned_data["course"]
    else:
        form = DemoRequestForm()

    context = {
        "form": form,
        "student_name": student_name,
        "course_name": course_name,
    }

    return render(
        request=request,
        template_name="core/request_demo.html",
        context=context,
    )
