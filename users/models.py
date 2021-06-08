from datetime import date

from django.db import models

from django.utils.html import escape

from django.utils.html import mark_safe

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.contenttypes.fields import GenericRelation

from hashlib import md5


def user_dir_path(instance, filename):
    return f'profile/user_{instance.id}/avatar/{filename}'


def user_photos_path(instance, filename):
    return f'profile/user_{instance.user_id.id}/photo_album/{filename}'


class UserManager(BaseUserManager):
    def create_user(self, email, login, password, token):
        user = self.model(
            login=login,
            email=self.normalize_email(email),
            created_at=date.today().strftime("%Y-%m-%d"),
            token=token
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    
    def create_superuser(self, login, password, token='', email=''):
        user = self.model(
            login=login,
            token=token,
            email=email,
            is_admin=True,
            is_active=True
        )
        
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    MALE = 'm'
    FEMALE = 'f'
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]

    login = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=254)
    full_name  = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
    status = models.CharField(max_length=150, null=True)
    avatar = models.ImageField(upload_to=user_dir_path, null=True, blank=True)
    created_at = models.DateField(null=True)
    last_login = models.DateField(null=True)
    token = models.CharField(max_length=500)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'login'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        super().save()

    def __str__(self):
        return f"{self.login} {self.email} {self.full_name}"


class UserPhotos(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE) 
    photo = models.ImageField(upload_to=user_photos_path, blank=True, null=True)


class Follower(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='From_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='To_user' )


class Blocked_user(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='from_user') 
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='to_user' )


class User_settings(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    dark_theme = models.BooleanField(default=False)


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Post(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    created_at = models.DateField()

    @property
    def total_likes(self):
        return self.liked.count()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Posts_photo(models.Model):
    post_id  = models.ForeignKey('Post', on_delete=models.CASCADE)
    photo = models.ImageField()


class Comment(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    photos = models.BooleanField(default=False)
    text = models.CharField(max_length=300) 


class Replies_on_comments(models.Model):
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE) 
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)   
    text = models.CharField(max_length=200)
    likes = models.IntegerField()