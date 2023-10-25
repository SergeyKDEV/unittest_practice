from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from news.models import Comment, News

User = get_user_model()


class TestHomePage(TestCase):
    HOME_URL = reverse('news:home')

    @classmethod
    def setUpTestData(cls):
        today = datetime.today()
        News.objects.bulk_create(
            News(title=f'News {index}',
                 text='Sample text.',
                 date=today - timedelta(days=index)
                 )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        )

    def test_news_count(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        self.assertEqual(len(object_list), settings.NEWS_COUNT_ON_HOME_PAGE)

    def test_news_order(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        all_dates = [news.date for news in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)


class TestNewsPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title='News title',
            text='News text.'
        )
        cls.detail_url = reverse(
            'news:detail',
            args=(cls.news.id,)
        )
        cls.author = User.objects.create(username='Commenter')
        now = timezone.now()
        for index in range(2):
            comment = Comment.objects.create(
                news=cls.news,
                author=cls.author,
                text=f'Comment #{index}',
            )
            comment.created = now + timedelta(days=index)
            comment.save()

    def detail_url_response(self):
        return self.client.get(self.detail_url)

    def test_comments_order(self):
        self.assertIn('news', self.detail_url_response().context)
        news = self.detail_url_response().context['news']
        all_comments = news.comment_set.all()
        self.assertLess(all_comments[0].created, all_comments[1].created)

    def test_anonymous_form_absent(self):
        self.assertNotIn('form', self.detail_url_response().context)

    def test_authorized_form_present(self):
        self.client.force_login(self.author)
        self.assertIn('form', self.detail_url_response().context)
