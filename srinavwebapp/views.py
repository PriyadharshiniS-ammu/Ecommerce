from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator

from .models import User, Product, Category, Cart, CartItem, Order, OrderItem, Review
from .forms import (
    AddToCartForm, CheckoutForm, ReviewForm, 
    ProductFilterForm, SignUpForm, LoginForm, SellerProductForm
)


def homepage(request):
    """Display homepage with featured products"""
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]
    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'homepage.html', context)


def product_list(request):
    """Display all products with filtering and search"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Filtering
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort_by', '-created_at')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    valid_sorts = ['-created_at', 'created_at', 'price', '-price', 'name']
    if sort_by in valid_sorts:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'product_list.html', context)


def product_detail(request, product_id):
    """Display product detail page with reviews"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    add_to_cart_form = AddToCartForm()
    review_form = ReviewForm()
    
    # Check if user has already reviewed
    user_review = None
    if request.user.is_authenticated and request.user.is_buyer():
        user_review = reviews.filter(buyer=request.user).first()
    
    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_buyer():
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.buyer = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('product_detail', product_id=product_id)
    
    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'review_count': reviews.count(),
        'add_to_cart_form': add_to_cart_form,
        'review_form': review_form,
        'user_review': user_review,
    }
    return render(request, 'product_detail.html', context)


@require_POST
@login_required(login_url='login')
def add_to_cart(request, product_id):
    """Add product to cart"""
    # Only buyers can add to cart
    if not request.user.is_buyer():
        messages.error(request, 'Only buyers can add items to cart.')
        return redirect('product_detail', product_id=product_id)
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    form = AddToCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        
        # Get or create user's cart
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{product.name} added to cart!')
        return redirect('view_cart')
    
    return redirect('product_detail', product_id=product_id)


@login_required(login_url='login')
def view_cart(request):
    """View shopping cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)


@require_POST
@login_required(login_url='login')
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    quantity = request.POST.get('quantity')
    if quantity:
        try:
            quantity = int(quantity)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated!')
            else:
                cart_item.delete()
                messages.success(request, 'Item removed from cart!')
        except ValueError:
            messages.error(request, 'Invalid quantity!')
    
    return redirect('view_cart')


@require_POST
@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('view_cart')


@login_required(login_url='login')
def checkout(request):
    """Checkout page"""
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.warning(request, 'Your cart is empty!')
            return redirect('view_cart')
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty!')
        return redirect('view_cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            
            # Calculate totals
            subtotal = cart.get_total_price()
            tax = subtotal * 0.1  # 10% tax
            shipping_cost = 50 if subtotal > 0 else 0  # Free shipping over certain amount
            total = subtotal + tax + shipping_cost
            
            order.subtotal = subtotal
            order.tax = tax
            order.shipping_cost = shipping_cost
            order.total_price = total
            order.save()
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                # Update product stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_confirmation.html', context)


@login_required(login_url='login')
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(buyer=request.user).prefetch_related('items')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'orders': page_obj.object_list,
    }
    return render(request, 'order_history.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_detail.html', context)


def signup(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()
            
            # Create cart only for buyers
            if user.is_buyer():
                Cart.objects.create(user=user)
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    
    context = {'form': form}
    return render(request, 'signup.html', context)


def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        if request.user.is_seller():
            return redirect('seller_dashboard')
        else:
            return redirect('homepage')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!')
                    
                    # Ensure buyer has cart
                    if user.is_buyer():
                        Cart.objects.get_or_create(user=user)
                        return redirect('homepage')
                    else:
                        return redirect('seller_dashboard')
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('homepage')


@login_required(login_url='login')
def profile(request):
    """User profile page"""
    orders = Order.objects.filter(buyer=request.user).count()
    
    context = {
        'user': request.user,
        'orders_count': orders,
    }
    return render(request, 'profile.html', context)


# ============ SELLER VIEWS ============

def seller_only(function):
    """Decorator to ensure only sellers can access"""
    @login_required(login_url='login')
    def wrap(request, *args, **kwargs):
        if not request.user.is_seller():
            messages.error(request, 'This page is only for sellers.')
            return redirect('homepage')
        return function(request, *args, **kwargs)
    return wrap


@seller_only
def seller_dashboard(request):
    """Seller dashboard"""
    seller = request.user
    products = Product.objects.filter(seller=seller)
    orders = OrderItem.objects.filter(product__seller=seller)
    
    total_products = products.count()
    total_orders = orders.count()
    total_revenue = sum(item.product.price * item.quantity for item in orders)
    
    context = {
        'seller': seller,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'products': products[:5],
        'orders': orders[:5],
    }
    return render(request, 'seller_dashboard.html', context)


@seller_only
def seller_products(request):
    """View seller's products"""
    seller = request.user
    products = Product.objects.filter(seller=seller).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
    }
    return render(request, 'seller_products.html', context)


@seller_only
def seller_add_product(request):
    """Add new product"""
    categories = Category.objects.all()
    if request.method == 'POST':
        form = SellerProductForm(request.POST, request.FILES, categories=categories)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('seller_products')
    else:
        form = SellerProductForm(categories=categories)
    
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'seller_add_product.html', context)


@seller_only
def seller_edit_product(request, product_id):
    """Edit product"""
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = SellerProductForm(request.POST, request.FILES, instance=product, categories=categories)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('seller_products')
    else:
        form = SellerProductForm(instance=product, categories=categories)
    
    context = {'form': form, 'product': product, 'categories': categories}
    return render(request, 'seller_edit_product.html', context)


@seller_only
def seller_delete_product(request, product_id):
    """Delete product"""
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('seller_products')
    
    context = {'product': product}
    return render(request, 'seller_delete_product.html', context)


@seller_only
def seller_orders(request):
    """View orders for seller's products"""
    seller = request.user
    orders = OrderItem.objects.filter(product__seller=seller).select_related('order', 'product')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'orders': page_obj.object_list,
    }
    return render(request, 'seller_orders.html', context)
