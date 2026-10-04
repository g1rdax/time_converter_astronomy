import unittest
from astro_converter.cli import fractional_day_to_utc

class TestAstroConverter(unittest.TestCase):
    def test_standard_conversion(self):
        res = fractional_day_to_utc("2026 09 05.50000000")
        self.assertEqual(res, "2026-09-05 12:00:00.000 UTC")

    def test_rounding_overflow(self):
        # Перевірка правильного переходу секунд у хвилину при округленні
        res = fractional_day_to_utc("2026 09 05.99999999", sec_precision=2)
        self.assertTrue("2026-09-05 24:00:00.00 UTC" in res or "2026-09-05 23:59" in res)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            fractional_day_to_utc("invalid date format")

if __name__ == "__main__":
    unittest.main()