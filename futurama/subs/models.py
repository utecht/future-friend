from django.db import models

# Create your models here.
class Episode(models.Model):
    name = models.CharField(max_length=200)
    episode_file = models.CharField(max_length=200, blank=True, null=True)
    season = models.IntegerField()
    number = models.IntegerField()

    def __str__(self):
        return "{}x{} - {}".format(self.season, self.number, self.name)

class Sub(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='sub')
    line = models.TextField()
    line_formatted = models.TextField()
    index = models.IntegerField()
    duration = models.CharField(max_length=20)
    start = models.CharField(max_length=20)
    end = models.CharField(max_length=20)

    def __str__(self):
        return self.line
