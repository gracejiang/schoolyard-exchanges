from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from main.models import Exchange
from datetime import datetime

'''TEMPLATE RENDERING'''
def main_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash/')

    exchanges = Exchange.objects.all().order_by('-created_at')
    return render(request, 'main.html', {'tweets': exchanges})

def splash_view(request):
    return render(request, 'splash.html' )

def new_listing_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash/')

    if request.method == 'POST':
        print("HELLOOOO")
        if request.POST['offer_title'] != "" and request.POST['offer_type'] != "" and request.POST['offer_description'] != "" and request.POST['lf_title'] != "" and request.POST['lf_type'] != "" and request.POST['lf_description'] != "":
            print("sup")
            print(request.POST['offer_title'])
            exchange = Exchange.objects.create(
                offer_title = request.POST['title'],
                offer_description = request.POST['offer_description'],
                offer_type = request.POST['offer_type'],
                lf_description = request.POST['lf_description'],
                lf_type = request.POST['lf_type'],
                seller = request.user,
                buyer = None,
                created_at = datetime.now()
            )
            exchange.save()

            exchanges = Exchange.objects.all().order_by('-created_at')
            return render(request, 'main.html', {'exchanges': exchanges})
        else:
            return redirect('/new_listing?error=EmptyInputFields')
            
    return render(request, 'new_listing.html' )

'''ACTIONS'''
# delete an exchange routing
def delete_exchange_view(request):
    exchange = Exchange.objects.get(id=request.GET['id'])
    if exchange.seller == request.user:
        exchange.delete()
    return redirect('/')


'''USER LOGIN/REGISTRATION/LOGOUT'''

# login
def login_view(request):
    username, password = request.POST['username'], request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/splash?error=LoginError')

# signup
def signup_view(request):
    user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email'],
    )
    login(request, user)
    return redirect('/')

# logout
def logout_view(request):
    logout(request)
    return redirect('/splash')