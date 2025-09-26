from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from .utils import send_mailing
from django.views.decorators.cache import cache_page


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


@cache_page(60 * 15)
@login_required
def index(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='running').count()
    unique_clients = Client.objects.count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
    }
    return render(request, 'index.html', context)


@login_required
def client_list(request):
    if is_manager(request.user):
        clients = Client.objects.all()
    else:
        clients = Client.objects.filter(owner=request.user)
    return render(request, 'clients/client_list.html', {'clients': clients})


@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user
            client.save()
            messages.success(request, 'Клиент успешно добавлен.')
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form})


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not is_manager(request.user) and client.owner != request.user:
        messages.error(request, 'У вас нет прав редактировать этого клиента.')
        return redirect('client_list')

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клиент успешно обновлён.')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/client_form.html', {'form': form})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not is_manager(request.user) and client.owner != request.user:
        messages.error(request, 'У вас нет прав удалять этого клиента.')
        return redirect('client_list')

    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Клиент успешно удалён.')
        return redirect('client_list')
    return render(request, 'clients/client_confirm_delete.html', {'client': client})


@login_required
def message_list(request):
    messages_list = Message.objects.all()
    return render(request, 'messages/message_list.html', {'messages': messages_list})


@login_required
def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение успешно добавлено.')
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'messages/message_form.html', {'form': form})


@login_required
def message_update(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение успешно обновлено.')
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    return render(request, 'messages/message_form.html', {'form': form})


@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Сообщение успешно удалено.')
        return redirect('message_list')
    return render(request, 'messages/message_confirm_delete.html', {'message': message})


@login_required
def mailing_list(request):
    if is_manager(request.user):
        mailings = Mailing.objects.all()
    else:
        mailings = Mailing.objects.filter(owner=request.user)
    return render(request, 'mailings/mailing_list.html', {'mailings': mailings})


@login_required
def mailing_create(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user
            mailing.save()
            form.save_m2m()
            messages.success(request, 'Рассылка успешно создана.')
            return redirect('mailing_list')
    else:
        form = MailingForm()
    return render(request, 'mailings/mailing_form.html', {'form': form})


@login_required
def mailing_update(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if not is_manager(request.user) and mailing.owner != request.user:
        messages.error(request, 'У вас нет прав редактировать эту рассылку.')
        return redirect('mailing_list')

    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Рассылка успешно обновлена.')
            return redirect('mailing_list')
    else:
        form = MailingForm(instance=mailing)
    return render(request, 'mailings/mailing_form.html', {'form': form})


@login_required
def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if not is_manager(request.user) and mailing.owner != request.user:
        messages.error(request, 'У вас нет прав удалять эту рассылку.')
        return redirect('mailing_list')

    if request.method == 'POST':
        mailing.delete()
        messages.success(request, 'Рассылка успешно удалена.')
        return redirect('mailing_list')
    return render(request, 'mailings/mailing_confirm_delete.html', {'mailing': mailing})


@login_required
def mailing_send(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if not is_manager(request.user) and mailing.owner != request.user:
        messages.error(request, 'У вас нет прав отправлять эту рассылку.')
        return redirect('mailing_list')

    try:
        send_mailing(mailing.id)
        messages.success(request, f'Рассылка #{mailing.id} успешно отправлена.')
    except Exception as e:
        messages.error(request, f'Ошибка при отправке рассылки: {e}')
    return redirect('mailing_list')


@login_required
@user_passes_test(is_manager)
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


@login_required
@user_passes_test(is_manager)
def user_toggle_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, 'Нельзя блокировать суперпользователя.')
        return redirect('user_list')
    user.is_active = not user.is_active
    user.save()
    status = 'активирован' if user.is_active else 'заблокирован'
    messages.success(request, f'Пользователь {user.username} {status}.')
    return redirect('user_list')


@login_required
def user_statistics(request):
    user = request.user

    success_count = MailingAttempt.objects.filter(
        mailing__owner=user,
        status='success'
    ).count()

    failed_count = MailingAttempt.objects.filter(
        mailing__owner=user,
        status='failed'
    ).count()

    total_sent = success_count + failed_count

    context = {
        'success_count': success_count,
        'failed_count': failed_count,
        'total_sent': total_sent,
    }
    return render(request, 'statistics/user_statistics.html', context)
