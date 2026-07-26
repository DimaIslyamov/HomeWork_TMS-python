from django.http import HttpResponse
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


def request_demo(request):
    student = request.GET.get('student')
    course = request.GET.get('course')

    return HttpResponse(
        f"""
        <h2>Request Demo</h2>
        Student: {student}<br>
        Course: {course}
        """
    )
