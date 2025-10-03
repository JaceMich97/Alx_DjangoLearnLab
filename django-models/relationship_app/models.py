from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Author(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self): return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    class Meta:
        permissions = (
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        )
    def __str__(self): return f"{self.title} by {self.author.name}"

class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='libraries', blank=True)
    def __str__(self): return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, related_name='librarian', on_delete=models.CASCADE)
    def __str__(self): return f"{self.name} ({self.library.name})"

class UserProfile(models.Model):
    ROLE_CHOICES = (('Admin','Admin'),('Librarian','Librarian'),('Member','Member'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    def __str__(self): return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created: UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try: instance.userprofile.save()
    except UserProfile.DoesNotExist: UserProfile.objects.create(user=instance)
