from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order, Review, CartItem, Product, Category


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=1000,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'max-width: 100px;',
        })
    )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country']
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your shipping address'
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'shipping_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'shipping_postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal Code'
            }),
            'shipping_country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i}★') for i in range(1, 6)], attrs={
                'class': 'form-check-input',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts about this product'
            }),
        }


class ProductFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price'
        })
    )
    
    def __init__(self, *args, **kwargs):
        from .models import Category
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    user_type = forms.ChoiceField(
        choices=User.USER_TYPES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    shop_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Shop Name (for sellers)'
    }))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'user_type', 'phone', 'shop_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class SellerProductForm(forms.ModelForm):
    category_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter category name',
            'list': 'category-list'
        })
    )

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock', 'image', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Product Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', None)
        super().__init__(*args, **kwargs)
        if categories is not None:
            self.fields['category_name'].widget.attrs['list'] = 'category-list'
            self.categories = categories
        else:
            self.categories = Category.objects.all()
        self.fields['category_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter category name',
            'list': 'category-list'
        })
        if self.instance and self.instance.pk:
            self.fields['category_name'].initial = self.instance.category.name

    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name', '').strip()
        if not category_name:
            raise forms.ValidationError('Category name is required.')
        return category_name

    def save(self, commit=True):
        category_name = self.cleaned_data.pop('category_name', '').strip()
        category = Category.objects.filter(name__iexact=category_name).first()
        if not category:
            category = Category.objects.create(name=category_name)
        instance = super().save(commit=False)
        instance.category = category
        if commit:
            instance.save()
        return instance

