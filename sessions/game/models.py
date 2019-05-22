from django.db import models


class Player(models.Model):
    pass


class Game(models.Model):
    value = models.IntegerField()
    game_over = models.BooleanField(default=False)
    players = models.ManyToManyField(Player, related_name='games')


class PlayerGameInfo(models.Model):
    creator = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='creator', null=True, blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player', null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_info')
    counter = models.IntegerField(default=0)


