from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from reservationsApp.models import Reservation
from loansApp.models import Loan
from articlesApp.models import Article
from spacesApp.models import Space
from mainApp.models import User, Item
from datetime import datetime, timedelta, date
import pytz
from django.utils.timezone import localtime
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.conf import settings


@login_required
def user_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'user_panel.html', context)


@login_required
def items_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    articles = Article.objects.all()
    spaces = Space.objects.all()
    context = {
        'articles': articles,
        'spaces': spaces
    }
    return render(request, 'items_panel.html', context)


@login_required
def actions_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    try:
        current_date = request.GET["date"]
    except:
        current_date = date.today().strftime("%Y-%m-%d")
    reservations = Reservation.objects.exclude(state='R').order_by('starting_date_time')
    spaces = Space.objects.all()
    coloresP = ['rgba(102,153,102,0.7)', 'rgba(153,102,102,0.7)', 'rgba(102,102,153,0.7)', 'rgba(153,127,102,0.5)',
                'rgba(153,102,153,0.7)', 'rgba(102,153,153,0.7)']
    coloresA = ['rgba(63,191,63,0.9)', 'rgba(191,63,63,0.9)', 'rgba(63,63,191,0.9)', 'rgba(191,127,63,0.9)',
                'rgba(191,63,191,0.9)', 'rgba(63,191,191,0.9)']
    spaces_list = []
    reservations_list = []
    space_filter = []
    i = 0
    for s in spaces:
        espacio_dic = {
            "id": s.id,
            "nombre": s.name,
            "estado": s.state,
            "colorP": coloresP[i],
            "colorA": coloresA[i]
        }
        i = i + 1
        spaces_list.append(espacio_dic)

    if request.method == 'POST':
        for sid in request.POST.getlist('optcheck[]'):
            space_filter.append(int(sid))
    else:
        for s in spaces:
            space_filter.append(int(s.id))

    for r in reservations:
        if r.space.id in space_filter:
            for s in spaces_list:
                if r.space.id == s["id"]:
                    title = str(r.space.name) + " - " + str(r.user.get_full_name())
                    color = s["colorA"]
                    if r.state == 'P':
                        title = title + " (pendiente)"
                        color = s["colorP"]
                    reserva_dic = {
                        "title": title,
                        "start": r.starting_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "end": r.ending_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "color": color,
                        "estado": r.state
                    }
                    reservations_list.append(reserva_dic)

    actual_date = datetime.now()
    pending_reservations = Reservation.objects.filter(state='P').order_by('starting_date_time')

    try:
        if request.method == 'POST':
            if request.POST["loan_action"] == 'aceptar':
                some_loans = Loan.objects.filter(id__in=request.POST.getlist("loan_selected"))
                for a_loan in some_loans:
                    a_loan.state = 'A'
                    a_loan.save()
            elif request.POST["loan_action"] == 'rechazar':
                some_loans = Loan.objects.filter(id__in=request.POST.getlist("loan_selected"))
                for a_loan in some_loans:
                    a_loan.state = 'R'
                    a_loan.save()
            elif request.POST["loan_action"] == 'entregado':
                some_loans = Loan.objects.filter(id__in=request.POST.getlist("loan_selected"))
                for a_loan in some_loans:
                    article = Article.objects.get(id=a_loan.article.id)
                    article.state = 'D'
                    article.save()
            elif request.POST["loan_action"] == 'perdido':
                some_loans = Loan.objects.filter(id__in=request.POST.getlist("loan_selected"))
                for a_loan in some_loans:
                    article = Article.objects.get(id=a_loan.article.id)
                    article.state = 'L'
                    article.save()
            elif request.POST["loan_action"] == 'encontrado':
                some_loans = Loan.objects.filter(id__in=request.POST.getlist("loan_selected"))
                for a_loan in some_loans:
                    article = Article.objects.get(id=a_loan.article.id)
                    article.state = 'D'
                    article.save()
    except:
        redirect('/admin/actions-panel/')
    loans = Loan.objects.filter(ending_date_time__gt=actual_date,
                                state='A').order_by('starting_date_time')
    loan_filter = 'activos'
    try:
        if request.method == "POST":
            if request.POST["filter"] == 'activos':
                loans = Loan.objects.filter(ending_date_time__gt=actual_date,
                                            state='A').order_by('starting_date_time')
                loan_filter = 'activos'
            elif request.POST["filter"] == 'entregados':
                loans = Loan.objects.filter(ending_date_time__lt=actual_date, state='A',
                                            article__state='D').order_by('starting_date_time')
                loan_filter = 'entregados'
            elif request.POST["filter"] == 'pendientes':
                loans = Loan.objects.filter(starting_date_time__gt=actual_date,
                                            state='P').order_by('starting_date_time')
                loan_filter = 'pendientes'
            elif request.POST["filter"] == 'caducados':
                loans = Loan.objects.filter(ending_date_time__lt=actual_date, state='A',
                                            article__state='P').order_by('starting_date_time')
                loan_filter = 'caducados'
            elif request.POST["filter"] == 'perdidos':
                loans = Loan.objects.filter(ending_date_time__lt=actual_date, state='A',
                                            article__state='L').order_by('starting_date_time')
                loan_filter = 'perdidos'
    except:
        loans = Loan.objects.filter(ending_date_time__lt=actual_date, state='A',
                                    article__state='P').order_by('starting_date_time')
        loan_filter = 'activos'

    context = {
        'reservations_query': pending_reservations,
        'loans': loans,
        'current_date': current_date,
        'reservations': reservations_list,
        'spacesList': spaces_list,
        'spacesFilter': space_filter,
        'request': request,
        'loan_filter': loan_filter
    }
    return render(request, 'actions_panel.html', context)


@login_required
def add_item(request):
    if not request.user.is_staff:
        return redirect('/')
    else:
        try:
            return render(request, 'add_item.html')#, context)
        except:
            return redirect('/')


def add_new_item(request):

    context = {'error_message': '', }


    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        try:
            image = request.FILES['image']
            tmp_file = os.path.join('mainApp/static/mainApp/img/items', image.name)
            path = default_storage.save(tmp_file, ContentFile(image.read()))
        except:
            path = 'img/items/default_article.jpg'

        new_item = Article(name=name, description=description, image = path, state='D')
        new_item.save()
        messages.success(request, 'Articulo agregado correctamente.')
    return redirect('/admin/items-panel/')
