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


def user_cancel_reservation(request, reservation_id):
    space_id = None
    if request.method == 'POST':
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            space_id = reservation.space_id
            if reservation.user.id != request.user.id and not (request.user.is_staff or request.user.is_superuser):
                messages.warning(request, 'Usuario no autorizado para cancelar reserva')
            elif reservation.state == 'P':
                reservation.delete()
        except:
            messages.warning(request, 'Ha ocurrido un error y la reserva no se ha eliminado')

        redirect_string = '/'
        if space_id is not None:
            redirect_string = '/space/%d' % space_id
        return redirect(redirect_string , user_id=request.user.id)


def modify_reservations(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    if request.method == "POST":

        accept = True if (request.POST["accept"] == "1") else False
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


def reservations_data(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        space = reservation.space
        user = reservation.user
        login_email = request.user.email
        user_owns_reservation = user.id == request.user.id or request.user.is_superuser or request.user.is_staff
        context = {'reservation': reservation,
                   'space': space,
                   'user': user,
                   'login_email': login_email,
                   'user_owns_reservation': user_owns_reservation
                   }

        if login_email == user.email and reservation.state == 'A':
            if space.state == 'D':
                context['change_space'] = 'P'
            elif space.state == 'P':
                context['change_space'] = 'L'
            elif space.state == 'R	':
                context['change_space'] = 'L'
        return render(request, 'reservations_data.html', context)
    except Exception as e:

        return redirect('/')
