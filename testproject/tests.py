from django.contrib.auth import get_user_model
from django.test import TestCase

import syngo


class SyngoTest(TestCase):
    async def test_register(self):
        User = get_user_model()
        user = await User.objects.acreate(username="toto", password="toto")
        self.assertEqual(len(syngo.list_accounts()), 1)
        self.assertEqual(syngo.register(user).status_code, 201)
        self.assertEqual(syngo.register(user).status_code, 200)
        self.assertEqual(syngo.register(user).status_code, 200)
        self.assertEqual(len(syngo.list_accounts()), 2)
