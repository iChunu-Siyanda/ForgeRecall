from django.urls import path
from .views import due_cards, get_decks, review_card

urlpatterns = [
    path('due-cards/', due_cards, name='due_cards'),
    path('review-card/', review_card, name='review_card'),
    path('decks/', get_decks, name='get_decks'),
]