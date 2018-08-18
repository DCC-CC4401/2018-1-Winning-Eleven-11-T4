from django.shortcuts import render, redirect
from spacesApp.models import Space
from reservationsApp.models import Reservation
import datetime
from django.contrib import messages
from datetime import timedelta

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


        context = {
            'space': space,
            'reservations': reservations_list,
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