from django.shortcuts import render

from heart_site.forms import PatientForm

# Create your views here.

# Our new Form page
def index(request):
    if request.method == "POST":
        return render(request, 'home.html', {})
    else:
        context = {'form': PatientForm() }
        return render(request, 'new_form.html', context)