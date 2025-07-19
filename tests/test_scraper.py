import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import scraper

HTML_WITH_TIME = """
<table>
    <tr><td>A</td><td>B</td><td>C</td><td>10 mins</td></tr>
</table>
"""

HTML_NO_DATA = """
<table>
    <tr><td>Max Wait Time</td><td></td><td></td><td>4 mins</td></tr>
</table>
"""


def make_mock_driver(html):
    driver = MagicMock()
    driver.page_source = html
    return driver


def test_scrape_wait_time_success():
    driver = make_mock_driver(HTML_WITH_TIME)
    with patch('selenium.webdriver.Chrome', return_value=driver) as mc, \
         patch('time.sleep'):
        result = scraper.scrape_wait_time('http://example.com')
        assert result == '10 mins'
        driver.get.assert_called_once_with('http://example.com')
        driver.quit.assert_called_once()


def test_scrape_wait_time_no_data():
    driver = make_mock_driver(HTML_NO_DATA)
    with patch('selenium.webdriver.Chrome', return_value=driver) as mc, \
         patch('time.sleep'):
        result = scraper.scrape_wait_time('http://example.com')
        assert result == 'No Data'
        driver.quit.assert_called_once()
