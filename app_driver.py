from fetch_data.fetcher import Fetcher
from verify_data.verifier import Verifier
from send_data.sender import Sender
import os, schedule, time, uuid


def run_script(sender_email, sender_pass, url, receiver_email, public_id):
    # First create a fetcher object to grab the data
    from datetime import datetime
    fetcher = Fetcher(url)
    new_data = fetcher.fetch_data()
    print("--------------------------------------------------")
    # print("Retrieved new response at "+str(datetime.utcnow())+" for "+receiver_email)
    # print("Retrieved new response for "+receiver_email)
    print("\n\n")

    # Check json-store dir path
    if not os.path.exists("json_store"):
        os.makedirs("json_store")

    # Now verify the new data against the existing data
    file_path = "json_store/"+str(public_id)+".json"
    data_verifier = Verifier()
    existing_data = data_verifier.get_data_from_file(file_path)
    unseen_items = data_verifier.filter_new_items(existing_data, new_data)

    if unseen_items != []:
        print("Unseen data: ")
        print(unseen_items)
        print("\n\n")

        # Write the new data to the existing data-store
        data_verifier.write_to_json_file(new_data, file_path)

        # and then email the unseen items
        print("Sending email now...")
        sender = Sender(sender_email, sender_pass, receiver_email)
        if sender.send_email(unseen_items) != 200:
            print("Email failed to send")

    else:
        print("No new data.")

    print("--------------------------------------------------")

if __name__ == "__main__":
    sender_email = str(os.environ.get('SENDER_EMAIL'))
    sender_pass = str(os.environ.get('SENDER_PASS'))

    users = [
        {
            "email" : str(os.environ.get('RECEIVER_EMAIL')),
            "public_id" : str(uuid.uuid4()),
            "url" : "https://slo.craigslist.org/search/cta?query=4runner&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=104&nearbyArea=7&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=103&nearbyArea=209&nearbyArea=92&nearbyArea=12&nearbyArea=8&nearbyArea=62&nearbyArea=710&nearbyArea=1&nearbyArea=97&nearbyArea=208&nearbyArea=346&nearbyArea=456&min_price=500&max_price=8500&min_auto_year=2000&max_auto_year=2009&auto_drivetrain=3&auto_title_status=1"
        },
    ]

    for user in users:
        schedule.every(30).seconds.do(run_script, sender_email, sender_pass, user['url'], user['email'], user['public_id'])
    
    while True:
        schedule.run_pending()
        time.sleep(1)


