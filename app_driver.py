from fetch_data.fetcher import Fetcher
from verify_data.verifier import Verifier
from send_data.sender import Sender
import os, schedule, time, uuid, sys

def run_script(sender_email, sender_pass, receiver_email, query_name, url):
    # Open output destination file descriptor to direct print statements to logfile
    f = open("script-logs.txt", "a")

    # First create a fetcher object to grab the data
    from datetime import datetime,timezone
    fetcher = Fetcher(url)
    new_data = fetcher.fetch_data()
    curr_utc_time = datetime.now(timezone.utc)

    print("--------------------------------------------------", file=f)
    print("Retrieved new response for '"+query_name+"' at "+str(curr_utc_time), file=f)
    print("\n\n", file=f)

    # Check json-store dir path
    if not os.path.exists("json_store"):
        os.makedirs("json_store")

    # Now verify the new data against the existing data .. see if there is anything we haven't seen yet.
    file_path = "json_store/"+query_name+".json"
    data_verifier = Verifier()
    existing_data = data_verifier.get_data_from_file(file_path)
    unseen_items = data_verifier.filter_new_items(existing_data, new_data)

    # If there are some unseen items, process & email them ..!
    if unseen_items != []:
        print("Unseen data: ", file=f)
        print(unseen_items, file=f)
        print("\n\n", file=f)

        # Write the new data to the existing data-store
        data_verifier.write_to_json_file(new_data, file_path)

        # and then email the unseen items
        print("Sending email now...", file=f)
        sender = Sender(sender_email, sender_pass, receiver_email)
        if sender.send_email(query_name, unseen_items) != 200:
            print("Email failed to send", file=f)

    # If the unseen_items list is empty, that means the new response yielded no difference to the existing data .. so assume no new listings
    else:
        print("No new data.", file=f)

    # Print iteration delimiter and close file descriptor
    print("--------------------------------------------------", file=f)
    f.close() 

if __name__ == "__main__":
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_pass = os.environ.get('SENDER_PASS')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    
    reader = Verifier()
    queries = reader.get_data_from_file("query_list.json")

    for query in queries:
        schedule.every(5).minutes.do(
            run_script, sender_email, sender_pass, receiver_email, query['query_name'], query['url']
            )
    
    while True:
        schedule.run_pending()
        time.sleep(1)

    '''
    Use linux screen to manage background scripts on ec2 centOS ... see :
    - https://stackoverflow.com/questions/23166158/make-python-script-to-run-forever-on-amazon-ec2
    - https://stackoverflow.com/questions/537942/how-to-list-running-screen-sessions
    - https://askubuntu.com/questions/356006/kill-a-screen-session
    '''


