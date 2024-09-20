from django.db import models
from django.utils import timezone

class Episode(models.Model):
    id_episode = models.AutoField(primary_key=True)
    season_number = models.PositiveIntegerField(verbose_name='Номер сезона')
    episode_number = models.PositiveIntegerField(verbose_name='Номер выпуска')
    city = models.CharField(max_length=100, verbose_name='Город')

    def __str__(self):
        return f'Сезон {self.season_number}, Выпуск {self.episode_number} — {self.city}'
    
class Heroine(models.Model):
    id_heroine = models.AutoField(primary_key=True)
    heroine_name = models.CharField(max_length=100, verbose_name='Имя героини')
    heroine_age = models.PositiveIntegerField(verbose_name='Возраст героини')
    heroine_photo = models.ImageField(upload_to='heroines/', verbose_name='Фото героини')
    episode = models.OneToOneField(Episode, on_delete=models.CASCADE, related_name='heroine')

    def __str__(self):
        return self.heroine_name

class Father(models.Model):
    id_father = models.AutoField(primary_key=True)
    father_name = models.CharField(max_length=100, verbose_name='Имя отца', blank=True, null=True)
    father_age = models.PositiveIntegerField(verbose_name='Возраст отца', blank=True, null=True)
    father_photo = models.ImageField(upload_to='fathers/', verbose_name='Фото отца', blank=True, null=True)
    episode = models.OneToOneField(Episode, on_delete=models.CASCADE, related_name='father')

    def __str__(self):
        return self.father_name if self.father_name else 'Без информации'

class Child(models.Model):
    id_child = models.AutoField(primary_key=True)
    child_name = models.CharField(max_length=100, verbose_name='Имя ребенка')
    episode = models.OneToOneField(Episode, on_delete=models.CASCADE, related_name='child')

    def __str__(self):
        return self.child_name

class Marker(models.Model):
    id_marker = models.AutoField(primary_key=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='markers', verbose_name='Эпизод')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления')

    def __str__(self):
        return f'Метка для эпизода: Сезон {self.episode.season_number}, Выпуск {self.episode.episode_number}'
