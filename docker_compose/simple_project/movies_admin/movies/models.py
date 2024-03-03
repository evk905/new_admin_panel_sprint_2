from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin
from .enums import Role, Type


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("genre"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = 'content"."genre'
        ordering = ["-name"]
        indexes = [models.Index(fields=["-name"])]
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full name"), max_length=255)

    class Meta:
        db_table = 'content"."person'
        ordering = ["full_name"]
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    def __str__(self):
        return self.full_name

    def role_in_film(self):
        person_filmworks = PersonFilmwork.objects.filter(person=self).values_list("role", flat=True).distinct()
        roles = ", ".join(person_filmworks)
        return roles

    role_in_film.short_description = _("role")


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255)
    genre = models.ManyToManyField(Genre, through="GenreFilmwork")
    person = models.ManyToManyField(Person, through="PersonFilmwork")
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.CharField(_("year_of_release"), blank=True, null=True, db_index=True)
    rating = models.FloatField(
        _("rating"), blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.CharField(_("type"), choices=Type.choices, default=Type.movie)


    class Meta:
        db_table = 'content"."film_work'
        ordering = ["-creation_date"]
        indexes = [models.Index(fields=["creation_date"])]
        verbose_name = _("film work")
        verbose_name_plural = _("film works")

    def __str__(self):
        return self.title

    def get_genre(self):
        return ",".join([genre.name for genre in self.genre.all()])

    get_genre.short_description = _("genre")


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE, verbose_name=_("genre"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("genre film work")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"],
                name="unique_filmwork_genre",
            ),
        ]


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE, verbose_name=_("person"))
    role = models.TextField(_("role"), choices=Role.choices, default=Role.actor)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = (_("person film work"),)
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"],
                name="unique_filmwork_preson_role",
            ),
        ]