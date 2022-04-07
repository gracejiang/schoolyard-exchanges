from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from main.models import Exchange
from datetime import datetime

'''TEMPLATE RENDERING'''
def get_exchanges_filter(request):
    searchText = (".filter(name__contains=\"" + request.POST['searchText'] + "\")") if ('searchText' in request.POST and request.POST['searchText'] != "") else ""
    filterOffering = (".filter(lf_type=\"" + request.POST['filterOffering'] + "\")") if (('filterOffering' in request.POST) and request.POST['filterOffering'] != "any") else ""
    filterLf = (".filter(offer_type=\"" + request.POST['filterLf'] + "\")") if (('filterLf' in request.POST) and request.POST['filterLf'] != "any") else ""
    filters_str = "Exchange.objects.all()" + searchText + filterOffering + filterLf + ".order_by('-created_on')" 

    print("filsters_str")
    print(filters_str)
    exchanges = eval(filters_str)
    
    return exchanges

def main_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash/')
    
    if request.method == 'POST':
        exchanges = get_exchanges_filter(request)
    else:
        exchanges = Exchange.objects.all().order_by('-created_on')

    return render(request, 'main.html', {'exchanges': exchanges})

def your_listings_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash/')

    exchanges = Exchange.objects.all().order_by('-created_on').filter(seller=request.user)
    return render(request, 'your_listings.html', {'exchanges': exchanges})

def your_biddings_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash/')

    exchanges = Exchange.objects.all().order_by('-created_on').filter(buyer=request.user)
    return render(request, 'your_listings.html', {'exchanges': exchanges})

def splash_view(request):
    return render(request, 'splash.html' )

def new_listing_view(request):
    if not request.user.is_authenticated:
        return redirect('/splash/')

    if request.method == 'POST':
        valid_request = 'offer_title' in request.POST and 'offer_type' in request.POST and 'offer_description' in request.POST and 'lf_title' in request.POST and 'lf_type' in request.POST and 'lf_description' in request.POST 
        if valid_request and request.POST['offer_title'] != "" and request.POST['offer_type'] != "" and request.POST['offer_description'] != "" and request.POST['lf_title'] != "" and request.POST['lf_type'] != "" and request.POST['lf_description'] != "":
            print(request.POST['offer_title'])
            exchange = Exchange.objects.create(
                offer_title = request.POST['offer_title'],
                offer_description = request.POST['offer_description'],
                offer_type = request.POST['offer_type'],
                lf_title = request.POST['lf_title'],
                lf_description = request.POST['lf_description'],
                lf_type = request.POST['lf_type'],
                seller = request.user,
                buyer = None,
                name = request.POST['offer_title'] + " " + request.POST['lf_title'],
                created_on = datetime.now()
            )
            exchange.save()

            exchanges = Exchange.objects.all().order_by('-created_on')
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
    return redirect('/your_listings')


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