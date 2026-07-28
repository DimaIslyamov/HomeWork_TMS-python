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
    result = None

    if request.method == "POST":
        form = DemoRequestForm(request.POST)

        if form.is_valid():
            result = form.cleaned_data
    else:
        form = DemoRequestForm()

    context = {
        "form": form,
        "result": result,
    }

    return render(
        request,
        "core/request_demo.html",
        context,
    )

