from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
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
