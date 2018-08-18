from django.shortcuts import render
import datetime
from datetime import timedelta
from articlesApp.models import Article
from reservationsApp.models import Reservation
from spacesApp.models import Space
from django.contrib.auth.decorators import login_required
from django.contrib import messages
@login_required
def landing_articles(request):
    context = {}
    return render(request, 'articulos.html', context)


@login_required
def landing_spaces(request):


    reservations = Reservation.objects.exclude(state='R').order_by('starting_date_time')
    spaces = Space.objects.all()
    coloresP = ['rgba(102,153,102,0.7)', 'rgba(153,102,102,0.7)', 'rgba(102,102,153,0.7)', 'rgba(153,127,102,0.5)',
                'rgba(153,102,153,0.7)', 'rgba(102,153,153,0.7)']
    coloresA = ['rgba(63,191,63,0.9)', 'rgba(191,63,63,0.9)', 'rgba(63,63,191,0.9)', 'rgba(191,127,63,0.9)',
               'rgba(191,63,191,0.9)', 'rgba(63,191,191,0.9)']

    spaces_list=[]
    reservations_list=[]
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

        if "ReservaForm" in request.POST:
            for s in spaces:
                space_filter.append(int(s.id))
            if request.user.enabled:
                space = Space.objects.get(id=request.POST["spaceid"])
                try:
                    string_startDate = request.POST["startDate"]
                    string_endDate = request.POST["endDate"]
                    start_date_time = datetime.datetime.strptime(string_startDate, '%Y-%m-%d %H:%M')
                    end_date_time = datetime.datetime.strptime(string_endDate, '%Y-%m-%d %H:%M')
                    if start_date_time > end_date_time:
                        messages.warning(request, 'La reserva debe terminar después de iniciar.')
                    elif start_date_time < datetime.datetime.now() + timedelta(hours=1):
                        messages.warning(request, 'Los pedidos deben ser hechos al menos con una hora de anticipación.')
                    elif start_date_time.date() != end_date_time.date():
                        messages.warning(request, 'Los pedidos deben ser devueltos el mismo día que se entregan.')
                    elif not verificar_horario_habil(start_date_time) and not verificar_horario_habil(end_date_time):
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
                        "estado": r.state,
                        "id": r.id
                    }
                    reservations_list.append(reserva_dic)

    context = {'reservations': reservations_list,
               'spacesList': spaces_list,
               'spacesFilter': space_filter,
               'request': request
    }
    return render(request, 'espacios.html', context)


@login_required
def landing_search(request, products):
    if not products:
        return landing_articles(request)
    else:
        context = {'productos' : products,
                   'colores' : {'D': '#009900',
                                'R': '#ffcc00',
                                'P': '#3333cc',
                                'L': '#cc0000'}
                   }
        return render(request, 'articulos.html', context)


@login_required
def search(request):
    if request.method == "GET":
        query = request.GET['query']
        #a_type = "comportamiento_no_definido"
        a_state = "A" if (request.GET['estado'] == "A") else request.GET['estado']

        if not (a_state == "A"):
            articles = Article.objects.filter(state=a_state,name__icontains=query.lower())
        else:
            articles = Article.objects.filter(name__icontains=query.lower())

        products = None if (request.GET['query'] == "") else articles
        return landing_search(request, products)

def verificar_horario_habil(horario):
    if horario.isocalendar()[2] > 5:
        return False
    if horario.hour < 9 or horario.hour > 18:
        return False

    return True