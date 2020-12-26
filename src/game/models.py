from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import now


class Game(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    title = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):

    RELATED_NAME = 'questions'

    game = models.ForeignKey(Game, related_name=RELATED_NAME, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name=RELATED_NAME, on_delete=models.CASCADE)
    round = models.IntegerField()
    value = models.IntegerField()
    clue = models.TextField()
    answer = models.TextField()
    link_question = models.TextField(blank=True)
    link_answer = models.TextField(blank=True)

    class QuestionState(models.TextChoices):
        COVERED = 'C'
        UNCOVERED = 'U'
        ANSWERED = 'A'

    state = models.CharField(
        max_length=2,
        choices=QuestionState.choices,
        default=QuestionState.COVERED)

    def __str__(self):
        return self.clue


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


class Answer(models.Model):

    RELATED_NAME = 'answers'

    match = models.ForeignKey(Match, related_name=RELATED_NAME, on_delete=models.CASCADE)
    player = models.ForeignKey(User, related_name=RELATED_NAME, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name=RELATED_NAME, on_delete=models.CASCADE)
    ts = models.DateTimeField(default=now, editable=False)
    submission = models.TextField()
    value = models.IntegerField(null=True)

    def __str__(self):
        return self.submission


class Score(models.Model):

    RELATED_NAME = 'scores'

    player = models.ForeignKey(User, related_name=RELATED_NAME, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, related_name=RELATED_NAME, on_delete=models.CASCADE)
    value = models.IntegerField()
