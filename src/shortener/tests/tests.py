import json

from django.test import TestCase
from django.urls import reverse

from shortener.models import Url


class ShortURLTest(TestCase):
    def test_create_url(self):
        # need to test expected answer
        create_url_endpoint = reverse('api_url_list')
        data = {
            'url': 'localhost'
        }

        response = self.client.post(create_url_endpoint, json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

        url = Url.objects.get(id=1)
        hash = url.short
        url.save()
        updated_hash = url.short
        self.assertEqual(hash, updated_hash)

        url = Url.objects.get(id=1)
        self.assertEqual(url.url, 'localhost')

    def test_list_url(self):
        list_url_endpoint = reverse('api_url_list')

        response = self.client.get(list_url_endpoint,
                                   content_type="application/json")
        content = response.json()['objects']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [])

    def test_detail_url(self):
        create_url_endpoint = reverse('api_url_list')
        data = {
            'url': 'localhost'
        }
        response = self.client.post(create_url_endpoint, json.dumps(data),
                                    content_type="application/json")

        pk = 1
        detail_url_endpoint = reverse('api_url_detail', args=(pk,))

        response = self.client.get(detail_url_endpoint,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

        url_response = response.json()['url']
        hash_response = response.json()['short']
        url = Url.objects.get(id=1)

        self.assertEqual(url.url, url_response)
        self.assertEqual(url.short, hash_response)
        self.assertEqual(url.url, 'localhost')
        self.assertEqual(url_response, 'localhost')

    def test_delete_url(self):
        create_url_endpoint = reverse('api_url_list')
        data = {
            'url': 'localhost'
        }

        response = self.client.post(create_url_endpoint, json.dumps(data),
                                    content_type="application/json")
        registers = len(Url.objects.all())
        self.assertEqual(registers, 1)

        pk = 1
        delete_url_endpoint = reverse('api_url_detail', args=(pk,))

        response = self.client.delete(delete_url_endpoint,
                                      content_type="application/json")
        self.assertEqual(response.status_code, 204)

        registers = len(Url.objects.all())
        self.assertEqual(registers, 0)

        content = response.content
        self.assertEqual(content, b'')