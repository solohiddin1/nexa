from django.db import models
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser


# Create your models here.

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam '+998XXXXXXXXX' formatida bo'lishi kerak!"
    )
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    name = models.BooleanField(default=False)
    email = models.EmailField(unique=True, default=None)
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.username else self.phone_number

    @property
    def is_superuser(self):
        return self.is_admin


# 2️⃣ CHAT MODEL
class Chat(models.Model):
    CHAT_TYPES = (
        ("private", "Private"),
        ("group", "Group"),
        ("channel", "Channel"),
    )
    type = models.CharField(max_length=10, choices=CHAT_TYPES)
    title = models.CharField(max_length=100, blank=True)
    members = models.ManyToManyField(User, related_name="chats", through="ChatMember")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"{self.type} chat #{self.id}"


class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default="member")  # admin, owner, etc.
    joined_at = models.DateTimeField(auto_now_add=True)


# 3️⃣ MESSAGE MODEL
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField(blank=True)
    media = models.FileField(upload_to="messages/media/", blank=True, null=True)
    reply_to = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Msg {self.id} from {self.sender}"


# 4️⃣ MESSAGE REACTION (optional)
class Reaction(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
