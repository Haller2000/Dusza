from django.db import models
from .models import WorldCard, Dungeon, PlayerDeck, PlayerCards, Battle

class CardService:
    @staticmethod
    def get_player_collection(user):
        return PlayerCards.objects.filter(player=user).select_related('world_card')
    
    @staticmethod
    def get_available_dungeons_for_deck(deck):
        card_count = deck.deck_cards.count()
        return Dungeon.objects.annotate(
            card_count=models.Count('dungeon_cards')
        ).filter(card_count=card_count).select_related('leader_card')
    
    @staticmethod
    def get_player_active_deck(user):
        try:
            return PlayerDeck.objects.get(player=user, is_active=True)
        except PlayerDeck.DoesNotExist:
            return None
        
    def get_card_by_id(card_id):
        try:
            return WorldCard.objects.get(id=card_id)
        except WorldCard.DoesNotExist:
            return None