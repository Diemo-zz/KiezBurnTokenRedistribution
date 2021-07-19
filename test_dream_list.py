import unittest
from DreamsList import DreamList
from DreamsList import Dream


class MyTestCase(unittest.TestCase):
    def get_dream(self, total_funding: float):
        d = Dream(
            name=f"Dream {total_funding}",
            link=f"https://test{total_funding}.test",
            dreamers=[f"test dreamer {total_funding}"],
            minimum_budget=100,
            maximum_budget=200,
            preexisting_funding=50,
            total_funding=total_funding,
        )
        return d

    def test_calculate_budget(self):
        d1 = self.get_dream(100)
        dreamlist = DreamList(dreams_in=[d1])
        funding_allocated = dreamlist.calculate_funding(50)
        self.assertEqual(50, funding_allocated)

    def test_calculate_budget_with_two_dreams(self):
        d1 = self.get_dream(75)
        d2 = self.get_dream(125)

        dreamlist = DreamList(dreams_in=[d1, d2])
        expected = dreamlist.calculate_funding(100)
        self.assertEqual(d1.funded, 25)
        self.assertEqual(d2.funded, 75)
        self.assertEqual(100, expected)

    def test_reallocated_funding(self):
        d1 = self.get_dream(100)
        d2 = self.get_dream(150)
        dreamlist = DreamList(dreams_in=[d1, d2])
        funding_allocated = dreamlist.calculate_funding(400)
        self.assertEqual(400, funding_allocated)
        self.assertEqual(200, d1.funded)
        self.assertEqual(200, d2.funded)

    def test_with_invalid_dream(self):
        import math

        invalid_dream = self.get_dream(math.nan)
        valid_dream = self.get_dream(100)

        dreamlist = DreamList(dreams_in=[valid_dream, invalid_dream])
        expected = dreamlist.calculate_funding(50)
        self.assertEqual(50, expected)
        self.assertEqual(1, len(dreamlist.invalid_dreams))
        self.assertEqual(50, valid_dream.funded)


if __name__ == "__main__":
    unittest.main()
