from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .userAuth import CustomAuthManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    hash = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True, default=0000)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "phone"]

    objects = CustomAuthManager()

    def __str__(self):
        return self.email


class ClientBusiness(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="client_profile",
        limit_choices_to={"is_staff": False},
    )
    business_name = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to="buyers/images/cafe_logos/", null=True, blank=True
    )
    account_number = models.CharField(max_length=50, unique=True)
    business_email = models.EmailField()
    business_phone = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)

    sales_rep = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_staff": True, "is_superuser": False},
        related_name="clients_handled",
    )

    account_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.business_name


class StaffProfile(models.Model):
    ROLE_CHOICES = [
        ("manager", "Manager"),
        ("sales_rep", "Sales Representative"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True, "is_superuser": False},
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.full_name} ({self.role})"


class ClientCataloge(models.Model):
    ORDER_FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("biweekly", "Every 15 Days"),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="client_catalog",
        limit_choices_to={"is_staff": False},
    )
    image = models.ImageField(
        upload_to="buyers/images/client_images/", null=True, blank=True
    )
    order_frequency = models.CharField(
        max_length=20, choices=ORDER_FREQUENCY_CHOICES, default="weekly"
    )
    pricing_enabled = models.BooleanField(default=False)
    default_cataloge = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email}'s Client Catalog"


class ClientAddress(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="client_address",
        limit_choices_to={"is_staff": False},
    )
    billing_address1 = models.TextField()
    billing_address2 = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_pincode = models.CharField(max_length=10)

    shipping_address1 = models.TextField(blank=True, null=True)
    shipping_address2 = models.TextField(blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_pincode = models.CharField(max_length=10, blank=True, null=True)

    shippingSameAsBilling = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} Address"
