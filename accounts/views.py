# вьюха регистрации нового юзера
# логин/логаут используем встроенные из django.contrib.auth

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # сразу логиним юзера после регистрации чтобы два раза не вводил пароль
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    # накидываем bootstrap-класс на поля чтобы красиво выглядели
    for field in form.fields.values():
        field.widget.attrs.setdefault('class', 'form-control')
    return render(request, 'accounts/register.html', {'form': form})
