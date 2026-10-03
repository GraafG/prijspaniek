import json
import unittest
from unittest.mock import patch

import scrape


class ParsingTests(unittest.TestCase):
    def setUp(self):
        network = patch(
            "urllib.request.urlopen",
            side_effect=AssertionError("Network access is forbidden in offline tests"),
        )
        self.urlopen = network.start()
        self.addCleanup(network.stop)

    def tearDown(self):
        self.urlopen.assert_not_called()

    def test_rsc_payload_to_product(self):
        product = {
            "code": "fixture-1",
            "title": 'Test "chocolade"',
            "description": "100 g",
            "brand": "Fixture",
            "price": {"current": {"amount": 1.239}, "original": {"amount": 1.99}},
            "isDeal": True,
            "image": "https://example.invalid/image/upload/fixture",
            "href": "/nl-nl/p/fixture-1/",
        }
        encoded = json.dumps({"product": product}, separators=(",", ":"))
        chunks = [encoded[:20], encoded[20:]]
        html = "".join(
            f"<script>self.__next_f.push([1,{json.dumps(chunk)}])</script>"
            for chunk in chunks
        )

        self.assertEqual(scrape.payload(html), encoded)
        self.assertEqual(
            scrape.parse_products(scrape.payload(html), "Chocolade"),
            [{
                "code": "fixture-1",
                "name": 'Test "chocolade"',
                "desc": "100 g",
                "brand": "Fixture",
                "cat": "Chocolade",
                "price": 1.24,
                "original": 1.99,
                "isDeal": True,
                "image": "https://example.invalid/image/upload/fixture",
                "href": "/nl-nl/p/fixture-1/",
            }],
        )

    def test_missing_title_or_price_is_skipped(self):
        for product in (
            {"price": {"current": {"amount": 1}}},
            {"title": "Fixture"},
            {"title": "Fixture", "price": {}},
        ):
            with self.subTest(product=product):
                encoded = json.dumps({"product": product}, separators=(",", ":"))
                self.assertEqual(scrape.parse_products(encoded, "Fixture"), [])

    def test_empty_payload(self):
        self.assertEqual(scrape.payload("<html></html>"), "")
        self.assertEqual(scrape.parse_products("", "Fixture"), [])

    def test_square_image_url(self):
        self.assertEqual(
            scrape.square_img("https://example.invalid/image/upload/fixture"),
            "https://example.invalid/image/upload/t_digital_square,w_500,f_auto/fixture.webp",
        )


if __name__ == "__main__":
    unittest.main()
