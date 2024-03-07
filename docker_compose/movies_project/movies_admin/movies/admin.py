from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 1
    classes = ("collapse",)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 1
    classes = ("collapse",)
    fields = ["person", "film_work", "role"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    save_on_top = True
    list_per_page = 10


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = [PersonFilmworkInline]
    list_display = (
        "full_name",
        "role_in_film",
    )
    list_filter = (
        "full_name",
        "personfilmwork__role",
    )
    search_fields = (
        "full_name",
        "personfilmwork__role",
    )
    save_on_top = True
    list_per_page = 10


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "created_at",
        "get_genre",
    )
    list_filter = (
        "type",
        "creation_date",
        "genre__name",
    )
    search_fields = (
        "title",
        "description",
        "id",
        "genre__name",
        "type",
        "person__full_name",
    )
    list_editable = (
        "type",
        "creation_date",
        "rating",
    )
    save_on_top = True
    list_per_page = 10
