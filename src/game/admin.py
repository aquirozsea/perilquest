from django.contrib import admin

# Register your models here.
from game.models import Category, Game, Question, Match

admin.site.register(Game)
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Match)
