from django.db import models
from django.utils import timezone

class Episode(models.Model):
    id_episode = models.AutoField(primary_key=True)
    season_number = models.PositiveIntegerField(verbose_name='Номер сезона')
    episode_number = models.PositiveIntegerField(verbose_name='Номер выпуска')
    city = models.CharField(max_length=100, verbose_name='Город')

    def __str__(self):
        return f"Сезон {self.season_number}, Выпуск {self.episode_number}, Город: {self.city}"

class Heroine(models.Model):
    id_heroine = models.AutoField(primary_key=True)
    heroine_name = models.CharField(max_length=100, verbose_name='Имя героини')
    heroine_age = models.PositiveIntegerField(verbose_name='Возраст героини')
    heroine_photo = models.ImageField(upload_to='heroines/', verbose_name='Фото героини')
    episode = models.OneToOneField(Episode, on_delete=models.CASCADE, related_name='heroine')

    def __str__(self):
        return f"{self.heroine_name}, Возраст: {self.heroine_age}, Эпизод: {self.episode}"

class Father(models.Model):
    id_father = models.AutoField(primary_key=True)
    father_name = models.CharField(max_length=100, verbose_name='Имя отца', blank=True, null=True)
    father_age = models.PositiveIntegerField(verbose_name='Возраст отца', blank=True, null=True)
    father_photo = models.ImageField(upload_to='fathers/', verbose_name='Фото отца', blank=True, null=True)
    episode = models.OneToOneField(Episode, on_delete=models.CASCADE, related_name='father')

    def __str__(self):
        return (f"{self.father_name}, Возраст: {self.father_age}, Эпизод: {self.episode}" 
                if self.father_name else 'Без информации')

class Child(models.Model):
    id_child = models.AutoField(primary_key=True)
    child_name = models.CharField(max_length=100, verbose_name='Имя ребенка')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='children', verbose_name='Эпизод')  

    def __str__(self):
        return f"Имя ребенка: {self.child_name}, Эпизод: {self.episode}"

class Marker(models.Model):
    id_marker = models.AutoField(primary_key=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='markers', verbose_name='Эпизод')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления')
    is_deleted = models.BooleanField(default=False, verbose_name='Метка удалена')  # Добавляем поле

    def __str__(self):
        return (f"Эпизод: {self.episode}, Широта: {self.latitude}, Долгота: {self.longitude}, "
                f"Дата добавления: {self.created_at}")
