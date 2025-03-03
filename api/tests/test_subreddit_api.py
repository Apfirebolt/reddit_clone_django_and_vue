"""
Tests for the Question API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from api.serializers import SubRedditSerializer
from rest_framework.test import APIClient
from rest_framework import status
from subreddit.models import SubReddit


SUBREDDIT_URL = reverse("api:subreddit")


def detail_url(subreddit_id):
    """Return subreddit detail URL"""
    return reverse("api:subreddit-crud", args=[subreddit_id])


class PublicSubRedditApiTests(TestCase):
    """Test the publicly available subreddit API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving subreddits"""
        res = self.client.get(SUBREDDIT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateSubRedditApiTests(TestCase):
    """Test the authorized user subreddit API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@example.com", "password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_subreddits(self):
        """Test retrieving a list of subreddits"""
        SubReddit.objects.create(
            name="Sample subreddit 1",
            description="Sample description 1",
            creator=self.user,
        )
        SubReddit.objects.create(
            name="Sample subreddit 2",
            description="Sample description 2",
            creator=self.user,
        )

        res = self.client.get(SUBREDDIT_URL)

        subreddits = SubReddit.objects.all().order_by("-id")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_subreddit(self):
        """Test creating subreddit"""
        payload = {
            "name": "sample-subreddit-1",
            "description": "Sample description 1",
            "creator": self.user.id,
        }
        res = self.client.post(SUBREDDIT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["description"], payload["description"])

    def test_get_subreddit_detail(self):
        """Test viewing a subreddit detail"""
        subreddit = SubReddit.objects.create(
            name="Sample subreddit 1",
            description="Sample description 1",
            creator=self.user,
        )

        url = detail_url(subreddit.id)
        res = self.client.get(url)

        serializer = SubRedditSerializer(subreddit)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_subreddit(self):
        """Test updating a subreddit"""
        subreddit = SubReddit.objects.create(
            name="Sample subreddit 1",
            description="Sample description 1",
            creator=self.user,
        )

        payload = {"name": "Updated subreddit", "description": "Updated description", "creator": self.user.id}
        url = detail_url(subreddit.id)
        res = self.client.put(url, payload)

        subreddit.refresh_from_db()
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(subreddit.name, payload["name"])
        self.assertEqual(subreddit.description, payload["description"])

    def test_delete_subreddit(self):
        """Test deleting a subreddit"""
        subreddit = SubReddit.objects.create(
            name="Sample subreddit 1",
            description="Sample description 1",
            creator=self.user,
        )

        url = detail_url(subreddit.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SubReddit.objects.filter(id=subreddit.id).exists())
