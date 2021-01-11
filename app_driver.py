from fetch_data.fetcher import Fetcher
from verify_data.verifier import Verifier
from send_data.sender import Sender

# First create a fetcher object to grab the data
url = "https://sfbay.craigslist.org/search/cta?query=4runner&srchType=T&hasPic=1&min_price=678&max_price=7500&min_auto_year=2003&max_auto_year=2009&auto_drivetrain=3"
test = Fetcher(url)
print(test.fetch_data())