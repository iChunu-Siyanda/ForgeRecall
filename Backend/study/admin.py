from django.contrib import admin
from study.models import Card, Deck, Review

# Register your models here.
admin.site.register(Deck)
admin.site.register(Card)   
admin.site.register(Review)