from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

class Brand(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'brands'

    def get_absolute_url(self):
        return reverse('store:brand_list', args=[self.slug])

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True,)
    
    slug = models.SlugField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, related_name='product_brand', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    dataSheet = models.URLField(max_length = 250, null = True, blank = True, help_text = "www.example.com")
    tutorial = models.URLField(max_length = 250, null = True, blank = True, help_text = "www.example.com")
    slug = models.SlugField(max_length=255)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager() # The default manager.
    products = ProductManager() #Active Product manager

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    """
    The Product Image table.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    name = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(verbose_name=("image"),
        help_text=("Upload a product image"),
        upload_to="images/products",
        default="images/products/default.jpg",)
    alt_text = models.CharField(
        verbose_name=("Alturnative text"),
        help_text=("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Product Images'

    def get_absolute_url(self):
        return reverse('store:image_s_list', args=[self.slug])

    def __str__(self):
        return self.name

