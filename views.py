from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import CoffeePaymentForm
import razorpay
from .models import ColdCoffee


# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html") 

def gallery(request):
    return render(request,"gallery.html")

def service(request):
    return render(request,"service.html")

def pricing(request):
    return render(request,"pricing.html")

def contact(request):
    return render(request,"contact.html")

def signup(request):
    if request.method == "POST":
       
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request,"Your Account has been successfully created.")

        return redirect('signin')

    return render(request,"authenticate/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "index.html",{'fname':fname})

        else:
            messages.error(request,"Bad Credentials")
            return redirect('home')    

    return render(request,"authenticate/signin.html")


def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('')

def coffee_payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount'))*100

        #create Razorpay client
        client = razorpay.Client(auth=('rzp_live_f7rU7Ets8WPW3R','bcd7vi3bF1AFAd6RLuJdIyCX'))


        #create order
        response_payment = client.order.create(dict(amount = amount,
                                                    currency = 'INR')
                                                    )
        order_id = response_payment['id']
        order_status = response_payment['status']

        if order_status == 'created':
            cold_coffee = ColdCoffee(
                name = name,
                amount = amount,
                order_id = order_id
            )
            cold_coffee.save()
            response_payment['name'] = name

            form = CoffeePaymentForm(request.POST or None)
            return render(request, 'coffee_payment.html', {'form': form, 'payment':response_payment})                                            



    form = CoffeePaymentForm()
    return render(request, 'coffee_payment.html', {'form':form})


def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_signature' : response['razorpay_signature']
    }

    #client instance
    client = razorpay.Client(auth = ('rzp_live_f7rU7Ets8WPW3R','bcd7vi3bF1AFAd6RLuJdIyCX'))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        cold_coffee = ColdCoffee.objects.get(order_id = response['razorpay_order_id'])
        cold_coffee.razorpay_payment_id = response['razorpay_payment_id']
        cold_coffee.paid = True
        cold_coffee.save()
        return render(request,'payment_status.html',{'status':True})
    except:
        return render(request,'payment_status.html',{'status':False})

    return render(request, 'payment_status.html')    