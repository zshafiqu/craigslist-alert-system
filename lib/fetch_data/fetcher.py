class Fetcher:

    def __init__(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def get_html_content(self):
        import requests
        response = requests.get(self.get_url())

        if response.status_code != 200:
            return 'HTTP error - status code '+str(response.status_code)
        
        return response.content

    def parse_html_content(self, html_byte_content):
        from bs4 import BeautifulSoup, SoupStrainer
        soup = BeautifulSoup(html_byte_content, 'html.parser')
        
        # Craigslist uses an unordered list with the class name "rows" for all of the posting cards.
        # Within this unordred list, each card is a list item with the class name "result-row".
        results = soup.find_all("li", class_="result-row")
        return results

    def convert_html_to_json(self, bs4_object):
        # All we're doing is traversing the 'DOM' object bs4 creates for us to search for data based on class
        # names or attributes, and then piecing these together into a JSON dictionary we can utilize later
        results = []

        for item in bs4_object:

            try:
                image_ids = item.find(class_="result-image gallery")['data-ids']
                first_image_id = image_ids.split(',')[0][2:]
                thumbnail_url = 'https://images.craigslist.org/'+first_image_id+'_300x300.jpg'
            except Exception as e:
                thumbnail_url = ""

            car_data = {
                "post-id" : item['data-pid'],
                "datetime" : item.find(class_="result-date")['datetime'],
                "title" : item.find(class_="result-title hdrlnk").text,
                "price" : item.find(class_="result-price").text,
                "url" : item.find(class_="result-title hdrlnk")['href'],
                "thumbnail-url" : thumbnail_url
            }

            results.append(car_data)
        
        return results

    def fetch_data(self):
        # Main driver for this class, makes all appropriate method calls
        # to retrieve data from Craigslist
        html_response = self.get_html_content()
        soup_obj = self.parse_html_content(html_response)
        data = self.convert_html_to_json(soup_obj)
        return data