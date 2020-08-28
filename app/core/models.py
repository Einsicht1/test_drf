from django.db import models

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """create and saves a new user """
        if not email:
            raise ValueError("insufficient number of user fields")
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
    grade = models.ForeignKey("UserGrade", on_delete=models.SET_NULL, null=True)
    point = models.IntegerField(default=0)
    purchase_count = models.IntegerField(default=0)
    purchase_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    sell_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    recent_login = models.DateTimeField(auto_now=True, null=True, blank=True)
    sleep_expiration_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_approved = models.BooleanField(default=True)
    coupon = models.CharField(max_length=50, default=0)
    gender = models.CharField(max_length=50)
    bank_account = models.CharField(max_length=160, blank=True)
    social_platform = models.ForeignKey(
        "socialplatform",
        on_delete=models.SET_NULL,
        max_length=20,
        blank=True,
        null=True,
    )
    social_login_id = models.CharField(max_length=50, blank=True)
    login_fail_count = models.IntegerField(blank=True, default=0)
    is_lock = models.BooleanField(default=False)
    latest_try_login_date = models.DateTimeField(default=None, null=True)
    lock_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # brand = models.ManyToManyField("sell.brand", through="userbrand")
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
        verbose_name_plural = "회원관리"


class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20)

    class Meta:
        db_table = "social_platforms"


class Address(models.Model):
    name = models.CharField(max_length=2000, verbose_name="주소")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_default = models.NullBooleanField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "addresses"
        verbose_name_plural = "addresses"


class PhoneAuthorization(models.Model):
    phone_number = models.CharField(max_length=20)
    authorization_number = models.CharField(max_length=20)

    def __str__(self):
        return self.phone_number

    class Meta:
        db_table = "phone_authorizations"


class UserGrade(models.Model):
    grade = models.CharField(max_length=50)

    def __str__(self):
        return self.grade

    class Meta:
        db_table = "user_grades"
        verbose_name_plural = "회원등급"


class UserBrand(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)

    class Meta:
        db_table = "users_brands"


class Product(models.Model):
    product_code = models.CharField(max_length=500, blank=True, verbose_name="자체상품코드")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="브랜드")
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True)
    purchased_year = models.CharField(max_length=200, verbose_name="구매연도")
    purchased_where = models.CharField(max_length=200, verbose_name="구매처")
    purchased_price = models.CharField(max_length=200, verbose_name="구매 가격")
    wish_price = models.CharField(max_length=200, verbose_name="희망 가격")
    name = models.CharField(max_length=200, null=True, verbose_name="상품명")
    agreement = models.ForeignKey("Agreement", on_delete=models.SET_NULL, null=True)
    discount_percentage = models.IntegerField(null=True)
    product_grade = models.ForeignKey(
        "ProductGrade",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="상품 등급",
        blank=True,
    )
    commission = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="purchase.UserProduct"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="판매자",
    )
    tag = models.ManyToManyField("Tag", through="ProductTag")
    memo = models.CharField(max_length=2000, blank=True)
    related_product = models.ManyToManyField("self", through="RelatedProduct")
    category = models.ManyToManyField("SubCategory", through="ProductCategory")
    sell_category = models.ForeignKey(
        "SellCategory", on_delete=models.SET_NULL, null=True, verbose_name="카테고리"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="신청일자")
    keyword = models.ManyToManyField("Keyword", through="ProductKeyword")
    product_status = models.ForeignKey(
        "ProductStatus",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="상태",
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="판매 가격", null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products"
        verbose_name_plural = "상품 관리"


class Agreement(models.Model):
    agreement_1 = models.BooleanField()
    agreement_2 = models.BooleanField()
    agreement_3 = models.BooleanField()
    agreement_4 = models.BooleanField()

    def __str__(self):
        return "동의함"

    class Meta:
        db_table = "agreements"


class ProductDetail(models.Model):
    component = models.CharField(max_length=500, verbose_name="구성품", blank=True)
    material = models.CharField(max_length=500, verbose_name="소재", blank=True)
    made_in = models.CharField(max_length=500, verbose_name="원산지", blank=True)
    dimension = models.CharField(max_length=500, verbose_name="실측 단면", blank=True)
    size = models.CharField(max_length=500, verbose_name="사이즈", blank=True)
    model_name = models.CharField(max_length=500, verbose_name="모델명", blank=True)
    texture = models.CharField(max_length=500, verbose_name="재질", blank=True)
    color = models.CharField(max_length=500, verbose_name="대표색상", blank=True)
    condition = models.CharField(max_length=500, verbose_name="상태", blank=True)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = "products_details"


class Image(models.Model):
    image_url = models.ImageField(max_length=2000)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    is_damaged = models.BooleanField()

    def __str(self):
        return ""

    class Meta:
        db_table = "images"


class PriceHistory(models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="판매 가격")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name="상품명")
    created_at = models.DateTimeField(auto_now_add=True)
    discounted_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    is_uptodate = models.BooleanField(verbose_name="최신여부")

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = "price_histories"


class ProductGrade(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_grades"
        verbose_name_plural = "상품등급 관리"


class Consignment(models.Model):
    date = models.CharField(max_length=50, blank=True, verbose_name="수거 일시")
    pickup_time = models.ForeignKey(
        "PickupTime",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="수거 희망시간",
    )
    is_arrived = models.NullBooleanField(verbose_name="수거여부")
    is_pickup = models.BooleanField(verbose_name="방문수거 희망여부")
    address = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="주소",
    )
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return ""

    class Meta:
        db_table = "consignments"


class PickupTime(models.Model):
    time = models.CharField(max_length=50)

    def __str__(self):
        return self.time

    class Meta:
        db_table = "pickup_times"


class SellCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sell_categories"


class MainCategory(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "main_categories"


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    main_category = models.ForeignKey("MainCategory", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sub_categories"


class ProductCategory(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        "SubCategory", on_delete=models.CASCADE, verbose_name="카테고리"
    )

    class Meta:
        db_table = "products_categories"
        verbose_name_plural = "카테고리"


class BrandCategory(models.Model):
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    category = models.ForeignKey("SellCategory", on_delete=models.CASCADE)

    class Meta:
        db_table = "brands_categories"


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "tags"


class ProductTag(models.Model):
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    tag = models.ForeignKey("Tag", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "products_tags"


class Brand(models.Model):
    kor_name = models.CharField(max_length=50)
    kor_letters = models.CharField(max_length=50)
    eng_name = models.CharField(max_length=50)
    sell_category = models.ManyToManyField("SellCategory", through="BrandCategory")

    def __str__(self):
        return self.kor_name

    class Meta:
        db_table = "brands"
        verbose_name_plural = "브랜드 관리"


class ProductStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_status"
        verbose_name_plural = "product_status"


class ProductStatusLog(models.Model):
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    product_status = models.ForeignKey(
        "ProductStatus", on_delete=models.SET_NULL, null=True
    )
    time_elapsed = models.DateTimeField(null=True, blank=True)
    is_valid = models.BooleanField(null=True)

    def __str__(self):
        return ""

    class Meta:
        db_table = "product_status_log"
        verbose_name_plural = "상품 상태"


class SellStatistic(models.Model):
    total_price = models.DecimalField(max_digits=18, decimal_places=2)
    total_count = models.IntegerField()
    average_period = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sell_statistics"


class SellerReview(models.Model):
    comment = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "seller_reviews"


class RelatedProduct(models.Model):
    from_product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="to_product"
    )
    to_product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="from_product"
    )

    class Meta:
        db_table = "related_produtcs"


class Keyword(models.Model):
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "keywords"


class ProductKeyword(models.Model):
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    keyword = models.ForeignKey("Keyword", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "products_keywords"
