# Django E-Commerce Project - Setup Guide

## Project Overview
This is a fully functional Django-based e-commerce web application with a complete UI using Bootstrap 5.

### Features
✅ User Authentication (Sign Up, Login, Logout)
✅ Product Catalog with Categories
✅ Shopping Cart Management
✅ Checkout System
✅ Order Management & History
✅ Product Reviews & Ratings
✅ Responsive Bootstrap UI
✅ Admin Dashboard for Product Management
✅ Search & Filter Functionality
✅ User Profiles

---

## Installation & Setup

### 1. Install Required Packages
```bash
pip install django pillow
```

### 2. Navigate to Project Directory
```bash
cd c:\Users\LEGION\OneDrive\Desktop\Priyadharshini\Django\ecommerce
```

### 3. Create Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### 5. Run Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

---

## Project Structure

```
ecommerce/
├── manage.py                          # Django management script
├── db.sqlite3                        # SQLite database
├── ecommerce/                        # Main project settings
│   ├── settings.py                  # Project settings
│   ├── urls.py                      # Main URL configuration
│   ├── wsgi.py                      # WSGI configuration
│   └── asgi.py                      # ASGI configuration
└── srinavwebapp/                    # Main app
    ├── models.py                    # Database models (Product, Category, Cart, Order, etc.)
    ├── views.py                     # View functions for all pages
    ├── forms.py                     # Django forms for user input
    ├── urls.py                      # App URL routing
    ├── admin.py                     # Django admin configuration
    ├── templates/                   # HTML templates
    │   ├── base.html               # Base template (navbar, footer)
    │   ├── homepage.html           # Home page
    │   ├── product_list.html       # Product listing with filters
    │   ├── product_detail.html     # Product detail page with reviews
    │   ├── cart.html               # Shopping cart
    │   ├── checkout.html           # Checkout form
    │   ├── order_confirmation.html # Order confirmation page
    │   ├── order_history.html      # User's order history
    │   ├── order_detail.html       # Detailed order view
    │   ├── login.html              # Login page
    │   ├── signup.html             # Sign up page
    │   └── profile.html            # User profile page
    └── static/                      # Static files (CSS, JS, Bootstrap)
        └── bootstrap/              # Bootstrap files
```

---

## Database Models

### 1. **Category**
- Store product categories

### 2. **Product**
- Product information (name, price, stock, description)
- Links to categories
- Image upload support

### 3. **Cart**
- One-to-one relationship with User
- Contains cart items

### 4. **CartItem**
- Individual items in the cart
- Links cart to products with quantity

### 5. **Order**
- Customer orders with shipping information
- Order status tracking
- Tax and shipping cost calculation

### 6. **OrderItem**
- Individual items in an order
- Stores price snapshot at time of order

### 7. **Review**
- Product reviews and ratings
- Links users to products

---

## Main Views & URLs

### Public Pages
- `/ ` → Homepage with featured products
- `/products/` → Product listing with filters & search
- `/products/<id>/` → Product detail page with reviews

### Authentication
- `/login/` → User login
- `/signup/` → User registration
- `/logout/` → Logout

### Shopping (Login Required)
- `/cart/` → View shopping cart
- `/add-to-cart/<id>/` → Add product to cart
- `/update-cart/<id>/` → Update cart item quantity
- `/remove-from-cart/<id>/` → Remove item from cart
- `/checkout/` → Checkout page

### Orders (Login Required)
- `/orders/` → User's order history
- `/orders/<id>/` → View specific order details
- `/order-confirmation/<id>/` → Order confirmation

### User Account (Login Required)
- `/profile/` → User profile page

---

## Admin Dashboard

Access the admin panel at **http://localhost:8000/admin**

### Admin Features
- Manage Products (Create, Update, Delete)
- Manage Categories
- View Orders & Order Items
- View Customer Information
- Manage Cart & Cart Items
- Moderate Reviews & Ratings

---

## How to Add Sample Products

1. Log in to the admin panel: http://localhost:8000/admin
2. Click on "Categories" and create some categories (Electronics, Fashion, Furniture, etc.)
3. Click on "Products" and create new products:
   - Fill in name, description, price, stock
   - Select a category
   - Set is_active to True
4. Products will now appear on the homepage and products page

---

## Key Features Explained

### 1. **Shopping Cart**
- Auto-creates cart for new users
- Add/remove items
- Update quantities
- Real-time price calculation (includes 10% tax + shipping)

### 2. **Checkout**
- Collects shipping information
- Calculates totals
- Creates order and order items
- Updates product stock
- Clears cart after order

### 3. **Product Reviews**
- Users can leave ratings (1-5 stars)
- Add review comments
- Shows average rating on product page
- One review per user per product

### 4. **Search & Filters**
- Search by product name or description
- Filter by category
- Filter by price range
- Sort by newest, price, name

### 5. **Order Management**
- Track order status
- View order history
- See order items and pricing
- Shipping address details

---

## Front-End Features

### Bootstrap 5 UI
- Fully responsive design
- Mobile-friendly navigation
- Beautiful card layouts
- Smooth transitions and hover effects

### Color Scheme
- Primary: Yellow (#FFC107)
- Dark: #212529
- Bootstrap components for consistency

### User Experience
- Clear navigation breadcrumbs
- Success/Error messages
- Loading states
- Pagination for long lists
- Form validation

---

## Security Features

- CSRF protection on all forms
- Login required decorators on sensitive views
- User-specific cart and order access
- Email validation on signup
- Password hashing with Django's auth system

---

## Customization Guide

### Change Store Name
Edit in `base.html` and `homepage.html`

### Change Colors
Edit CSS in `base.html` `:root` section

### Add More Product Fields
1. Add fields to `Product` model in `models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Update `product_detail.html` template

### Add Product Images
1. Install Pillow: `pip install pillow`
2. Create `media` folder in project root
3. Update `settings.py` with MEDIA configuration
4. Upload images through admin panel

---

## Troubleshooting

### Database Issues
```bash
# Delete db.sqlite3 and start fresh
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Issues
```bash
python manage.py collectstatic --noinput
```

### Port Already in Use
```bash
python manage.py runserver 8001  # Use different port
```

---

## Requirements

- Python 3.8+
- Django 5.2
- Pillow (for image handling)
- Bootstrap 5 (via CDN)
- Font Awesome Icons (via CDN)

---

## Next Steps

1. Run the development server
2. Create admin account
3. Add product categories in admin
4. Add sample products
5. Test the application
6. Customize colors and branding
7. Deploy to production (Heroku, AWS, etc.)

---

## Support & Contact

For questions or issues, contact: support@shopmart.com

Happy Shopping! 🛍️
