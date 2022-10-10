import csv

from django.core.management.base import BaseCommand

from api_yamdb import settings
from reviews.models import Category, Comment, Genre, Review, Title, User

TABLES = (
    (User, 'users.csv'),
    (Category, 'category.csv'),
    (Genre, 'genre.csv'),
    (Title, 'titles.csv'),
    (Review, 'review.csv'),
    (Comment, 'comments.csv'),
)
GENRE_TITLE_TPL = (Title, 'genre_title.csv')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # User.objects.all().delete()
        # Genre.objects.all().delete()
        # Category.objects.all().delete()
        # Title.objects.all().delete()
        # Review.objects.all().delete()
        # Comment.objects.all().delete()

        for tpl in TABLES:
            model, csv_f = tpl
            with open(
                f'{settings.BASE_DIR}/api/static/data/{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                for data in reader:
                    if 'category' in data:
                        obj = Category.objects.get(pk=int(data['category']))
                        data['category'] = obj
                    if 'author' in data:
                        obj = User.objects.get(pk=int(data['author']))
                        data['author'] = obj
                    model.objects.get_or_create(**data)
        model, csv_f = GENRE_TITLE_TPL
        with open(
                f'{settings.BASE_DIR}/api/static/data/{csv_f}',
                'r',
                encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for data in reader:
                title = Title.objects.get(pk=int(data['title_id']))
                genre = Genre.objects.get(pk=int(data['genre_id']))
                title.genre.add(genre)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
