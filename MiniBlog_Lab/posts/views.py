from django.shortcuts import render


def home(request):
    context = {
        'page_title': 'Home Page',
        'student_name': 'Dima',
    }

    return render(
        request=request,
        template_name='posts/home.html',
        context=context
    )
