from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
import json
import datetime
from django.utils import timezone
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    cartItems = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only get existing orders, don't create new ones
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            cartItems = order.get_cart_items
    
    context = {'cartItems': cartItems}
    return render(request, 'shop/home.html', context)


def explore(request):
    cartItems = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only get existing orders, don't create new ones
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            cartItems = order.get_cart_items
    
    context = {'cartItems': cartItems}
    return render(request, 'shop/explore.html', context)


@login_required(login_url='login')
def account(request):
    cartItems = 0
    shipping_address = None
    
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only get existing orders, don't create new ones
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            cartItems = order.get_cart_items
        
        # Try to get the most recent shipping address for this customer
        shipping_address = ShippingAddress.objects.filter(customer=customer).order_by('-date_created').first()
    
    context = {
        'cartItems': cartItems,
        'shipping_address': shipping_address
    }
    return render(request, 'shop/account.html', context)


@login_required(login_url='login')
def orderhistory(request):
    cartItems = 0
    orders = []
    
    if request.user.is_authenticated:
        customer = request.user.customer
        # Get current cart items count
        current_order = Order.objects.filter(customer=customer, complete=False).first()
        if current_order:
            cartItems = current_order.get_cart_items
            
        # Get completed orders
        orders = Order.objects.filter(
            customer=customer, 
            complete=True
        ).order_by('-date_created')
    
    context = {
        'cartItems': cartItems,
        'orders': orders
    }
    return render(request, 'shop/orderhistory.html', context)


@login_required(login_url='login')
def bookhistory(request):
    cartItems = 0
    bookings = []
    
    if request.user.is_authenticated:
        customer = request.user.customer
        # Get current cart items count
        current_order = Order.objects.filter(customer=customer, complete=False).first()
        if current_order:
            cartItems = current_order.get_cart_items
            
        # Get all bookings
        bookings = ServiceBooking.objects.filter(
            customer=customer
        ).order_by('-date_created')
    
    context = {
        'cartItems': cartItems,
        'bookings': bookings
    }
    return render(request, 'shop/bookhistory.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Invalid username OR password')

        context = {}
        return render(request, 'shop/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                # Create a Customer object for the new user
                Customer.objects.create(
                    user=user,
                    name=f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}",
                    phone=form.cleaned_data.get('phone'),
                    email=form.cleaned_data.get('email')
                )
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account created for ' + username)            
                return redirect('login')
        context = {'form': form}
        return render(request, 'shop/register.html', context)
    

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only create new order if it's the shop page - this is where users actually shop
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cartItems = 0
        items = []

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'shop/shop.html', context)


@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only get existing orders, don't create new ones
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            cartItems = 0
            order = None
    else:
        return redirect('login')

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shop/cart.html', context)


@login_required(login_url='login')
def shopcheckout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only get existing orders, don't create new ones
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            items = order.orderitem_set.all()
        else:
            items = []
            order = None
            # Redirect to cart if no order exists
            return redirect('cart')
    else:
        return redirect('login')

    context = {'items': items, 'order': order}
    return render(request, 'shop/shopcheckout.html', context)


@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action', action)
    print('ProductId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    
    # Here we need to create an order if it doesn't exist
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0    

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='login')
def processOrder(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
        
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print("Received data:", data)  # Debug print

    customer = request.user.customer
    # Only get existing orders, don't create new ones
    order = Order.objects.filter(customer=customer, complete=False).first()
    
    if not order:
        return JsonResponse({'error': 'No active order found'}, status=400)

    if order.transaction_id:
        print(f"Order {order.id} already has transaction ID {order.transaction_id}")
        # This is a duplicate submission, just return success
        return JsonResponse('Order already processed', safe=False)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    print(f"Order total: {order.get_cart_total}, Form total: {total}")  # Debug print
    
    # Update order status
    order.complete = True 
    order.status = 'Pending'
    order.save()
    
    # Print shipping data
    print("Shipping data:", data.get('shipping', {}))
    
    # Create shipping address
    try:
        shipping_data = data.get('shipping', {})
        if shipping_data:
            existing_address = ShippingAddress.objects.filter(order=order).first()
            
            if existing_address:
                # Update existing address
                existing_address.address = shipping_data.get('address', '')
                existing_address.city = shipping_data.get('city', '')
                existing_address.state = shipping_data.get('state', '')
                existing_address.save()
                print(f"Updated shipping address with ID: {existing_address.id}")
            else:
                # Create new address
                shipping_address = ShippingAddress(
                    customer=customer,
                    order=order,
                    address=shipping_data.get('address', ''),
                    city=shipping_data.get('city', ''),
                    state=shipping_data.get('state', '')
                )
                shipping_address.save()
                print(f"Shipping address saved with ID: {shipping_address.id}")
        else:
            print("No shipping data found in request")
    except Exception as e:
        print(f"Error saving shipping address: {str(e)}")
    
    return JsonResponse('Payment submitted..', safe=False)


@login_required(login_url='login')
def book(request):
    services = Service.objects.all()
    cartItems = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only get existing orders, don't create new ones
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            cartItems = order.get_cart_items
    
    context = {'services': services, 'cartItems': cartItems}
    return render(request, 'shop/book.html', context)


@login_required(login_url='login')
def book_service(request, service_id):
    service = Service.objects.get(id=service_id)
    cartItems = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only get existing orders, don't create new ones
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            cartItems = order.get_cart_items
    
    context = {'service': service, 'cartItems': cartItems}
    return render(request, 'shop/book_service.html', context)


@login_required(login_url='login')
def bookcheckout(request, service_id):
    service = Service.objects.get(id=service_id)
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    # Include the current date to set minimum date in the form
    today = datetime.date.today()
    cartItems = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only get existing orders, don't create new ones
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            cartItems = order.get_cart_items
    
    context = {'service': service, 'cartItems': cartItems, 'today': today}
    return render(request, 'shop/bookcheckout.html', context)


@login_required(login_url='login')
def process_booking(request, service_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    data = json.loads(request.body)
    booking_data = data.get('booking', {})
    
    service = Service.objects.get(id=service_id)
    customer = request.user.customer
    
    # Get form data
    booking_date = booking_data.get('booking_date')
    booking_time = booking_data.get('booking_time')
    notes = booking_data.get('notes', '')
    
    # Properly combine date and time for scheduled_date
    try:
        date_obj = datetime.datetime.strptime(booking_date, '%Y-%m-%d').date()
        time_obj = datetime.datetime.strptime(booking_time, '%H:%M').time()
        
        scheduled_datetime = datetime.datetime.combine(date_obj, time_obj)
        scheduled_datetime = timezone.make_aware(scheduled_datetime)
        
        # Create the booking
        booking = ServiceBooking(
            customer=customer,
            service=service,
            scheduled_date=scheduled_datetime,
            notes=notes,
            status='Pending'
        )
        booking.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Booking created successfully',
            'booking_id': booking.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    

@login_required(login_url='login')
def shopsuccess(request):
    cartItems = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        # Only get existing orders, don't create new ones
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order:
            cartItems = order.get_cart_items
    
    context = {'cartItems': cartItems}
    return render(request, 'shop/shopsuccess.html', context)


@login_required(login_url='login')
def booksuccess(request):
    context = {}
    return render(request, 'shop/booksuccess.html')