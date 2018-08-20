from django.shortcuts import render, redirect
from spacesApp.models import Space
from django.contrib.auth.decorators import login_required
from reservationsApp.models import Reservation
import datetime
from django.contrib import messages
from datetime import timedelta
import os
from django.core.files import File
import urllib


def space_data(request, space_id):
    try:
        space = Space.objects.get(id=space_id)
        reservations = Reservation.objects.filter(space=space_id).exclude(state='R')
        reservations_list = []

        for r in reservations:
            title = str(r.space.name) + " - " + str(r.user.get_full_name())
            color = 'rgba(102,153,102,0.9)'
            if r.state == 'P':
                title = title + " (pendiente)"
                color = 'rgba(102,153,102,0.7)'
                reserva_dic = {
                    "title": title,
                    "start": r.starting_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": r.ending_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "color": color,
                    "estado": r.state
                }
                reservations_list.append(reserva_dic)
        if request.method == 'POST':
            if "ReservaForm" in request.POST:
                if request.user.enabled:
                    try:
                        string_startDate = request.POST["startDate"]
                        string_endDate = request.POST["endDate"]
                        start_date_time = datetime.datetime.strptime(string_startDate, '%Y-%m-%d %H:%M')
                        end_date_time = datetime.datetime.strptime(string_endDate, '%Y-%m-%d %H:%M')
                        if start_date_time > end_date_time:
                            messages.warning(request, 'La reserva debe terminar después de iniciar.')
                        elif start_date_time < datetime.datetime.now() + timedelta(hours=1):
                            messages.warning(request,
                                             'Los pedidos deben ser hechos al menos con una hora de anticipación.')
                        elif start_date_time.date() != end_date_time.date():
                            messages.warning(request, 'Los pedidos deben ser devueltos el mismo día que se entregan.')
                        elif not verificar_horario_habil(start_date_time) and not verificar_horario_habil(
                                end_date_time):
                            messages.warning(request, 'Los pedidos deben ser hechos en horario hábil.')
                        else:
                            newReserv = Reservation()
                            newReserv.space = space
                            newReserv.starting_date_time = start_date_time
                            newReserv.ending_date_time = end_date_time
                            newReserv.user = request.user
                            newReserv.save()
                            messages.success(request, 'Reserva realizada con éxito')
                    except Exception as e:
                        messages.warning(request, 'Ingrese una fecha y hora válida. ')
                else:
                    messages.warning(request, 'Usuario no habilitado para pedir préstamos')

        last_reservations = Reservation.objects.filter(space=space_id).order_by('-ending_date_time')[:10]

        reservations_last_ten = list()
        for reservation in last_reservations:
            starting_day = reservation.starting_date_time.strftime("%d-%m-%Y")
            ending_day = reservation.ending_date_time.strftime("%d-%m-%Y")
            starting_hour = reservation.starting_date_time.strftime("%H:%M")
            ending_hour = reservation.ending_date_time.strftime("%H:%M")

            content = ''

            if starting_day == ending_day:
                content = starting_day + " " + starting_hour + " a " + ending_hour
            else:
                content = starting_day + ", " + starting_hour + " a " + ending_day + ", " + ending_hour

            url = '/reservation/%d' % reservation.id
            reservation_info = {
                'content': content,
                'url': url
            }

            reservations_last_ten.append(reservation_info)

        context = {
            'space': space,
            'reservations': reservations_list,
            'reservations_last_ten': reservations_last_ten,
            'request': request
        }

        return render(request, 'space_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')


def verificar_horario_habil(horario):
    if horario.isocalendar()[2] > 5:
        return False
    if horario.hour < 9 or horario.hour > 18:
        return False

    return True


@login_required
def space_data_admin(request, space_id):
    if not request.user.is_staff:
        return redirect('/')
    else:
        try:
            space = Space.objects.get(id=space_id)
            context = {
                'space': space
            }
            return render(request, 'space_data_admin.html', context)
        except:
            return redirect('/')


@login_required
def space_edit_fields(request, space_id):
    if request.method == "POST":
        s = Space.objects.get(id=space_id)
        if request.POST["name"] != "":
            s.name = request.POST["name"]
        s.description = request.POST["description"]

        u_file = request.FILES.get('image', False)
        if 'image' in request.FILES:
            extension = os.path.splitext(u_file.name)[1]
            s.image.save(str(space_id)+"_image"+extension, u_file)

        s.save()
        return redirect('/admin/items-panel/')
    return redirect('/space/' + str(space_id) + '/edit')


