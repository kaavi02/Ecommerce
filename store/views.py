from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import Product, CartItem, WishlistItem, Order, UserProfile

def seed_sample_products():
    """Populates default products with verified, high-availability image URLs."""
    if Product.objects.count() == 0:
        sample_items = [
            # --- SAREES ---
            {"name": "Traditional Kerala Kasavu Onam Saree", "category": "Saree", "price": 1299, "description": "Authentic white cotton Kasavu saree with rich gold zari border.", "image_url": "/static/images/img1.jpg"},
           {"name": "Golden Tissue Onam Kasavu Saree", "category": "Saree", "price": 1499, "description": "Lustrous golden tissue silk Kasavu saree with woven peacock motifs.", "image_url": "/static/images/img2.jpg"},
            {"name": "Handloom Cotton Onam Saree with Mural Art", "category": "Saree", "price": 1899, "description": "Handpainted Kerala mural design on pure off-white cotton fabric.", "image_url": "/static/images/img3.jpg"},
            {"name": "Cotton Silk Red Saree", "category": "Saree", "price": 899, "description": "Elegant traditional saree with rich woven gold border.", "image_url": "/static/images/img4.jpg"},
            {"name": "Printed Georgette Saree", "category": "Saree", "price": 699, "description": "Lightweight casual floral printed saree for daily wear.", "image_url": "/static/images/img5.jpg"},
            {"name": "Kanjeevaram Soft Silk Saree", "category": "Saree", "price": 2499, "description": "Royal temple border silk saree with broad contrast pallu.", "image_url": "/static/images/img6.jpg"},
            {"name": "Banarasi Art Silk Saree", "category": "Saree", "price": 1999, "description": "Intricate golden brocade work saree for wedding ceremonies.", "image_url": "/static/images/img7.jpg"},
            {"name": "Chiffon Floral Printed Saree", "category": "Saree", "price": 799, "description": "Breezy pastel green chiffon saree with matching blouse piece.", "image_url": "/static/images/img8.jpg"},

            # --- KURTAS & SHORT KURTIS ---
            {"name": "Cotton Anarkali Kurti", "category": "Kurtha Set", "price": 950, "description": "Floral printed ethnic flared long kurti.", "image_url": "/static/images/img9.jpg"},
            {"name": "Short Chikankari Cotton Kurti", "category": "Kurtha Set", "price": 649, "description": "White hand-embroidered short kurti for casual denim pairing.", "image_url": "/static/images/img10.jpg"},
            {"name": "Printed Short Tunic Kurti", "category": "Kurtha Set", "price": 499, "description": "Boho floral printed short kurti with bell sleeves.", "image_url": "/static/images/img11.jpg"},
            {"name": "Straight Kurti & Dupatta", "category": "Kurtha Set", "price": 749, "description": "Designer printed straight kurti set with matching dupatta.", "image_url": "/static/images/img12.jpg"},

            # --- JEANS ---
            {"name": "High-Waist Wide-Leg Jeans", "category": "Jeans", "price": 1299, "description": "Trendy baggy fit high-rise blue denim jeans.", "image_url": "/static/images/img13.jpg"},
            {"name": "Straight Fit Black Jeans", "category": "Jeans", "price": 1199, "description": "Fade-resistant solid black denim jeans.", "image_url": "/static/images/img14.jpg"},

            # --- MAKEUP ---
            {"name": "Matte Lipstick Combo", "category": "Makeup", "price": 499, "description": "Long-lasting waterproof matte liquid lipsticks set.", "image_url": "/static/images/img15.jpg"},
            {"name": "Mascara & Eyeliner Kit", "category": "Makeup", "price": 349, "description": "Smudge-proof eye makeup combination set.", "image_url": "/static/images/img16.jpg"},
            {"name": "Nude Eyeshadow Palette", "category": "Makeup", "price": 699, "description": "12-color shimmer and matte eyeshadow palette.", "image_url": "static/images/img17.jpg"},

            # --- ELECTRONICS ---
            {"name": "Wireless Earbuds", "category": "Electronics", "price": 999, "description": "Noise isolating Bluetooth earphones with deep bass.", "image_url": "/static/images/img18.jpg"},
            {"name": "Smart Fitness Band", "category": "Electronics", "price": 850, "description": "Real-time heart rate and step tracker watch.", "image_url": "/static/images/img19.jpg"},

            # --- FOOTWEAR & JEWELLERY ---
            {"name": "Flat Ethnic Sandals", "category": "Sandals", "price": 450, "description": "Comfortable embroidered flat slip-on sandals.", "image_url": "/static/images/img20.jpg"},
            {"name": "Kundan Necklace Set", "category": "Jewellery", "price": 899, "description": "Traditional gold-plated ethnic necklace & earrings.", "image_url": "/static/images/img21.jpg"}
        ]

        for item in sample_items:
            Product.objects.create(**item)

# ================================
# STOREFRONT VIEWS
# ================================

def home(request):
    seed_sample_products()
    search_query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()
    sort_option = request.GET.get('sort', '').strip()

    products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)

    if selected_category:
        products = products.filter(category=selected_category)

    if sort_option == 'high_low':
        products = products.order_by('-price')
    elif sort_option == 'low_high':
        products = products.order_by('price')

    categories = ['Saree', 'Kurtha Set', 'Jeans', 'Makeup', 'Electronics', 'Sandals', 'Jewellery']

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
        'sort_option': sort_option
    }
    return render(request, 'home.html', context)

def products_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def about(request):
    return render(request, 'about.html')

# ================================
# CART & WISHLIST VIEWS
# ================================

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    WishlistItem.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"'{product.name}' added to your Cart!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total})

@login_required
def update_cart_quantity(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f"'{product.name}' added to Wishlist!")
    return redirect('wishlist')

@login_required
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})

@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    wishlist_item.delete()
    messages.success(request, "Item removed from wishlist.")
    return redirect('wishlist')

# ================================
# CHECKOUT & PAYMENT VIEWS
# ================================

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_amount': total})

@login_required
def process_payment(request):
    if request.method == "POST":
        mode = request.POST.get('payment_mode')
        full_name = request.POST.get('full_name', request.user.username)
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        pincode = request.POST.get('pincode', '')

        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.product.price * item.quantity for item in cart_items)
        product_names = ", ".join([item.product.name for item in cart_items])
        
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('home')

        status = "Paid" if mode == "ONLINE" else "Pending (COD)"
        order = Order.objects.create(
            user=request.user, 
            total_amount=total, 
            payment_mode=mode, 
            payment_status=status
        )
        cart_items.delete()

        context = {
            'order': order,
            'full_name': full_name,
            'phone': phone,
            'address': address,
            'city': city,
            'state': state,
            'pincode': pincode,
            'product_names': product_names,
            'total_amount': total,
            'mode': mode,
            'delivery_time': "3 - 5 Business Days"
        }
        
        return render(request, 'order_success.html', context)
    return redirect('checkout')

# ================================
# AUTHENTICATION & SECURITY VIEWS
# ================================

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username', '').strip()
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username', '').strip()
        p = request.POST.get('password')
        cp = request.POST.get('confirm_password')
        q = request.POST.get('question')
        a = request.POST.get('answer', '').strip()

        if len(p) < 8:
            messages.error(request, "Password should be at least 8 characters long.")
            return render(request, 'register.html')

        if p != cp:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        final_username = u
        count = 1
        while User.objects.filter(username__iexact=final_username).exists():
            final_username = f"{u}{count}"
            count += 1

        try:
            user = User.objects.create_user(username=final_username, password=p)
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'security_question': q, 'security_answer': a}
            )

            messages.success(request, f"Registration successful! Your username is '{final_username}'. Please log in.")
            return redirect('login')

        except Exception as e:
            messages.error(request, "An error occurred during registration. Please try again.")
            return render(request, 'register.html')

    return render(request, 'register.html')

def forgot_password_view(request):
    if request.method == 'POST':
        u = request.POST.get('username', '').strip()
        q = request.POST.get('question')
        ans = request.POST.get('answer', '').strip()
        new_p = request.POST.get('new_password')
        conf_p = request.POST.get('confirm_password')

        if len(new_p) < 8:
            messages.error(request, "Password should be at least 8 characters long.")
            return render(request, 'forgot_password.html')

        if new_p != conf_p:
            messages.error(request, "New passwords do not match.")
            return render(request, 'forgot_password.html')

        try:
            user = User.objects.get(username__iexact=u)
            profile = UserProfile.objects.get(user=user)
            
            if profile.security_question == q and profile.security_answer.lower() == ans.lower():
                user.set_password(new_p)
                user.save()
                messages.success(request, "Password reset successful! Please log in.")
                return redirect('login')
            else:
                messages.error(request, "Incorrect security question or answer.")
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, "Invalid username or security profile.")

    return render(request, 'forgot_password.html')

def user_logout(request):
    logout(request)
    return redirect('home')