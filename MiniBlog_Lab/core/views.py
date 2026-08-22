from django.shortcuts import render

from core.forms import DemoRequestForm


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
