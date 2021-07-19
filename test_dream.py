import unittest
from DreamsList import Dream


class MyTestCase(unittest.TestCase):
    def test_dream_is_invalid(self):
        d = Dream(
            name="test",
            link="https://test.test",
            dreamers=["test dreamer"],
            minimum_budget=0,
            maximum_budget=0,
            preexisting_funding=0,
            total_funding=0
        )
        self.assertFalse(d.is_valid())

    def test_dream_is_invalid_because_max_budget_equal_prexisting_funding(self):
        d = Dream(
            name="test",
            link="https://test.test",
            dreamers=["test dreamer"],
            minimum_budget=100.0,
            maximum_budget=120.0,
            preexisting_funding=10.0,
            total_funding=0
        )
        self.assertFalse(d.is_valid())

    def test_dream_is_valid(self):
        d = Dream(
            name="test",
            link="https://test.test",
            dreamers=["test dreamer"],
            minimum_budget=100.0,
            maximum_budget=200.0,
            preexisting_funding=50.0,
            total_funding=100.0
        )
        self.assertTrue(d.is_valid())


if __name__ == "__main__":
    unittest.main()
