from django.contrib.auth import get_user_model
from django.test import TestCase

import syngo


class SyngoTest(TestCase):
    def test_syngo(self):
        User = get_user_model()
        user = User.objects.create(username="toto", password="toto")

        # Test register
        self.assertEqual(len(syngo.list_accounts()), 1)
        self.assertEqual(syngo.register(user).status_code, 201)
        self.assertEqual(syngo.register(user).status_code, 200)
        self.assertEqual(syngo.register(user).status_code, 200)
        self.assertEqual(len(syngo.list_accounts()), 2)

        # Test shadow_ban
        self.assertEqual(syngo.list_accounts()[1]["shadow_banned"], 0)
        syngo.shadow_ban(syngo.django_to_matrix(user))
        self.assertEqual(syngo.list_accounts()[1]["shadow_banned"], 1)
        syngo.shadow_ban(syngo.django_to_matrix(user), unban=True)
        self.assertEqual(syngo.list_accounts()[1]["shadow_banned"], 0)

        # Test deactivate
        syngo.deactivate(user)
        self.assertEqual(len(syngo.list_accounts()), 1)

        # Test registration token
        ret = syngo.registration_token().json()
        self.assertEqual(len(ret["token"]), 16)
        self.assertEqual(ret["uses_allowed"], 1)
        self.assertEqual(ret["completed"], 0)
