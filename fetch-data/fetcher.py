class Fetcher:

    def __init__(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def set_url(self, new_url):
        self.url = new_url
        return None

    def get_html_content(self):
        import requests
        response = requests.get(self.get_url())

        if response.status_code != 200:
            return 'HTTP error - status code '+str(response.status_code)
        
        return response.content

    def parse_html_content(self):
        pass

        





# Test Script -----------------------------------
if __name__ == "__main__":
    # Create Fetcher object
    test = Fetcher('https://sfbay.craigslist.org/search/cta?query=4Runner&srchType=T&min_price=678&max_price=7500&min_auto_year=2003&max_auto_year=2009')

    # Print intial URL
    print(test.get_url())

    # Set new URL, print data. It should be empty
    test.set_url("")
    print(test.get_url())

    # Test HTTP request for HTML data response
    test.set_url("https://sfbay.craigslist.org/search/cta?query=4Runner&srchType=T&min_price=678&max_price=7500&min_auto_year=2003&max_auto_year=2009'")
    test.get_html_content()

    # Test BS4 parser against byte content response
    test.parse_html_content()