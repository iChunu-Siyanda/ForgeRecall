from django.db import models

class Deck(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    deck = models.ForeignKey(Deck, related_name='cards', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    explanation = models.TextField(blank=True)

    interval = models.IntegerField(default=1)  #Days
    ease_factor = models.FloatField(default=2.5)
    repetitions = models.IntegerField(default=0)

    last_reviewed = models.DateTimeField(blank=True, null=True)
    next_review = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card in {self.deck.name}: {self.question[:50]}..."

    
class Review(models.Model):
    RATING_CHOICES = [
        (1, 'Hard'),
        (2, 'Medium'),
        (3, 'Easy'),
    ]
    card = models.ForeignKey(Card, related_name='reviews', on_delete=models.CASCADE)
    review_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=RATING_CHOICES)  

    def __str__(self):
        return f"{self.card.id} - {self.rating} at {self.review_at}"   

     

