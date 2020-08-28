from django.db import models

# from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """create and saves a new user """
        if not email:
            raise ValueError("users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """create and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    # password = models.CharField(max_length=1000, blank=True)
    # grade = models.ForeignKey(
    # "usergrade", on_delete=models.set_null, null=True)
    point = models.IntegerField(default=0)
    purchase_count = models.IntegerField(default=0)
    purchase_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=0)
    sell_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=0)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    recent_login = models.DateTimeField(auto_now=True, null=True, blank=True)
    sleep_expiration_date = models.DateTimeField(
        auto_now=True, null=True, blank=True)
    is_approved = models.BooleanField(default=True)
    coupon = models.CharField(max_length=50, default=0)
    gender = models.CharField(max_length=50)
    bank_account = models.CharField(max_length=160, blank=True)
    # social_platform = models.ForeignKey(
    # "socialplatform", on_delete = models.set_null, max_length = 20,
    # blank = True, null = True)
    social_login_id = models.CharField(max_length=50, blank=True)
    login_fail_count = models.IntegerField(blank=True, default=0)
    is_lock = models.BooleanField(default=False)
    latest_try_login_date = models.DateTimeField(default=None, null=True)
    lock_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # brand = models.ManyToManyField("sell.brand", through="userbrand")
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    class meta:
        db_table = "users"
        verbose_name_plural = "회원관리"


"""
class socialplatform(models.Model):
    platform = models.CharField(max_length = 20, default = 0)

    class meta:
        db_table = "social_platforms"


class address(models.Model):
    name = models.CharField(max_length=2000, verbose_name="주소")
    user = models.ForeignKey(
        settings.auth_user_model, on_delete=models.cascade)
    is_default = models.nullBooleanField()

    def __str__(self):
        return self.name

    class meta:
        db_table = "addresses"
        verbose_name_plural = "addresses"


class phoneauthorization(models.Model):
    phone_number = models.CharField(max_length=20)
    authorization_number = models.CharField(max_length=20)

    def __str__(self):
        return self.phone_number

    class meta:
        db_table = "phone_authorizations"


class usergrade(models.Model):
    grade = models.CharField(max_length=50)

    def __str__(self):
        return self.grade

    class meta:
        db_table = "user_grades"
        verbose_name_plural = "회원등급"


class userbrand(models.Model):
    user  = models.ForeignKey(
        settings.auth_user_model, on_delete=models.cascade)
    brand = models.ForeignKey("sell.brand", on_delete=models.cascade)

    class meta:
        db_table = "users_brands"
"""
