# ShopMart - Django E-Commerce Application

A fully-featured, responsive e-commerce web application built with Django and Bootstrap 5.

## 🌟 Features

### Core E-Commerce Features
- 🛍️ **Product Catalog** - Browse products with detailed information
- 🏷️ **Categories** - Organize products by category
- 🔍 **Search & Filter** - Find products easily with advanced search and filtering
- ⭐ **Product Reviews** - Users can rate and review products (1-5 stars)
- 🛒 **Shopping Cart** - Add/remove items, update quantities
- 💳 **Checkout System** - Complete checkout with shipping information
- 📦 **Order Management** - Track orders and view order history
- 👤 **User Accounts** - Register, login, and manage profile

### Technical Features
- ✅ Responsive Bootstrap 5 UI
- ✅ User Authentication System
- ✅ Admin Dashboard for Product Management
- ✅ Real-time Cart Updates
- ✅ Order Status Tracking
- ✅ Database Models with Relationships
- ✅ Django Forms & Validation
- ✅ Security (CSRF Protection, Password Hashing)

---

## 📋 Requirements

- Python 3.8 or higher
- Django 5.2
- Pillow (for image handling)
- Modern web browser

---

## 🚀 Quick Start

### Option 1: Automated Setup (Windows)
```bash
setup.bat
```

### Option 2: Manual Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Create Database**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Create Admin Account**
```bash
python manage.py createsuperuser
```

4. **Run Development Server**
```bash
python manage.py runserver
```

5. **Access the Application**
- Main Site: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

---

## 📁 Project Structure

```
ecommerce/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── SETUP_GUIDE.md
├── README.md (this file)
├── setup.bat
│
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── srinavwebapp/
    ├── models.py          # Database models
    ├── views.py           # View functions
    ├── forms.py           # Django forms
    ├── urls.py            # URL routing
    ├── admin.py           # Admin configuration
    │
    ├── templates/
    │   ├── base.html
    │   ├── homepage.html
    │   ├── product_list.html
    │   ├── product_detail.html
    │   ├── cart.html
    │   ├── checkout.html
    │   ├── order_confirmation.html
    │   ├── order_history.html
    │   ├── order_detail.html
    │   ├── login.html
    │   ├── signup.html
    │   └── profile.html
    │
    └── static/
        └── bootstrap/    # Bootstrap files
```

---

## 🗄️ Database Models

### Product
- Name, Description, Price
- Category relationship
- Stock management
- Image support
- Active status

### Category
- Name and description
- Organizes products

### Cart
- One-to-one with User
- Contains cart items

### CartItem
- Links cart to products
- Quantity tracking

### Order
- User relationship
- Status tracking
- Shipping information
- Tax and shipping cost calculation

### OrderItem
- Items in an order
- Price snapshot

### Review
- Star rating (1-5)
- Comment
- User and product links

---

## 🔗 Main URLs

| URL | Purpose | Auth Required |
|-----|---------|---|
| `/` | Homepage | No |
| `/products/` | Product listing | No |
| `/products/<id>/` | Product detail | No |
| `/cart/` | View cart | Yes |
| `/checkout/` | Checkout | Yes |
| `/orders/` | Order history | Yes |
| `/orders/<id>/` | Order details | Yes |
| `/login/` | Login | No |
| `/signup/` | Register | No |
| `/profile/` | User profile | Yes |
| `/admin/` | Admin panel | Yes (Admin) |

---

## 🛠️ How to Use

### For Customers

1. **Browse Products**
   - Visit homepage to see featured products
   - Use search bar to find products
   - Filter by category and price range

2. **Product Details**
   - Click on product to view details
   - See customer reviews and ratings
   - Add your own review (after login)

3. **Shopping**
   - Click "Add to Cart"
   - Update quantities or remove items
   - Proceed to checkout

4. **Checkout**
   - Enter shipping address
   - Review order summary
   - Place order

5. **Track Orders**
   - View order history in account
   - Check order status
   - View order details

### For Administrators

1. **Access Admin Panel**
   - Go to http://localhost:8000/admin
   - Log in with superuser account

2. **Manage Products**
   - Create new products
   - Update product information
   - Manage stock
   - Delete products

3. **Manage Categories**
   - Create product categories
   - Organize products

4. **View Orders**
   - See all customer orders
   - Update order status
   - View customer information

5. **Manage Reviews**
   - Moderate product reviews
   - View ratings

---

## 🎨 Customization

### Change Store Name
Edit in templates:
- `base.html` - Navbar brand
- `homepage.html` - Hero section

### Change Colors
Edit CSS variables in `base.html`:
```css
:root {
    --primary-color: #FFC107;
    --dark-color: #212529;
}
```

### Add Product Images
1. Create `media` folder in project root
2. Update `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
3. Upload images through admin panel

---

## 🔒 Security Features

- ✅ CSRF Protection on all forms
- ✅ Password hashing with Django's auth system
- ✅ SQL injection prevention (ORM)
- ✅ Login required decorators
- ✅ User-specific data access
- ✅ Email validation

---

## 📊 Features Breakdown

### Shopping Cart System
- **Add Items**: Click "Add to Cart" with quantity
- **Update**: Change quantity directly
- **Remove**: Delete items from cart
- **Auto Calculation**: Real-time price updates

### Checkout System
- **Shipping Information**: Address, city, state, postal code
- **Tax Calculation**: 10% tax on subtotal
- **Shipping Cost**: $50 flat rate
- **Order Creation**: Automatic order and order items generation
- **Stock Update**: Product stock decreases on order

### Review System
- **Rating**: 1-5 star system
- **Comments**: Text-based product feedback
- **Average Rating**: Displayed on product page
- **One Per User**: Prevents duplicate reviews

### Order Management
- **Status Tracking**: Pending, Processing, Shipped, Delivered, Cancelled
- **Order History**: All user orders in one place
- **Order Details**: Complete order information
- **Date Tracking**: Order date and updates

---

## 🐛 Troubleshooting

### Issue: "Port Already in Use"
```bash
python manage.py runserver 8001  # Use port 8001
```

### Issue: Database Errors
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Issue: Form Validation Errors
- Check form requirements in admin panel
- Ensure all required fields are filled
- Check email format if registration fails

---

## 📝 Example: Adding a Product

1. Go to **Admin Panel** (http://localhost:8000/admin)
2. Click on **Products**
3. Click **Add Product**
4. Fill in the form:
   - **Name**: Wireless Headphones
   - **Description**: Premium quality wireless headphones
   - **Category**: Electronics
   - **Price**: 2499
   - **Stock**: 50
   - **Is Active**: ✓ Checked
5. Click **Save**

---

## 🌐 Deployment

For production deployment, refer to Django's deployment guide:
https://docs.djangoproject.com/en/5.2/howto/deployment/

Popular options:
- Heroku
- AWS
- PythonAnywhere
- DigitalOcean
- Render

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/)
- [Font Awesome Icons](https://fontawesome.com/icons/)

---

## 📧 Support

For issues or questions:
1. Check the SETUP_GUIDE.md
2. Review Django documentation
3. Contact support@shopmart.com

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🎉 Enjoy Your E-Commerce Platform!

Happy selling! If you find this useful, please consider starring the project.

**Last Updated**: June 2024
**Django Version**: 5.2.14
**Python Version**: 3.8+
