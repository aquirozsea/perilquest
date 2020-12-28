from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):

    RELATED_NAME = 'questions'

    category = models.ForeignKey(Category, related_name=RELATED_NAME, on_delete=models.CASCADE)
    clue = models.TextField()
    answer = models.TextField()
    link_question = models.TextField(blank=True)
    link_answer = models.TextField(blank=True)

    def __str__(self):
        return self.clue


class Clue(models.Model):

    RELATED_NAME = 'clues'

    question = models.ForeignKey(Question, related_name=RELATED_NAME, on_delete=models.CASCADE)
    value = models.IntegerField()

    class ClueState(models.TextChoices):
        COVERED = 'C'
        UNCOVERED = 'U'
        ANSWERED = 'A'

    state = models.CharField(
        max_length=2,
        choices=ClueState.choices,
        default=ClueState.COVERED)


class CategoryBlock(models.Model):

    clue1 = models.IntegerField()
    clue2 = models.IntegerField()
    clue3 = models.IntegerField()
    clue4 = models.IntegerField()
    clue5 = models.IntegerField()

    @classmethod
    def clue(cls, index):
        # type: (int) -> models.IntegerField
        return [cls.clue1, cls.clue2, cls.clue3, cls.clue4, cls.clue5][index-1]


class Round(models.Model):

    block1 = models.IntegerField()
    block2 = models.IntegerField()
    block3 = models.IntegerField()
    block4 = models.IntegerField()
    block5 = models.IntegerField()

    double_trouble1 = models.CharField(max_length=5)
    double_trouble2 = models.CharField(max_length=5, null=True)

    @classmethod
    def block(cls, index):
        # type: (int) -> models.IntegerField
        return [cls.block1, cls.block2, cls.block3, cls.block4, cls.block5][index-1]


class Game(models.Model):

    name = models.CharField(max_length=50, unique=True)
    round1 = models.IntegerField()
    round2 = models.IntegerField()

    @classmethod
    def round(cls, index):
        # type: (int) -> models.IntegerField
        return [cls.round1, cls.round2][index-1]


class Match(models.Model):
    game = models.ForeignKey(Game, related_name='matches', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=False)
    date = models.DateTimeField(default=now, editable=False)

    class MatchState(models.TextChoices):
        OPEN = 'O'
        STARTED = 'S'
        COMPLETED = 'C'

    state = models.CharField(
        max_length=2,
        choices=MatchState.choices,
        default=MatchState.OPEN)

    def __str__(self):
        return '{name} | {date}'.format(name=self.name, date=self.date)


class Player(models.Model):

    RELATED_NAME = 'players'

    user = models.ForeignKey(User, related_name=RELATED_NAME, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, related_name=RELATED_NAME, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class Answer(models.Model):

    RELATED_NAME = 'answers'

    player = models.ForeignKey(Player, related_name=RELATED_NAME, on_delete=models.CASCADE)
    clue = models.ForeignKey(Clue, related_name=RELATED_NAME, on_delete=models.DO_NOTHING)
    ts = models.DateTimeField(default=now, editable=False)
    submission = models.TextField()
    value = models.IntegerField(null=True)

    def __str__(self):
        return self.submission
