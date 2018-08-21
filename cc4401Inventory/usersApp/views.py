from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from mainApp.models import User
from django.contrib import messages

from reservationsApp.models import Reservation

from loansApp.models import Loan


def login_view(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'usersApp/login.html', context=context)
    if request.method == 'POST':
        pass


# se llama cuando se envia el formulario de login
def login_submit(request):

    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    context = {'error_message': ''}

    if user is not None:
        login(request, user)
        return redirect('/articles/')
    else:
        messages.warning(request, 'La contraseña ingresada no es correcta o el usuario no existe')
        return redirect('/user/login')


# se llama cuando se quiere acceder a la pagina de creacion de cuentas
def signup(request):
    if request.method == 'GET':
        return render(request, 'usersApp/create_account.html')
    if request.method == 'POST':
        pass


# se llama cuando se manda el formulario de creacion de cuentas
def signup_submit(request):

    context = {'error_message': '', }

    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        rut = request.POST['RUT']

        if password != password_confirm:
            messages.warning(request, 'Las contraseñas deben ser iguales.')
            return redirect('/user/signup/')
        elif User.objects.filter(email = email).exists():
            messages.warning(request, 'Ya existe una cuenta con ese correo.')
            return redirect('/user/signup/')
        elif User.objects.filter(rut = rut).exists():
            messages.warning(request, 'Ya existe una cuenta con ese rut')
            return redirect('/user/signup/')
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, rut = rut)
            login(request, user)
            messages.success(request, 'Bienvenid@, ' + user.first_name + ' ya puedes comenzar a hacer reservas :)')
            return redirect('/articles/')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/user/login/')



@login_required
def user_data(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        reservations = Reservation.objects.filter(user = user_id).order_by('-starting_date_time')
        loans = Loan.objects.filter(user = user_id).order_by('-starting_date_time')

        index_res = 0
        index_loans = 0

        articulos1 = Loan.objects.filter(user = user_id).order_by('-starting_date_time')[:10]
        espacios1  = []

        articulos2 = Reservation.objects.filter(user = user_id).order_by('-starting_date_time')[:10]
        espacios2  = []

        for res in reservations:
            if res.state == 'A':
                espacios2.append(res)
        for loan in loans:
            if loan.state == 'A':
                espacios1.append(loan)

        context = {
            'user': user,
            'reservations': reservations,
            'loans': loans,
            'articulos1': articulos1,
            'espacios1': espacios1,
            'articulos2': articulos2,
            'espacios2': espacios2
        }
        return render(request, 'usersApp/user_profile.html', context)
    except Exception:
        return redirect('/')


def delete(request):
    if request.method == 'POST':
        reservation_ids = request.POST.getlist('loan')
        try:
            for reservation_id in reservation_ids:
                reservation = Loan.objects.get(id=reservation_id)
                if reservation.state == 'P':
                    reservation.delete()
        except:
            messages.warning(request, 'Ha ocurrido un error y la reserva no se ha eliminado')

        return redirect('user_data', user_id=request.user.id)
