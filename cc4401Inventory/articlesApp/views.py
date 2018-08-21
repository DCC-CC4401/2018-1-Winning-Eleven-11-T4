from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from articlesApp.models import Article
from loansApp.models import Loan
from django.db import models
from datetime import datetime, timedelta

import random, os
import pytz
from django.contrib import messages

from utils.time_utils import to_datetime, is_non_workday




@login_required
def article_data(request, article_id):
    if request.user.is_staff:
        return redirect("/article/"+str(article_id)+"/edit")


    try:
        article = Article.objects.get(id=article_id)

        last_loans = Loan.objects.filter(article=article#,
                                         #ending_date_time__lt=datetime.now(tz=pytz.utc)
                                         ).order_by('-ending_date_time')[:10]

        loan_list = list()
        for loan in last_loans:

            starting_day = loan.starting_date_time.strftime("%d-%m-%Y")
            ending_day = loan.ending_date_time.strftime("%d-%m-%Y")
            starting_hour = loan.starting_date_time.strftime("%H:%M")
            ending_hour = loan.ending_date_time.strftime("%H:%M")

            content = ''

            if starting_day == ending_day:
                content = starting_day + " " + starting_hour + " a " + ending_hour
            else:
                content = starting_day + ", " + starting_hour + " a " + ending_day + ", " + ending_hour

            url = '/loans/%d' % loan.id
            reservation_info = {
                'content': content,
                'url': url
            }

            loan_list.append(reservation_info)


        context = {
            'article': article,
            'last_loans': loan_list
        }

        return render(request, 'article_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')


def verificar_horario_habil(horario):
    return not is_non_workday(horario) and not (horario.hour < 9 or horario.hour > 18)
    # return not (horario.hour < 9 or horario.hour > 18)

@login_required
def article_request(request):
    if request.method == 'POST':
        article = Article.objects.get(id= request.POST['article_id'])

        if request.user.enabled:
            try:

                string_inicio = request.POST['fecha_inicio'] + " " + request.POST['hora_inicio']
                start_date_time = to_datetime(string_inicio)
                string_fin = request.POST['fecha_fin'] + " " + request.POST['hora_fin']
                end_date_time = to_datetime(string_fin)
                now_time = datetime.now()
                errors_found = False
                if start_date_time > end_date_time:
                    messages.warning(request, 'La reserva debe terminar después de iniciar.')
                    errors_found = True
                if start_date_time < now_time + timedelta(hours=1):
                    messages.warning(request, 'Los pedidos deben ser hechos al menos con una hora de anticipación.')
                    errors_found = True
                if not verificar_horario_habil(start_date_time) and not verificar_horario_habil(end_date_time):
                    messages.warning(request, 'Los pedidos deben ser hechos en horario hábil.')
                    errors_found = True
                if not errors_found:
                    loan = Loan(article=article, starting_date_time=start_date_time, ending_date_time=end_date_time,
                                user=request.user)
                    loan.save()
                    messages.success(request, 'Pedido realizado con éxito')
            except Exception as e:
                print(e)
                messages.warning(request, 'Ingrese una fecha y hora válida.')
        else:
            messages.warning(request, 'Usuario no habilitado para pedir préstamos')

        return redirect('/article/' + str(article.id))


@login_required
def article_data_admin(request, article_id):
    if not request.user.is_staff:
        return redirect('/')
    else:
        try:
            article = Article.objects.get(id=article_id)
            context = {
                'article': article
            }
            return render(request, 'article_data_admin.html', context)
        except:
            return redirect('/')


@login_required
def article_edit_fields(request, article_id):
    if request.method == "POST":
        try:
            a = Article.objects.get(id=article_id)

            if request.POST["name"] != "":
                a.name = request.POST["name"]

            a.description = request.POST["description"]

            if request.POST["state"] != "":
                a.state = request.POST["state"]

            u_file = request.FILES.get('image', False)
            if 'image' in request.FILES:
                extension = os.path.splitext(u_file.name)[1]
                a.image.save(str(article_id)+"_image"+extension, u_file)

            a.save()
            messages.success(request, 'Artículo editado exitosamente')
            return redirect('/admin/items-panel/')
        except Exception as e:
            messages.warning(request, 'Error al editar')

    return redirect('/space/' + str(article_id) + '/edit')

@login_required
def delete_item(request, article_id):

    item = Article.objects.get(id=article_id)
    item.delete()
    return redirect('/admin/items-panel/')
