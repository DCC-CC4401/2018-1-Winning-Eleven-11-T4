from django.shortcuts import render, redirect
from loansApp.models import Loan


# Create your views here.
def loan_data(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        article = loan.article
        user = loan.user
        context = {'loan': loan,
                   'article': article,
                   'user': user}
        return render(request, 'loan_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')
