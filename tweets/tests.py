from rest_framework.test import APITestCase
from users.models import User
from tweets.models import Tweet
from rest_framework.authtoken.models import Token

class TestTweets(APITestCase):
    USERNAME = "protester"
    PAYLOAD = "TestCase Tweets Test!"
    URL = "/api/v1/tweets/"

    def setUp(self):
        self.user = User.objects.create(username=self.USERNAME)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        Tweet.objects.create(payload=self.PAYLOAD, user=self.user)

    def test_all_tweets(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["user"], self.USERNAME)
        self.assertEqual(data[0]["payload"], self.PAYLOAD)
        self.assertEqual(data[0]["like_count"], 0)

    def test_create_tweet(self):
        new_payload = "Create test Payload"
        response = self.client.post(self.URL, data={"payload": new_payload})
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["user"], self.USERNAME)
        self.assertEqual(data["payload"], new_payload)
        self.assertEqual(data["like_count"], 0)

    def test_create_tweet_invalid_payload(self):
        response = self.client.post(self.URL, data={"payload": ""})

        self.assertEqual(response.status_code, 400, "Not 400 status code")

    def test_create_tweet_invalid_user(self):
        self.client.credentials()  # Remove authentication
        response = self.client.post(self.URL, data={"payload": "Create test Payload"})

        self.assertEqual(response.status_code, 401, "Not 401 status code")


class TestTweetDetail(APITestCase):
    USERNAME = "protester"
    PAYLOAD = "TestCase Tweets Test!"
    TEST_URL = "/api/v1/tweets/1"
    NOT_FOUND_URL = "/api/v1/tweets/2"

    def setUp(self):
        self.user = User.objects.create(username=self.USERNAME)
        Tweet.objects.create(payload=self.PAYLOAD, user=self.user)

    def test_get_tweet(self):
        response = self.client.get(self.TEST_URL)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["user"], self.USERNAME)
        self.assertEqual(data["payload"], self.PAYLOAD)
        self.assertEqual(data["like_count"], 0)

    def test_put_tweet(self):
        new_payload = "Update test Payload"
        self.client.force_login(self.user)

        response = self.client.put(self.TEST_URL, data={"payload": new_payload})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["user"], self.USERNAME)
        self.assertEqual(data["payload"], new_payload)
        self.assertEqual(data["like_count"], 0)

    def test_delete_tweet(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.TEST_URL)

        self.assertEqual(response.status_code, 204)

    def test_tweet_not_found(self):
        response = self.client.get(self.NOT_FOUND_URL)

        self.assertEqual(response.status_code, 404, "Not 404 status code")

    def test_put_tweet_not_owner(self):
        new_user = User.objects.create(username="not_owner")
        self.client.force_login(new_user)

        response = self.client.put(self.TEST_URL, data={"payload": "Update test Payload"})

        self.assertEqual(response.status_code, 403, "Not 403 status code")

    def test_delete_tweet_not_owner(self):
        new_user = User.objects.create(username="not_owner")
        self.client.force_login(new_user)

        response = self.client.delete(self.TEST_URL)

        self.assertEqual(response.status_code, 403, "Not 403 status code")
