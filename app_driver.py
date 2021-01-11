from fetch_data.fetcher import Fetcher
from verify_data.verifier import Verifier
from send_data.sender import Sender

# First create a fetcher object to grab the data
url = "https://sfbay.craigslist.org/search/cta?query=4runner&srchType=T&hasPic=1&min_price=678&max_price=7500&min_auto_year=2003&max_auto_year=2009&auto_drivetrain=3"
fetcher = Fetcher(url)
new_data = fetcher.fetch_data()

print("Retrieved new data: ")
print(new_data)
print("\n\n\n")

# Now verify the new data against the existing data
file_path = "data_store.json"

data_verifier = Verifier()
existing_data = data_verifier.get_data_from_file(file_path)

print("Printing existing data: ")
print(existing_data)
print("\n\n\n")

unseen_items = data_verifier.filter_new_items(existing_data, new_data)

print("Unseen data, to be emailed: ")
print(unseen_items)
print("\n\n\n")

# Write the new data to the existing data-store
data_verifier.write_to_json_file(new_data, file_path)

# and then email the unseen items
import os
sender_email = os.environ.get('SENDER_EMAIL')
sender_pass = os.environ.get('SENDER_PASS')
receiver_email = os.environ.get('RECEIVER_EMAIL')

if unseen_items != []:
    print("Sending email now...")
    sender = Sender(sender_email, sender_pass, receiver_email)
    sender.send_email(unseen_items)

else:
    print("No new data.")





