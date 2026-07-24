import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comment
from reviews.constants import USER

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов'

    def handle(self, *args, **options):
        csv_path = 'static/data/'

        self.stdout.write('Начинаем импорт данных...')

        self.import_users(csv_path)
        self.import_categories(csv_path)
        self.import_genres(csv_path)
        self.import_titles(csv_path)
        self.import_genre_title(csv_path)
        self.import_reviews(csv_path)
        self.import_comments(csv_path)

        self.stdout.write(self.style.SUCCESS('Импорт завершен!'))

    def import_users(self, csv_path):
        """Импорт пользователей"""
        filepath = os.path.join(csv_path, 'users.csv')

        if not os.path.exists(filepath):
            self.stdout.write(self.style.WARNING('users.csv не найден'))
            return

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'username': row['username'],
                        'email': row['email'],
                        'role': row.get('role', USER),
                        'bio': row.get('bio', ''),
                        'first_name': row.get('first_name', ''),
                        'last_name': row.get('last_name', ''),
                    }
                )
                count += 1

            self.stdout.write(f'Пользователи: {count} записей')

    def import_categories(self, csv_path):
        """Импорт категорий"""
        filepath = os.path.join(csv_path, 'category.csv')

        if not os.path.exists(filepath):
            self.stdout.write(self.style.WARNING('category.csv не найден'))
            return

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
                count += 1

            self.stdout.write(f'Категории: {count} записей')

    def import_genres(self, csv_path):
        """Импорт жанров"""
        filepath = os.path.join(csv_path, 'genre.csv')

        if not os.path.exists(filepath):
            self.stdout.write(self.style.WARNING('genre.csv не найден'))
            return

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
                count += 1

            self.stdout.write(f'Жанры: {count} записей')

    def import_titles(self, csv_path):
        """Импорт произведений"""
        filepath = os.path.join(csv_path, 'titles.csv')

        if not os.path.exists(filepath):
            self.stdout.write(self.style.WARNING('titles.csv не найден'))
            return

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                category = Category.objects.filter(id=row['category']).first()

                if not category:
                    self.stdout.write(
                        f'Категория {row["category"]} не найдена'
                    )
                    continue

                Title.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'year': row['year'],
                        'description': row.get('description', ''),
                        'category': category,
                    }
                )
                count += 1

            self.stdout.write(f'Произведения: {count} записей')

    def import_genre_title(self, csv_path):
        """Импорт связей произведений и жанров"""
        filepath = os.path.join(csv_path, 'genre_title.csv')

        if not os.path.exists(filepath):
            self.stdout.write(self.style.WARNING('genre_title.csv не найден'))
            return

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    genre = Genre.objects.get(id=row['genre_id'])

                    title.genre.add(genre)
                    count += 1

                except (Title.DoesNotExist, Genre.DoesNotExist):
                    self.stdout.write(
                        f'Связь не найдена: title={row["title_id"]}, '
                        f'genre={row["genre_id"]}'
                    )

            self.stdout.write(f'Связи жанров: {count} записей')

    def import_reviews(self, csv_path):
        """Импорт отзывов"""
        filepath = os.path.join(csv_path, 'review.csv')

        if not os.path.exists(filepath):
            self.stdout.write(self.style.WARNING('review.csv не найден'))
            return

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                author, created = User.objects.get_or_create(
                    id=row['author'],
                    defaults={
                        'username': f'user_{row["author"]}',
                        'email': f'user_{row["author"]}@example.com',
                        'role': USER,
                    }
                )

                if created:
                    self.stdout.write(f'Создан пользователь {author.username}')

                try:
                    title = Title.objects.get(id=row['title_id'])
                except Title.DoesNotExist:
                    self.stdout.write(
                        f'Произведение {row["title_id"]} не найдено'
                    )
                    continue

                Review.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'title': title,
                        'text': row['text'],
                        'author': author,
                        'score': row['score'],
                        'pub_date': row.get('pub_date'),
                    }
                )
                count += 1

            self.stdout.write(f'Отзывы: {count} записей')

    def import_comments(self, csv_path):
        """Импорт комментариев"""
        filepath = os.path.join(csv_path, 'comments.csv')

        if not os.path.exists(filepath):
            self.stdout.write(self.style.WARNING('comments.csv не найден'))
            return

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                author, created = User.objects.get_or_create(
                    id=row['author'],
                    defaults={
                        'username': f'user_{row["author"]}',
                        'email': f'user_{row["author"]}@example.com',
                        'role': USER,
                    }
                )

                if created:
                    self.stdout.write(f'Создан пользователь {author.username}')

                try:
                    review = Review.objects.get(id=row['review_id'])
                except Review.DoesNotExist:
                    self.stdout.write(
                        f'Отзыв {row["review_id"]} не найден'
                    )
                    continue

                Comment.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'review': review,
                        'text': row['text'],
                        'author': author,
                        'pub_date': row.get('pub_date'),
                    }
                )
                count += 1

            self.stdout.write(f'Комментарии: {count} записей')
