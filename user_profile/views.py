from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView
from user_profile.forms import RegistrationForm, EditForm


# TODO Можно перейти по ссылке выхода, убрать ниже код
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


class UpdateViewProfile(UpdateView):
    model = User
    form_class = EditForm
    template_name = 'user_profile/edit_profile.html'
    success_url = reverse_lazy('edit')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Данные были успешно изменены')
        return super().form_valid(form)
