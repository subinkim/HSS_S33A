from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Category, Toppings, Order, CustomerOrder

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": "Welcome. Please login."})
    context = {
        "user": request.user,
        "orders": Order.objects.all()
    }
    return render(request, "orders/index.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

def register(request):
    ##Only if user submitted the form
    if request.method == "POST":

        ##Get data from the form
        username = request.POST["username"].lower()
        password = request.POST["password"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        ##Check if all fields are entered
        if (username == "") or (password == "") or (email == "") or (firstname == "") or (lastname == ""):
            return render(request, "orders/register.html", {"message": "Please fill in all the fields."})

        ##Check if username or email is already taken
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
                return render(request, "orders/login.html", {"message": None})
            return render(request, "orders/login.html", {"message": "Email already in use. Please login."})
        return render(request, "orders/register.html", {"message": "Username already taken."})

    ##If method = 'GET'
    else:
        return render(request, "orders/register.html", {"message": "Welcome! All the fields are required."})

def shoppingCart(request):
    orders = Order.objects.all()
    toppings = Toppings.objects.all()
    if request.method == "POST":
        food = str(request.POST['category'])
        menu = str(request.POST["menu"])
        size = str(request.POST["size"])
        price = float(request.POST["price"])
        username = str(request.user.username)
        #if we need to add toppings to pizza
        b = CustomerOrder.objects.create(username=username, food=food, menu=menu, size=size, price=price, ordered = False, processed=False)
        # order_id = CustomerOrder.objects.filter(username=username, food=food, menu=menu, size=size, price=price)
        if food == "One Topping Pizza" or food == "Two Toppings Pizza" or food == "Three Toppings Pizza":
            return render(request, "orders/topping.html", {"food": request.POST['category'], "toppings": toppings, "new": b })
        return HttpResponseRedirect(reverse('index'))
    else:
        username = request.user.username
        try:
            orders = CustomerOrder.objects.filter(username=username).exclude(ordered=True).all()
            total = 0
            for order in orders:
                total += float(order.price)
            orders = CustomerOrder.objects.filter(username=username).all()
            return render(request, "orders/checkout.html", {"orders": orders, "total": total})
        except CustomerOrder.DoesNotExist:
            orders = CustomerOrder.objects.filter(username=username).exclude(ordered=False).all()
            return render(request, "orders/checkout.html", {"message": "None in your cart!", "orders": orders})
        return render(request, "orders/index.html", {"message": "Cannot process your order :(", "orders": orders})

def addTopping(request):
    if request.method == "POST":
        topping1 = request.POST['topping1']
        topping2 = request.POST['topping2']
        topping3 = request.POST['topping3']
        order_id = request.POST['order_id']
        CustomerOrder.objects.filter(id=order_id).update(topping1=topping1, topping2=topping2, topping3=topping3)
        return HttpResponseRedirect(reverse('index'))

def checkout(request):
    if request.method == "GET":
        username = request.user.username
        try:
            orders = CustomerOrder.objects.filter(username=username).exclude(ordered=True).all()
            for order in orders:
                if order.ordered == False:
                    order.ordered = True
            CustomerOrder.objects.filter(username=username).exclude(ordered=True).update(ordered=True)
            orders = CustomerOrder.objects.filter(username=username).all()
            return render(request, "orders/checkout.html", {"orders": orders, "message": "Checked out!"})
        except CustomerOrder.DoesNotExist:
            orders = CustomerOrder.objects.filter(username=username).exclude(ordered=False).all()
            return render(request, "orders/checkout.html", {"message": "Nothing to check out!", "orders":orders})

def manage(request):
    orders = CustomerOrder.objects.all()
    if request.method == "POST":
        order_id = int(request.POST['order_id'])
        CustomerOrder.objects.filter(id=order_id).update(processed = True)
        return HttpResponseRedirect(reverse('manage'))
    else:
        return render(request, "orders/manage.html", {"orders":orders})

