from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

from .models import Userprofile,details_new,menu_new,Cart,CartItems,payment

# Create your views here.
def register (request):
    if request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        pincode=request.POST['pincode']
        address=request.POST['address']
        role=request.POST['role']
        email=request.POST['email']
        password=request.POST['password']
        user=User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
        userProfile = Userprofile.objects.create(user=user,address=address,role=role,pincode=pincode)
        userProfile.save()
        return redirect('login')
    else:
        return render (request,'user/register.html')

def login_user(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        authenticated_user=authenticate(username=username,password=password)

        if authenticated_user is not None:
            login(request,authenticated_user)
            print(authenticated_user.userprofile.role)
            if authenticated_user.userprofile.role == 'customer':
                return redirect('restaurent')
            elif authenticated_user.userprofile.role == 'restaurent':
                return redirect('rest_home')
            # elif authenticated_user.userprofile.role == 'admin':
            #     return redirect('admin')
        else:
            return redirect('login') 
    return render (request,'user/login.html')

def restaurent (request):
    details = details_new.objects.all()
    return render (request,'user/restaurent.html',context={'details_new':details})

def index (request):
 
    return render (request,'user/index.html')

def rest_home (request):
    rests = details_new.objects.filter(is_active=True) 
    context = {
        'details':rests
    } 
    return render(request, 'restaurant/rest_home.html',context)
    

def admin(request):
   
    return render (request,'admin.html')

def rest_details(request):
    if request.method == 'POST':
        restaurantName = request.POST['restaurantName']
        address = request.POST['address']
        pincode = request.POST['pincode']
        location = request.POST['location']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        image = request.FILES['restaurantImage']

        # Create an instance of the Details model and save it
        details = details_new(
            restaurantName=restaurantName,
            address=address,
            pincode=pincode,
            location=location,
            latitude=latitude,
            longitude=longitude,
            image=image,
            created_by = request.user
        )
        details.save()
        return redirect('menu_details')  # Redirect after successful save
    else:
        return render(request, 'restaurant/rest_details.html')

def menu_details(request):
    if request.method == "POST":
        rest = details_new.objects.get(created_by=request.user)
        menuItemName=request.POST['menuItemName']   
        description=request.POST['description']  
        price=request.POST['price'] 
        category=request.POST['category']
        availability=request.POST['availability']  
        image1= request.FILES['menuItemImage']
        menu=menu_new(
            menuItemName=menuItemName,
            description=description,
            price=price,
            category=category,
            availability=availability,
            image1=image1,
            restaurant=rest,
            created_by = request.user
        )
        menu.save()
        return redirect('restaurent')
    return render (request,'menu_details.html')

def menu_home(request, rest):
    # Filter restaurants matching the criteria
    restaurants = details_new.objects.filter(id=rest)
    
    # Get all menu items for the filtered restaurants
    menu = menu_new.objects.filter(restaurant__in=restaurants)
    
    return render(request, 'menu_home.html', context={'menu_new': menu})

   

def update_rest(request):
    if request.method == 'POST':
        restaurantName = request.POST['restaurantName']
        address = request.POST['address']
        pincode = request.POST['pincode']
        location = request.POST['location']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        details=details_new.objects.get(created_by=request.user)
        details.restaurantName = restaurantName
        details.address = address
        details.pincode = pincode
        details.location = location
        details.latitude = latitude
        details.longitude = longitude
        details.save()
        return redirect('rest_home')
    else:
        details = details_new.objects.get(created_by=request.user)
        context={
            'details':details
        }
   
    return render (request,'restaurant/update_menu.html',context)

def cart(request):
    
    cart = Cart.objects.get(user=request.user,is_active=True)
    cart_items = CartItems.objects.filter(cart=cart)
    total_price = sum(float(item.menu_item.price) * item.quantity for item in cart_items)
    
    return render(request, 'restaurant/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })
    
    

def add_cart(request, menu):
    
    menu_item = menu_new.objects.get(id=menu)
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_item, item_created = CartItems.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not item_created:
       
        cart_item.save()
    else:
        
        cart_item.save()
    
    return redirect('cart')



def delete_cart(request,menu):
    menu_item=CartItems.objects.get(menu_item=menu) 
    menu_item.delete()
    return redirect('cart') 

def Payment(request):
    if request.method == 'POST':
        paymentOption= request.POST['paymentOption']
        cardNumber=request.POST['cardNumber']
        cardholderName=request.POST['cardholderName']
        print(paymentOption,cardNumber,cardholderName)
        pay=payment(user_id = request.user.id,paymentOption=paymentOption,cardNumber=cardNumber,cardholderName=cardholderName)
        
        pay.save()
        return redirect('payment_succes')
    else:
        return render(request,'payment/payment.html')

def payment_succes(request):
    return render(request,'payment/payment_succes.html')



def deletemenupage(request):
     delete = menu_new.objects.filter(created_by=request.user)
     
    
     return render(request, 'menudelete.html', {
          'menu_new': delete })
     
def delete_menu(request,menu):
    menu_item1=menu_new.objects.get(id=menu) 
    menu_item1.delete()
    return redirect('deletemenupage') 

def about_us(request):
    return render(request,'aboutus.html')




def update_login(request): 
    if request.method == 'POST':
        user = request.user
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')

        if new_username:
            user.username = new_username
        if new_password:
            user.set_password(new_password)  

        user.save()
        return redirect('login')

    else:
       
        user = request.user
        context = {
            'authenticated_user': user,
        }

    return render(request, 'update_login.html', context)
