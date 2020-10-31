from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, AddressForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form1 = UserRegistrationForm(request.POST)
        form2 = AddressForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            details = form2.save(commit=False)
            details.user = user
            details.save()
            messages.success(request, 'Your account has been created. You are requested to Log In')
            return redirect('login')
    else:
        form1 = UserRegistrationForm()
        form2 = AddressForm()
    return render(request, 'Users/register.html', {'form1': form1, 'form2': form2})