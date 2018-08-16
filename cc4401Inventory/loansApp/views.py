from django.shortcuts import render, redirect
from loansApp.models import Loan
from articlesApp.models import Article
from django.contrib.auth.decorators import login_required


@login_required
def loan_data(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        article = loan.article
        loan_user = loan.user
        login_email = request.user.email
        context = {'loan': loan,
                   'article': article,
                   'loan_user': loan_user,
                   'login_email': login_email}
        if login_email == loan_user.email and loan.state == 'A':
            if article.state == 'L':
                context['change_article'] = 'P'
            elif article.state == 'P':
                context['change_article'] = 'L'
        return render(request, 'loan_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')


def loan_change_article_state(request, loan_id):
    if request.method == 'POST':
        if request.POST['user'] == request.POST['loan_user']:
            loan = Loan.objects.get(id=loan_id)
            article = Article.objects.get(id=loan.article.id)
            article.state = request.POST['state']
            article.save()
    return redirect('/loans/' + str(loan_id))
