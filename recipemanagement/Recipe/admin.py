from django.contrib import admin
from Recipe.models import recipe
from Recipe.models import review

admin.site.register(recipe)
admin.site.register(review)
