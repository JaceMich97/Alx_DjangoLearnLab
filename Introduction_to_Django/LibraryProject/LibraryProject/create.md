# Create
from django.contrib.auth.models import User
user = User.objects.create(username="john", email="john@example.com", password="test123")
print(user)