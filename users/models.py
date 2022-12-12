import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

ROLE_CHOICES = (
    ("admin", "Admin"),
    ("staff", "Staff"),
    ("editor", "Editor"),
    ("student", "Student"),
)

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$', message="Not an valid number")


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey(
        "auth.User", blank=True, related_name="creator_%(class)s_objects", on_delete=models.CASCADE)
    updater = models.ForeignKey("auth.User", blank=True, null=True,
                                related_name="updater_%(class)s_objects", on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Users(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    nationality = models.CharField(max_length=200)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    country = models.CharField(max_length=200)
    phone = models.CharField(max_length=10, validators=[phone_regex],)
    password = models.CharField(max_length=256)

    class Meta:
        db_table = 'users_users'
        verbose_name = ('Users')
        verbose_name_plural = ('Users')

    def __str__(self):
        return str(self.name)