from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='tteesstt@test.com', password='testpass',
                phone_number = '01055525672', name = "kim", gender='남성'):
    """Create a sample user"""
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
        phone_number=phone_number,
        name=name,
        gender=gender
   )
    return user

def sample_grade():
    return models.UserGrade.objects.create(grade="일반회원")

def sample_social_platform():
    return models.SocialPlatform.objects.create(platform="카카오")


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Password123'
        phone_number= '01055525672'
        name= "kim"
        gender= '남성'
        user = get_user_model().objects.create_user(email,
                                                    password=password,
                                                    phone_number=phone_number,
                                                    name=name,
                                                    gender=gender)

        self.assertEqual(user.email, email)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.name, name)
        self.assertEqual(user.gender, gender)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@SEOULAPPDEV.COM"
        password = 'Password123'
        phone_number = '01055525672'
        name = "kim"
        gender='남성'
        user = get_user_model().objects.create_user(email,
                                                    password=password,
                                                    phone_number=phone_number,
                                                    name=name,
                                                    gender=gender)


        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@seoulappdev.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_grade_successful(self):
        grade_1 = models.UserGrade.objects.create(
            grade = '일반회원')

        self.assertEqual(str(grade_1), grade_1.grade)

    def test_create_phone_authorization_successful(self):
        phone_number = '01050318756',
        authorization_number = '1234'

        phone_auth = models.PhoneAuthorization.objects.create(
            phone_number = phone_number,
            authorization_number = authorization_number
        )

        self.assertEqual(phone_auth.phone_number, phone_number)
        self.assertEqual(phone_auth.authorization_number, authorization_number)

    def test_create_social_paltform_successful(self):
        platform = "apple"
        social_platform = models.SocialPlatform.objects.create(
            platform = platform)

        self.assertEqual(social_platform.platform, platform)

    def test_create_address_successful(self):
        name = "서울시 뱅뱅사거리",
        #user= sample_user(),
        is_default = True
        user = sample_user()
        address = models.Address.objects.create(
            name = name,
            user= user,
            is_default = is_default)

        self.assertEqual(address.name, name)
        self.assertEqual(address.user, user)
        self.assertEqual(address.is_default, is_default)

    def test_create_user_with_foreignkey_fields_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Password123'
        phone_number= '01055525672'
        name= "kim"
        gender= '남성'
        grade = sample_grade()
        social_platform = sample_social_platform()
        user = get_user_model().objects.create_user(email,
                                                    password=password,
                                                    phone_number=phone_number,
                                                    name=name,
                                                    gender=gender,
                                                    grade=grade,
                                                    social_platform=social_platform)

        self.assertEqual(user.social_platform, social_platform)
        self.assertEqual(user.grade, grade)
