from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Blog


class BlogAPITestCase(APITestCase):
	def setUp(self):
		self.blog = Blog.objects.create(title="First post", content="Hello DRF")
		self.list_url = reverse("blog-list")

	def test_list_blogs(self):
		response = self.client.get(self.list_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)

	def test_create_blog(self):
		payload = {"title": "New post", "content": "New content"}
		response = self.client.post(self.list_url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Blog.objects.count(), 2)

	def test_retrieve_blog(self):
		detail_url = reverse("blog-detail", kwargs={"pk": self.blog.pk})
		response = self.client.get(detail_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["title"], self.blog.title)

	def test_update_blog(self):
		detail_url = reverse("blog-detail", kwargs={"pk": self.blog.pk})
		payload = {"title": "Updated", "content": "Updated body"}
		response = self.client.put(detail_url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.blog.refresh_from_db()
		self.assertEqual(self.blog.title, "Updated")

	def test_delete_blog(self):
		detail_url = reverse("blog-detail", kwargs={"pk": self.blog.pk})
		response = self.client.delete(detail_url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Blog.objects.count(), 0)


