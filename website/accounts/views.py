import random
import string

from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.db import transaction, IntegrityError

from .models import AccountType, Order, Account
from .forms import OrderForm
from .funcs import generator, CountException, check_status
from website import settings


def main(request):
    types = AccountType.objects.all()
    return render(request, 'main.html', {'accounts': types})


def base_form(request, type_):
    form = OrderForm(request.POST or None)
    try:
        del request.session['id']
    except KeyError:
        pass

    if form.is_valid():
        try:
            data = form.cleaned_data
            if data['count'] > AccountType.objects.get(name=type_).get_count():
                raise CountException

            order = Order(email=data['email'],
                          count=data['count'],
                          type=get_object_or_404(AccountType, name=type_))

            order.pay_comment = generator(size=8, chars=string.digits)
            order.save()
            request.session['id'] = order.id

            return redirect(reverse('accounts:form_confirm', args=[type_, generator(size=25)]))
        except CountException:
            messages.add_message(request, messages.INFO, 'Недостаточно аккаунтов.')

    return render(request, 'form.html', {'type': type_, 'form': form})


def form_confirm(request, type_, code):
    order = get_object_or_404(Order, pk=request.session.get('id', None))

    if request.POST:
        if check_status(order):  # Проверка оплаты
            order.paid = True
            order.download_code = generator(size=20)
            order.save()

    qiwi_link = 'https://qiwi.com/payment/form/99?amountFraction=0&currency=RUB&extra%5B%27account%27%5D={}' \
                '&extra%5B%27comment%27%5D={}&amountInteger={}'.format(settings.base_num,
                                                                       order.pay_comment,
                                                                       order.total_price)
    return render(request, 'form_confirm.html', {'order': order,
                                                 'number': settings.base_num,
                                                 'qiwi_link': qiwi_link})


def txt_download(request, type_, d_link):
    local_type = AccountType.objects.get(name=type_)
    order = get_object_or_404(Order, pk=request.session.get('id', None))

    if d_link == order.download_code and local_type.get_count() > order.count:
        accounts = []
        if order.complete:
            accs = Account.objects.filter(order=order)
            accounts = ['%s:%s' % (a.login, a.password) for a in accs]
        else:
            for a in Account.objects.filter(type=local_type, is_active=True)[:order.count]:
                try:
                    with transaction.atomic():
                        a.order = order
                        a.is_active = False
                        a.save()
                        accounts += ['%s:%s' % (a.login, a.password)]
                except IntegrityError:
                    raise Http404('Ошибка во время запроса, свяжитесь с администрацией.')

            order.complete = True
            order.save()

        filename = 'accounts_{}.txt'.format(generator(size=15))
        content = '\r\n'.join(accounts)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
    else:
        raise Http404('Неверный адрес или недостаточно аккаунтов')


# TODO: Удалить представление после отладки
# def add(request):
#     types = ['Bitcointalk', 'Gmail', 'vk', 'test']
#     for i in range(10):
#         a = Account(type=AccountType.objects.get(name=random.choice(types)),
#                     login=generator(size=8) + '@gmail.com',
#                     password=generator(size=12))
#         a.save()
#     return redirect(reverse('accounts:main', args=[]))
