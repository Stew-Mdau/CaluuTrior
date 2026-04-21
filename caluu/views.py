from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, CartItem
from .forms import OrderForm, ProductForm, RegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import uuid

# --- HELPER: EMAIL SENDER ---
def send_caluu_email(subject, message, recipient_list):
    try:
        send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL,
            recipient_list, fail_silently=True,
        )
    except Exception:
        pass

# --- 1. AUTH & PRODUCT LIST ---
def product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'product_list.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_caluu_email('Welcome!', f'Hi {user.username}, account ready.', [user.email])
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# --- 2. SHOPPING & CART ---
@login_required
def add_to_cart(request, product_id):
    if request.user.is_staff: return redirect('product_list')
    product = get_object_or_404(Product, id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        if product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Updated {product.name} quantity.")
        else:
            messages.error(request, f"Only {product.stock} units available.")
    else:
        messages.success(request, f"{product.name} added to cart.")
    
    referer = request.META.get('HTTP_REFERER')
    return redirect('view_cart' if referer and 'cart' in referer else 'product_list')

@login_required
def view_cart(request):
    if request.user.is_staff: return redirect('seller_orders')
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def reduce_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    get_object_or_404(CartItem, id=item_id, user=request.user).delete()
    return redirect('view_cart')

# --- 3. THE FIXED CHECKOUT (Links to Payment) ---


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('product_list')

    # Generate ONE ID for the whole cart
    t_id = str(uuid.uuid4().hex[:10].upper()) 
    last_order_id = None

    for item in cart_items:
        if item.quantity <= item.product.stock:
            order = Order.objects.create(
                customer=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.total_price(),
                payment_status="Pending",
                transaction_id=t_id  # <--- Apply the same ID to all items
            )
            item.product.stock -= item.quantity
            item.product.save()
            last_order_id = order.id
        else:
            messages.error(request, f"Stock error for {item.product.name}.")
            return redirect('view_cart')

    cart_items.delete()
    
    if last_order_id:
        messages.success(request, f"Orders placed! Transaction ID: {t_id}")
        return redirect('payment_page', order_id=last_order_id)
    return redirect('my_orders')

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > product.stock:
                form.add_error('quantity', f"Only {product.stock} available.")
            else:
                # AMENDMENT: Generate a Transaction ID for Buy Now
                t_id = str(uuid.uuid4().hex[:10].upper()) 
                
                order = Order.objects.create(
                    customer=request.user, 
                    product=product, 
                    quantity=quantity,
                    total_price=product.price * quantity, 
                    payment_status="Pending",
                    transaction_id=t_id  # <--- Added this
                )
                product.stock -= quantity
                product.save()
                return redirect('payment_page', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'place_order.html', {'form': form, 'product': product})

# --- 4. PAYMENTS & ORDERS ---
@login_required
def payment_page(request, order_id):
    # Use .filter().first() instead of get_object_or_404 to see if it exists at all
    main_order = Order.objects.filter(id=order_id, customer=request.user).first()
    
    # If the specific ID in the URL is missing, grab the most recent pending order for this user
    if not main_order:
        main_order = Order.objects.filter(customer=request.user, payment_status='Pending').order_by('-id').first()

    # If still nothing, then redirect to shop
    if not main_order:
        messages.error(request, "Order not found or already processed.")
        return redirect('product_list')

    # GROUP LOGIC: Fetch all products with the same transaction_id
    if main_order.transaction_id:
        batch_orders = Order.objects.filter(
            transaction_id=main_order.transaction_id,
            customer=request.user
        ).exclude(payment_status='Cancelled')
    else:
        # If no transaction_id exists (old orders), just show the single order
        batch_orders = Order.objects.filter(id=main_order.id)

    total_to_pay = sum(item.total_price for item in batch_orders)

    return render(request, 'payment_page.html', {
        'main_order': main_order,
        'orders': batch_orders, # This displays all products in the cart together
        'total_to_pay': total_to_pay,
        'payment_number': '351085376',
        'help_whatsapp': '255627137665'
    })

@login_required
def notify_payment(request, order_id):
    # 1. Get the specific order the user clicked 'Paid' on
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    if request.method == "POST":
        # 2. Update ALL products that belong to this transaction
        updated_count = Order.objects.filter(
            transaction_id=order.transaction_id,
            customer=request.user,
            payment_status='Pending'
        ).update(payment_status='Paid')

        messages.success(request, f"Notification sent for all {updated_count} products in this order.")
    
    return redirect('payment_page', order_id=order.id)

@login_required
def notify_batch_payment(request):
    if request.method == "POST":
        ids = request.POST.get('order_ids', '').split(',')
        Order.objects.filter(id__in=[i.strip() for i in ids if i.strip()], customer=request.user).update(payment_status="Paid")
        messages.success(request, "Bulk payment reported.")
    return redirect('my_orders')

@login_required
def cancel_order(request, order_id):
    main_order = get_object_or_404(Order, id=order_id)
    
    if main_order.customer != request.user and not request.user.is_staff:
        return redirect('my_orders')
    
    # AMENDMENT: Get the whole batch by transaction_id
    if main_order.transaction_id:
        batch = Order.objects.filter(transaction_id=main_order.transaction_id)
    else:
        batch = Order.objects.filter(id=main_order.id)

    for order in batch:
        if order.payment_status not in ["Completed", "Cancelled"]:
            p = order.product
            p.stock += order.quantity
            p.save()
            order.payment_status = "Cancelled"
            order.save()
            
    messages.warning(request, "Transaction cancelled and stock returned.")
    
    if not request.user.is_staff:
        return redirect('product_list')
    return redirect('seller_orders')

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    p = order.product
    p.stock += order.quantity
    p.save()
    order.delete()
    return redirect('place_order', product_id=p.id)

@login_required
def my_orders(request):
    if request.user.is_staff: return redirect('seller_orders')
    orders = Order.objects.filter(customer=request.user).order_by('-id')
    pending = orders.filter(payment_status="Pending")
    total_to_pay = pending.aggregate(Sum('total_price'))['total_price__sum'] or 0
    pending_ids = ", ".join([str(o.id) for o in pending])
    return render(request, 'my_orders.html', {
        'orders': orders, 'total_to_pay': total_to_pay, 'payment_number': '351085376', 'pending_ids': pending_ids
    })

# --- 5. SELLER MANAGEMENT ---
@user_passes_test(lambda u: u.is_staff)
def seller_orders(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'seller_order.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # AMENDMENT: If it's part of a batch, confirm the whole batch
    if order.transaction_id:
        Order.objects.filter(transaction_id=order.transaction_id).update(
            payment_status="Completed", 
            is_confirmed=True
        )
        messages.success(request, f"Batch {order.transaction_id} confirmed!")
    else:
        # Fallback for single items without an ID
        order.payment_status, order.is_confirmed = "Completed", True
        order.save()
        messages.success(request, "Order confirmed.")
        
    return redirect('seller_orders')

@user_passes_test(lambda u: u.is_staff)
def confirm_all_orders(request, customer_id):
    customer = get_object_or_404(User, id=customer_id)
    Order.objects.filter(customer=customer, payment_status='Paid').update(payment_status='Completed', is_confirmed=True)
    return redirect('seller_orders')

@login_required
def confirm_payment_seller(request, order_id):
    # Seller clicks 'Confirm' on any product in the batch
    order = get_object_or_404(Order, id=order_id)
    
    # Update the status for the entire group of products
    Order.objects.filter(transaction_id=order.transaction_id).update(
        payment_status='Confirmed',
        is_confirmed=True
    )
    
    messages.success(request, f"Transaction {order.transaction_id} fully confirmed!")
    return redirect('seller_dashboard')

@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'add_product.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def update_product(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=p)
    if form.is_valid():
        form.save()
        messages.success(request, f"{p.name} updated successfully!")
        return redirect('product_list')
    return render(request, 'update_product.html', {'form': form, 'product': p})

@user_passes_test(lambda u: u.is_staff)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.warning(request, "Product deleted.")
    return redirect('product_list')