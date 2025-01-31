from django.http import HttpResponse



def home(request):
    return HttpResponse("<h1>Welcome to the Book Donation App!</h1>")