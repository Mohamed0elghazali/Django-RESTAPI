from django.contrib import admin
from .models import Guest, Movie, Reservation, Post

## SuperUser
## admin --- admin

## regularUser
## test --- dev12345

# Register your models here.
admin.site.register(Guest)
admin.site.register(Movie)
admin.site.register(Reservation)
admin.site.register(Post)