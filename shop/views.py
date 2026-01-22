import json
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from.models import Product
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProductForm
from django.contrib.auth import authenticate, login ,logout
from django.shortcuts import redirect, render
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import ProfileForm

@login_required
def profile_view(request):
    # THIS LINE FIXES YOUR ERROR
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'profile': profile,
        'form': form
    })



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
@login_required
def my_orders(request):
    # Current user ke orders fetch karo
    orders = Order.objects.filter(user=request.user).order_by('-id')  # latest first

    # Har order ke items fetch karo using related_name
    orders_with_items = []
    for order in orders:
        items = order.items.all()  # <--- related_name ke through
        orders_with_items.append({
            'order': order,
            'items': items
        })

    context = {
        'orders_with_items': orders_with_items
    }
    return render(request, 'my_orders.html', context)


def logout_view(request):
    logout(request)
    return redirect('signup')  
@login_required
def update_profile(request):
    user = request.user
    try:
        profile = user.userprofile  # Your OneToOne relation
    except:
        # In case the profile is not created yet
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }

    return render(request, 'update_profile.html', context)


# Create your views here.
def home(request):
    all=Product.objects.all()
    product=Product.objects.filter(category="men")
    women=Product.objects.filter(category="women")
    child=Product.objects.filter(category="child")
    acc=Product.objects.filter(category="accessories")
    return render(request,"newhome.html",locals())

def select(request,id):
    product_select=Product.objects.get(id=id)
    related_products=Product.objects.filter(category=product_select.category).exclude(id=product_select.id)[:4]
    return render(request,"new_select.html",locals())

def add_to_cart(request):
        product_id=str(request.POST.get("product_id"))
        # session se cart nikalo, agar nahi hai to empty dict
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, id=product_id)
        product_id = str(product.id)
        # agar product pehle se cart me hai to quantity +1
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        # session me wapas save
        request.session['cart'] = cart
        
        
        request.session.modified=True
        cart_count=len(cart)
        return JsonResponse({"message":"added",
                             "cart_count":cart_count,})
    # cart page pe bhej de
    


def add_to_cart_and_redirect(request, product_id):
    """Add product to cart and redirect to cart page"""
    # session se cart nikaalo
    cart = request.session.get('cart', {})

    product = get_object_or_404(Product, id=product_id)
    product_id_str = str(product.id)

    # quantity +1 agar already hai
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    # session me save karo
    request.session['cart'] = cart
    request.session.modified = True

    # redirect to existing cart page
    return redirect('showCart')
def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_price = 0

    for product in products:
        qty = cart[str(product.id)]
        subtotal = product.discount_price * qty
        total_price += subtotal

        cart_items.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal,
         
        })
        
                
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def increase_qty(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        product_id = str(data.get("product_id"))

        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session['cart'] = cart

        # Item subtotal
        product = Product.objects.get(id=product_id)
        item_subtotal = product.discount_price * cart[product_id]

        # Total cart price
        total_price = 0
        for pid, qty in cart.items():
            p = Product.objects.get(id=pid)
            total_price += p.discount_price * qty
            cart_count=len(cart)

        return JsonResponse({
            "quantity": cart[product_id],
            "item_subtotal": item_subtotal,
            "total_price": total_price,
            "cart_count":cart_count,
        })

def decrease_qty(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        product_id = str(data.get("product_id"))

        cart = request.session.get("cart", {})

        if product_id in cart:
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]
                


        request.session["cart"] = cart

        # Item subtotal
        item_subtotal = 0
        if product_id in cart:
            product = Product.objects.get(id=product_id)
            item_subtotal = product.discount_price * cart[product_id]

        # Total cart price
        total_price = 0
        for pid, qty in cart.items():
            p = Product.objects.get(id=pid)
            total_price += p.discount_price * qty
            cart_count=len(cart)
            

        return JsonResponse({
            "quantity": cart.get(product_id, 0),
            "item_subtotal": item_subtotal,
            "total_price": total_price,
            "cart_count":cart_count,
        })


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    removed = False
    if product_id in cart:
        del cart[product_id]
        removed = True

    request.session["cart"] = cart

    # Recalculate total
    total_price = 0
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        total_price += product.discount_price * qty

    cart_count = len(cart)   # 👈 yaha rakho

    return JsonResponse({
        "removed": removed,
        "total_price": total_price,
        "cart_count": cart_count,
    })




def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            password=password1
        )
        user.save()

        return redirect("login")

    return render(request, "signup.html")





def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")   # change if needed
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "🚀 Product has been published successfully!")
            return redirect('add_product')  # Redirect to the same page after successful submission
        else:
            messages.error(request, "Please fix the errors below.")  # Show validation errors
    else:
        form = ProductForm()

    return render(request, "addProducts.html", {"form": form})

def showCart(request):
    return render(request,"cart.html")

# views.py
# views.py



from .models import Product

def place_order(request):
    if request.method != "POST":
        return redirect("cart")
    cart = request.session.get("cart", {})  # {product_id: quantity}

    if not cart:
        return redirect("cart")

    total = 0

    order = Order.objects.create(
        user=request.user,
        total_price=0,  # temporary, update later
        status="Placed"
    )

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

    # Update total after adding all items
    order.total_price = total
    order.save()

    # Clear session cart
    request.session["cart"] = {}

    return redirect("order_success")


def confirm_order(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect("cart")

    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0
    
    

    for product in products:
        qty = cart[str(product.id)]
        subtotal = product.discount_price * qty
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal,
             
            
        })

    return render(request, "confirm_order.html", {
        'cart_items': cart_items,
        'total_price': total_price,
        'user_profile': user_profile,
    })


def order_success(request):
    return render(request,"order_success.html")