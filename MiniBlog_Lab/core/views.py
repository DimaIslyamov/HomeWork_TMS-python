from django.shortcuts import render

def home(request):
    context = {
        'page_title': 'Home Page',
        'student_name': 'Dima',
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contacts.html')