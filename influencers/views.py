from django.shortcuts import render
from django.http import HttpResponse
from .models import influencers

# Create your views here.
def home(request):
    #return HttpResponse('<h1>Welcome To Home Page</h1>')
    #return render(request, 'home.html')
    return render(request, 'home.html',{'name':'HireFlow'})
    searchTerm=request.GET.get('searchTerm')
    influencers=influencers.objects.all()
    return render(request, 'home.html',{'searchTerm':searchTerm,'influencers':influencers})
def about(request):
    #return HttpResponse('<h1>Welcome To About</h1>')
    return render(request, 'about.html')