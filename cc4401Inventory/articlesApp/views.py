from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from articlesApp.models import Article
from loansApp.models import Loan
from django.db import models
from datetime import datetime, timedelta

import random, os
from django.contrib import messages

from utils.time_utils import to_chile_time_normalization, to_datetime, is_non_workday




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

            if starting_day == ending_day:
                loan_list.append(starting_day+" "+starting_hour+" a "+ending_hour)
            else:
                loan_list.append(starting_day + ", " + starting_hour + " a " +ending_day + ", " +ending_hour)


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


@login_required
def article_request(request):
    if request.method == 'POST':
        article = Article.objects.get(id= request.POST['article_id'])

        if request.user.enabled:
            try:

                string_inicio = request.POST['fecha_inicio'] + " " + request.POST['hora_inicio']
                start_date_time = to_chile_time_normalization(to_datetime(string_inicio))
                string_fin = request.POST['fecha_fin'] + " " + request.POST['hora_fin']
                end_date_time = to_chile_time_normalization(to_datetime(string_fin))
                now_time = to_chile_time_normalization(datetime.now())
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
def article_edit_name(request, article_id):

    if request.method == "POST":
        a = Article.objects.get(id=article_id)
        a.name = request.POST["name"]
        a.save()
    return redirect('/article/'+str(article_id)+'/edit')


@login_required
def article_edit_image(request, article_id):

    if request.method == "POST":
        u_file = request.FILES["image"]
        extension = os.path.splitext(u_file.name)[1]
        a = Article.objects.get(id=article_id)
        a.image.save(str(article_id)+"_image"+extension, u_file)
        a.save()

    return redirect('/article/' + str(article_id) + '/edit')



@login_required
def article_edit_description(request, article_id):
    if request.method == "POST":
        a = Article.objects.get(id=article_id)
        a.description = request.POST["description"]
        a.save()

    return redirect('/article/' + str(article_id) + '/edit')
