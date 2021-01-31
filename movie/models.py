from datetime import date

from django.db import models

# Create your models here.
from rest_framework.reverse import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория",max_length=256)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=256,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Actor(models.Model):
    """Актеры и режисеры"""
    name = models.CharField("Имя",max_length=128)
    age = models.PositiveSmallIntegerField("Возраст",default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение",upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail",kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Актеры и режисеры"
        verbose_name_plural = "Актеры и режисеры"

class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя",max_length=128)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=256,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Movie(models.Model):
    """Фильмы"""
    title = models.CharField("Название",max_length=128)
    tagline = models.CharField("Слоган",max_length=128,default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер",upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода",default=2019)
    country = models.CharField("Страна",max_length=64)
    directors = models.ManyToManyField(Actor,verbose_name="режисер",related_name="film_director")
    actors = models.ManyToManyField(Actor,verbose_name="актеры",related_name="film_actor")
    genres = models.ManyToManyField(Genre,verbose_name="жанры")
    world_primiere = models.DateField("Примьера в мире", default=date.today)
    budjet = models.PositiveSmallIntegerField("Бюджет",default=0, help_text="указать сумму в долларах")
    fess_in_usa = models.PositiveSmallIntegerField("Сборы в США",default=0, help_text="указать сумму в долларах")
    fess_in_world = models.PositiveSmallIntegerField("Сборы в мире",default=0, help_text="указать сумму в долларах")
    category = models.ForeignKey(Category,verbose_name="Категория",on_delete=models.SET_NULL,null=True)
    url = models.SlugField(max_length=256,unique=True)
    draft = models.BooleanField("Черновик",default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail",kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок",max_length=128)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение",upload_to="movie_shots/")
    movie = models.ForeignKey(Movie,verbose_name="Фильм",on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"

class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение",default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering =["-value"]

class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адресс",max_length=16)
    star = models.ForeignKey(RatingStar,on_delete=models.CASCADE,verbose_name="звезда")
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,verbose_name="фильм",related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя",max_length=128)
    text = models.TextField("Сообщение",max_length=8000)
    parent = models.ForeignKey('self',verbose_name="Родитель",on_delete=models.SET_NULL,blank=True,null=True,
                               related_name="children")
    movie = models.ForeignKey(Movie,verbose_name="фильм",on_delete=models.CASCADE,related_name="reviews")

    def __str__(self):
        return f"{self.name}-{self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"