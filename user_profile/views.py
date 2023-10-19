from django.shortcuts import render

from user_profile.forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'user_profile/register_done.html', {'new_user': new_user})
    else:
        form = RegistrationForm()
    return render(request, 'user_profile/register.html', {'user_form': form})
