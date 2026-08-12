"""
Quick verification script to check if the Django e-commerce project is set up correctly.
Run this after setting up the project: python check_setup.py
"""

import os
import sys
import django

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

try:
    django.setup()
    print("✓ Django setup successful")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    sys.exit(1)

# Check models
try:
    from srinavwebapp.models import Product, Category, Cart, CartItem, Order, OrderItem, Review
    print("✓ All models imported successfully")
    print("  - Product")
    print("  - Category")
    print("  - Cart")
    print("  - CartItem")
    print("  - Order")
    print("  - OrderItem")
    print("  - Review")
except Exception as e:
    print(f"✗ Model import failed: {e}")
    sys.exit(1)

# Check views
try:
    from srinavwebapp import views
    print("✓ Views imported successfully")
    print("  - homepage")
    print("  - product_list")
    print("  - product_detail")
    print("  - add_to_cart")
    print("  - view_cart")
    print("  - checkout")
    print("  - order_confirmation")
    print("  - order_history")
except Exception as e:
    print(f"✗ Views import failed: {e}")
    sys.exit(1)

# Check forms
try:
    from srinavwebapp.forms import (
        AddToCartForm, CheckoutForm, ReviewForm,
        ProductFilterForm, SignUpForm, LoginForm
    )
    print("✓ Forms imported successfully")
    print("  - AddToCartForm")
    print("  - CheckoutForm")
    print("  - ReviewForm")
    print("  - ProductFilterForm")
    print("  - SignUpForm")
    print("  - LoginForm")
except Exception as e:
    print(f"✗ Forms import failed: {e}")
    sys.exit(1)

# Check templates
templates = [
    'base.html', 'homepage.html', 'product_list.html',
    'product_detail.html', 'cart.html', 'checkout.html',
    'order_confirmation.html', 'order_history.html',
    'order_detail.html', 'login.html', 'signup.html', 'profile.html'
]

template_dir = 'srinavwebapp/templates'
if os.path.isdir(template_dir):
    existing_templates = []
    for template in templates:
        path = os.path.join(template_dir, template)
        if os.path.isfile(path):
            existing_templates.append(template)
    
    print(f"✓ Templates found ({len(existing_templates)}/{len(templates)})")
    for template in existing_templates:
        print(f"  - {template}")
else:
    print(f"✗ Templates directory not found: {template_dir}")
    sys.exit(1)

# Check database
try:
    from django.core.management import call_command
    from django.db import connection
    
    # Check if migrations are applied
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
    
    if len(tables) > 0:
        print(f"✓ Database initialized ({len(tables)} tables)")
    else:
        print("⚠ Database appears empty. Run: python manage.py migrate")
except Exception as e:
    print(f"⚠ Database check failed: {e}")

print("\n" + "="*50)
print("✓ Project setup verification complete!")
print("="*50)
print("\nNext steps:")
print("1. Create a superuser: python manage.py createsuperuser")
print("2. Run server: python manage.py runserver")
print("3. Visit: http://localhost:8000")
print("4. Admin: http://localhost:8000/admin")
