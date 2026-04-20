from rest_framework import serializers
from .models import Deck, Card, Review  

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ["id", "name", "description", "created_at"]

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["id",
                  "deck", 
                  "question", 
                  "answer", 
                  "explanation", 
                  "interval", 
                  "ease_factor", 
                  "repetitions", 
                  "last_reviewed", 
                  "next_review", 
                  "created_at"
                  ]  

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "card", "review_at", "rating"]
        read_only_fields = ["review_at"]  # review_at is auto_now_add, so it's read-only    

class CardDetailSerializer(serializers.ModelSerializer): #Usable for GET /cards/{id}/. In the UX Card
    deck_name = serializers.CharField(source='deck.name', read_only=True)   

    class Meta:
        model = Card
        fields = ["id",
                  "question", 
                  "answer", 
                  "explanation",  
                  "next_review", 
                  "deck_name",
                  ]   

class ReviewDetailSerializer(serializers.ModelSerializer): #Usable for GET /reviews/{id}/. In the UX Review
    card_id = serializers.IntegerField(source='card.id')
    rating = serializers.IntegerField()  # Get the display value of the rating

    def validate_rating(self, value):
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("Rating must be 1 (Hard), 2 (Medium), or 3 (Easy).")
        return value