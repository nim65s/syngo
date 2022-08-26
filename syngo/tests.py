import os

from django.conf import settings
from django.test import TestCase

from nio import AsyncClient


class SyngoTest(TestCase):
    async def test_access_token(self):
        client = AsyncClient(settings.SYNGO_SYNAPSE_URL)
        client.access_token = settings.SYNGO_ACCESS_TOKEN
        client.user_id = os.environ["MATRIX_ID"]
        client.device_id = "test"
        await client.sync()
        await client.close()
