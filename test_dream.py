import unittest
from DreamsList import Dream, DreamInputException


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dream = Dream(
            name="test",
            link="https://test.test",
            dreamers=["test dreamer"],
            minimum_budget=100,
            maximum_budget=200,
            preexisting_funding=50,
            total_funding=100
        )

    def test_dream_is_invalid_because_minimum_is_equal_to_maximum(self):
        self.dream.preexisting_funding = 1
        self.dream.maximum_budget = 1
        self.dream.minimum_budget = 1
        self.assertFalse(self.dream.is_valid())

    def test_dream_is_invalid_because_no_votes(self):
        d = self.dream
        d.minimum_budget = 100
        d.maximum_budget = 200
        d.preexisting_funding = 10.0
        d.total_funding = 10
        d.calculate_grant()
        d.calculate_votes()
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

    def test_apply_funding(self):
        funding = self.dream.apply_funding(2)
        self.assertEqual(100, funding)

    def test_apply_funding_bigger_than_maximum_buget(self):
        funding = self.dream.apply_funding(20)
        self.assertEqual(150, funding)

    def test_raises_exception_on_bad_input(self):
        self.assertRaises(DreamInputException, self.dream.apply_funding, -2)


if __name__ == "__main__":
    unittest.main()
