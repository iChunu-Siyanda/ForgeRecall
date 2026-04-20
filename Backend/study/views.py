from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .serializers import CardDetailSerializer, DeckSerializer, ReviewDetailSerializer
from .models import Card, Review

@api_view(['GET']) 
def due_cards(request): #Shows that you are about to forget these cards, so you should review them now. This is the main page of the app.
    # now = timezone.now()
    # cards = Card.objects.filter(next_review__lte=now)|Card.objects.filter(next_review__isnull=True)
    # cards = cards.order_by('next_review')[:20]  # Limit to 20 cards     
    # serializer = CardDetailSerializer(cards, many=True)
    deck_id = request.query_params.get('deck')
    cards = Card.objects.all()
    if deck_id:
        cards = cards.filter(deck_id=deck_id)
    cards = cards.filter(next_review__lte=timezone.now()) | cards.filter(next_review__isnull=True)
    cards = cards.order_by('next_review')[:20]  # Limit to 20 cards 
    serializer = CardDetailSerializer(cards, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_decks(request):
    decks = Card.objects.all()
    serializer = DeckSerializer(decks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def review_card(request):
    serializer = ReviewDetailSerializer(data=request.data)
    if serializer.is_valid():
        card_id = serializer.validated_data['card_id']
        rating = serializer.validated_data['rating']

        try:
            card = Card.objects.get(id=card_id)
        except Card.DoesNotExist:
            return Response({"error": "Card not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create the review
        review = Review.objects.create(card=card, rating=rating)

        # Update the card's spaced repetition data
        if rating == 3:  # Easy
            card.repetitions += 1
            card.ease_factor = max(1.3, card.ease_factor - 0.15)  # Decrease ease factor slightly
            card.interval = int(card.interval * card.ease_factor)  # Increase interval
        elif rating == 2:  # Medium
            card.repetitions += 1
            card.ease_factor = max(1.3, card.ease_factor)  # Keep ease factor the same
            card.interval = int(card.interval * card.ease_factor)  # Increase interval
        else:  # Hard
            card.repetitions = 0  # Reset repetitions on hard
            card.ease_factor = max(1.3, card.ease_factor + 0.15)  # Increase ease factor slightly
            card.interval = 1  # Reset interval to 1 day

        card.last_reviewed = timezone.now()
        card.next_review = timezone.now() + timezone.timedelta(days=card.interval)
        card.save()

        return Response({"message": "Review recorded successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)