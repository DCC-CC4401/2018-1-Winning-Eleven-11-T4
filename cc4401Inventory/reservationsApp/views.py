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
		reservations = Reservation.objects.filter(id__in=request.POST["selected"])
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

		starting_day = reservation.starting_date_time.strftime("%d-%m-%Y")
		ending_day = reservation.ending_date_time.strftime("%d-%m-%Y")
		starting_hour = reservation.starting_date_time.strftime("%H:%M")
		ending_hour = reservation.ending_date_time.strftime("%H:%M")

		context = {
			'space': space,
			'reservation': reservation,
			'user': reservation.user,
			'starting_day': starting_day,
			'ending_day': ending_day,
			'starting_hour': starting_hour,
			'ending_hour': ending_hour
		}

		return render(request, 'reservations_data.html', context)
	except Exception as e:
		print(e)
		return redirect('/')
