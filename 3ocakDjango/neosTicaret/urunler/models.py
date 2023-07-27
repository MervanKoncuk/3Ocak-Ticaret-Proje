from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Satıcı")
    name = models.CharField(max_length=100, verbose_name="Ürün İsmi")
    content = models.TextField(verbose_name="Ürün Açıklaması")
    price = models.IntegerField(verbose_name="Ürün Fiyatı")
    image = models.ImageField(upload_to="products/", verbose_name="Ürün Resmi")
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace('ı', 'i'))
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ürünler"
        verbose_name = "Ürün"


class ShopCard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Ekleyen")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Eklenen Ürün")
    count = models.IntegerField(default=1, verbose_name='Adet')
    totalPrice = models.IntegerField(verbose_name="Toplam Fiyat")
    isPayment = models.BooleanField(default = False, verbose_name="Ödendi Mi?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = "Sepetteki Ürünler"
        verbose_name = "Sepet"
    
    def save(self, *args, **kwargs):
        self.totalPrice = self.product.price * self.count
        super(ShopCard, self).save(*args, **kwargs)


class Payment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Satın alan")
    products = models.ManyToManyField(ShopCard, verbose_name="Satın alınan ürünler")
    totalPrice = models.IntegerField(verbose_name="Toplam fiyat")
    isPayment = models.BooleanField(default = False, verbose_name="Ödendi Mi ?")

    def __str__(self):
        return self.owner.username
    
    
