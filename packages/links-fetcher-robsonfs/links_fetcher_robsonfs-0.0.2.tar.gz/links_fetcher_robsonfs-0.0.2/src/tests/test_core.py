from unittest import TestCase
from unittest.mock import MagicMock, patch

from links_fetcher_robsonfs import tag_extractor, get_source


class TestLinksFetcher(TestCase):

    def setUp(self):
        self.html_data = """
        <html>
            <head><title>Test Data</title></head>
            <body>
                <a href="https://example.com/home">
                    <img src="images/logo.png">
                </a>
                <a href="https://example.com/link1">Link 1</a>
                <a href="https://example.com/link2">Link 2</a>
                <a href="https://example.com/link3">Link 3</a>
            </body>
        </html>
        """
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200
        self.mock_response.text = self.html_data

    @patch('links_fetcher_robsonfs.core.requests.get')
    def test_get_source_get_is_properly_called(self, mock_requests):
        _ = get_source("https://example.com")
        mock_requests.assert_called_once_with("https://example.com")
