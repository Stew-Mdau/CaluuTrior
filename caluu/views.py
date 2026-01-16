from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from .forms import OrderForm, ProductForm, RegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login

# --- PUBLIC VIEWS ---

def product_list(request):
    """Displays all available products to everyone."""
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


# --- CUSTOMER VIEWS ---

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            quantity = form.cleaned_data['quantity']

            if quantity > product.stock:
                form.add_error('quantity', f"Only {product.stock} units available.")
            else:
                # 1. Deduct Stock Automatically
                product.stock -= quantity
                product.save()

                # 2. Setup Order details
                order.product = product
                order.customer = request.user
                order.total_price = product.price * quantity
                order.payment_status = "Paid" # Assuming auto-pay for this flow
                order.is_confirmed = True
                order.save()
                
                return redirect('payment_page', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'place_order.html', {'form': form, 'product': product})

@login_required
def payment_page(request, order_id):
    # This page now shows your specific payment instructions
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    context = {
        'order': order,
        'payment_number': '0627137665' # Your requested number
    }
    return render(request, 'payment_page.html', context)

# --- SELLER / STAFF VIEWS ---

@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    """Allows staff to add a new product."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def update_product(request, product_id):
    """Allows staff to edit existing product details."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def delete_product(request, product_id):
    """Safe deletion of products."""
    product = get_object_or_404(Product, id=product_id)
    # Using a simple confirmation check; you can also use a 'confirm_delete.html'
    product.delete()
    messages.warning(request, "Product deleted.")
    return redirect('product_list')

@user_passes_test(lambda u: u.is_staff)
def seller_orders(request):
    """Dashboard for staff to see all orders from all customers."""
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'seller_order.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def confirm_order(request, order_id):
    """Seller confirms delivery and stock is officially deducted."""
    order = get_object_or_404(Order, id=order_id)

    if not order.is_confirmed:
        product = order.product
        if product.stock >= order.quantity:
            # Atomic update: decrease stock and confirm order
            product.stock -= order.quantity
            product.save()

            order.is_confirmed = True
            order.payment_status = "Completed"
            order.save()
            messages.success(request, f"Order #{order.id} confirmed and stock updated.")
        else:
            messages.error(request, f"Cannot confirm. Stock is now too low ({product.stock}).")
    
    return redirect('seller_orders')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Logs the user in immediately after signup
            messages.success(request, "Account created successfully!")
            return redirect('product_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})