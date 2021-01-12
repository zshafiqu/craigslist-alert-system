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
    '''
    Use linux screen to manage background scripts on ec2 centOS ... 
    see https://stackoverflow.com/questions/23166158/make-python-script-to-run-forever-on-amazon-ec2
    https://stackoverflow.com/questions/537942/how-to-list-running-screen-sessions
    https://askubuntu.com/questions/356006/kill-a-screen-session

    '''
    queries = [
        {
            "email" : os.environ.get('RECEIVER_EMAIL'),
            "query_name" : "4th gen 4Runner 4WD, max price $8,999",
            "public_id" : uuid.uuid4(),
            "url" : "https://sfbay.craigslist.org/search/cta?query=4runner&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=189&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=188&nearbyArea=92&nearbyArea=12&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=708&nearbyArea=97&nearbyArea=707&nearbyArea=208&nearbyArea=346&nearbyArea=456&min_price=1000&max_price=8999&min_auto_year=2003&max_auto_year=2009&min_auto_miles=NaN&auto_drivetrain=3&auto_title_status=1"
        },
        {
            "email" : os.environ.get('RECEIVER_EMAIL'),
            "query_name" : "4th gen 4 Runner 4WD, max price $8,999",
            "public_id" : uuid.uuid4(),
            "url" : "https://sfbay.craigslist.org/search/cta?query=4+runner&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=189&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=188&nearbyArea=92&nearbyArea=12&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=708&nearbyArea=97&nearbyArea=707&nearbyArea=208&nearbyArea=346&nearbyArea=456&min_price=1000&max_price=8999&min_auto_year=2003&max_auto_year=2009&min_auto_miles=NaN&auto_drivetrain=3&auto_title_status=1"
        },
        {
            "email" : os.environ.get('RECEIVER_EMAIL'),
            "query_name" : "3rd gen 4Runner 4WD, max price $5,500",
            "public_id" : uuid.uuid4(),
            "url" : "https://sfbay.craigslist.org/search/cta?query=4runner&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=189&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=188&nearbyArea=92&nearbyArea=12&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=708&nearbyArea=97&nearbyArea=707&nearbyArea=208&nearbyArea=346&nearbyArea=456&min_price=1000&max_price=5500&min_auto_year=2000&max_auto_year=2002&auto_drivetrain=3&auto_title_status=1"
        },
        {
            "email" : os.environ.get('RECEIVER_EMAIL'),
            "query_name" : "3rd gen 4 Runner 4WD, max price $5,500",
            "public_id" : uuid.uuid4(),
            "url" : "https://sfbay.craigslist.org/search/cta?query=4+runner&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=189&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=188&nearbyArea=92&nearbyArea=12&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=708&nearbyArea=97&nearbyArea=707&nearbyArea=208&nearbyArea=346&nearbyArea=456&min_price=1000&max_price=5500&min_auto_year=2000&max_auto_year=2002&auto_drivetrain=3&auto_title_status=1"
        },
        {
            "email" : os.environ.get('RECEIVER_EMAIL'),
            "query_name" : "rx350, max price $6,000",
            "public_id" : uuid.uuid4(),
            "url" : "https://sfbay.craigslist.org/search/cta?query=rx350&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=189&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=188&nearbyArea=92&nearbyArea=12&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=708&nearbyArea=97&nearbyArea=707&nearbyArea=208&nearbyArea=346&nearbyArea=456&min_price=1000&max_price=6000&auto_title_status=1"
        },
        {
            "email" : os.environ.get('RECEIVER_EMAIL'),
            "query_name" : "rx 350, max price $6,000",
            "public_id" : uuid.uuid4(),
            "url" : "https://sfbay.craigslist.org/search/cta?query=rx+350&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=189&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=188&nearbyArea=92&nearbyArea=12&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=708&nearbyArea=97&nearbyArea=707&nearbyArea=208&nearbyArea=346&nearbyArea=456&min_price=1000&max_price=6000&auto_title_status=1"
        },
        {
            "email" : os.environ.get('RECEIVER_EMAIL'),
            "query_name" : "rx330, max price $6,000",
            "public_id" : uuid.uuid4(),
            "url" : "https://sfbay.craigslist.org/search/cta?query=rx330&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=189&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=188&nearbyArea=92&nearbyArea=12&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=708&nearbyArea=97&nearbyArea=707&nearbyArea=208&nearbyArea=346&nearbyArea=456&min_price=1000&max_price=6000&auto_title_status=1"
        },
        {
            "email" : os.environ.get('RECEIVER_EMAIL'),
            "query_name" : "rx 330, max price $6,000",
            "public_id" : uuid.uuid4(),
            "url" : "https://sfbay.craigslist.org/search/cta?query=rx+330&srchType=T&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=189&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=188&nearbyArea=92&nearbyArea=12&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=708&nearbyArea=97&nearbyArea=707&nearbyArea=208&nearbyArea=346&nearbyArea=456&min_price=1000&max_price=6000&auto_title_status=1"
        },
    ]

    sender_email = os.environ.get('SENDER_EMAIL')
    sender_pass = os.environ.get('SENDER_PASS')

    for query in queries:
        schedule.every(2).minutes.do(
            run_script, sender_email, sender_pass, query['url'], query['email'], query['public_id']
            )
    
    while True:
        schedule.run_pending()
        time.sleep(1)


