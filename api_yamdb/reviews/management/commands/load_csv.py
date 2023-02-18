import csv

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR

from reviews.models import Category, Genre, Title, GenreTitle, User


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):
        with open(
            f'{BASE_DIR}/static/data/category.csv', encoding='utf-8'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                category = Category(id=id, name=name, slug=slug)
                category.save()

        with open(
            f'{BASE_DIR}/static/data/genre.csv', encoding='utf-8'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                genre = Genre(id=id, name=name, slug=slug)
                genre.save()

        with open(
            f'{BASE_DIR}/static/data/titles.csv', encoding='utf-8'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                id = row['id']
                name = row['name']
                year = row['year']
                category_id = row['category']
                title = Title(
                    id=id, name=name, year=year, category_id=category_id
                )
                title.save()

        with open(
            f'{BASE_DIR}/static/data/genre_title.csv', encoding='utf-8'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                title_id = row['title_id']
                genre_id = row['genre_id']
                genre_title = GenreTitle(genre_id=genre_id, title_id=title_id)
                genre_title.save()

        with open(
            f'{BASE_DIR}/static/data/users.csv', encoding='utf-8'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                id = row['id']
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['bio']
                first_name = ['first_name']
                last_name = ['last_name']
                user = User(
                    id=id,
                    username=username,
                    email=email,
                    role=role,
                    bio=bio,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
