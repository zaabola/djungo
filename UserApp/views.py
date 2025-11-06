from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import logout
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'UserApp/register.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')
