from django.test import TestCase


class SmokeTest(TestCase):
    """Тест на токсичность"""

    def test_bad_match(self):
        """Тест: неправильные математические расчёты"""
        self.assertEquals(1 + 1, 3)
