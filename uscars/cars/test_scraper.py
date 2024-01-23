import httpx
from cars.scraper import parse_page, extract_text, get_html, find_max_pages
from selectolax.parser import HTMLParser

def test_get_html():
    url = "https://ucars.pro/pl/sales-history"
    test_html = "<html><body>Test content</body></html>"

    def mock_response(request):
        return httpx.Response(200, text=test_html)

    client = httpx.Client(transport=httpx.MockTransport(mock_response))
    parser = get_html(client, url)
    assert isinstance(parser, HTMLParser)
    assert parser.html == test_html

def test_parse_page():
    html_content = '<div class="vehicle-card__content"><span class="vehicle-card__title">Car Name</span><span class="vehicle-card__bid-digits">$1000</span><span class="vehicle-card__specs">New</span><a href="http://example.com/car"></a></div>'
    parser = HTMLParser(html_content)
    result = parse_page(parser)
    assert len(result) == 1
    assert result[0]['name'] == 'Car Name'
    assert result[0]['price'] == '$1000'
    assert result[0]['condition'] == 'New'
    assert result[0]['link'] == 'http://example.com/car'

def test_extract_text():
    html = "<div><p>Test paragraph</p></div>"
    parser = HTMLParser(html)
    result = extract_text(parser, "p")
    assert result == "Test paragraph"

def test_find_max_pages():
    html_content = '<div class="pagination"><a class="page-number">1</a><a class="page-number">2</a><a class="page-number">3</a></div>'
    parser = HTMLParser(html_content)
    max_pages = find_max_pages(parser)
    assert max_pages == 3
