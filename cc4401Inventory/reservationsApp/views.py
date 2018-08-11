from django.shortcuts import render, redirect
from .models import Reservation
from django.contrib import messages


def delete(request):
    if request.method == 'POST':
        reservation_ids = request.POST.getlist('reservation')
        try:
            for reservation_id in reservation_ids:
                reservation = Reservation.objects.get(id=reservation_id)
                if reservation.state == 'P':
                    reservation.delete()
        except:
            messages.warning(request, 'Ha ocurrido un error y la reserva no se ha eliminado')

        return redirect('user_data', user_id=request.user.id)


def modify_reservations(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    if request.method == "POST":

        accept = True if (request.POST["accept"] == "1") else False
        #reservations = Reservation.objects.filter(id__in=request.POST["selected"])
        reservations = Reservation.objects.filter(id__in=request.POST.getlist("selected"))

        if accept:
            for reservation in reservations:
                reservation.state = 'A'
                reservation.save()
        else:
            for reservation in reservations:
                reservation.state = 'R'
                reservation.save()

    return redirect('/admin/actions-panel')
