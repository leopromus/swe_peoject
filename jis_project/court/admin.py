from django.contrib import admin
from .models import User, CourtCase, Payment

admin.site.register(User)
admin.site.register(CourtCase)
admin.site.register(Payment)
