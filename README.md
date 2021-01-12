# Craigslist Alert System
__________________________________

This Craigslist Alert System is a tool that will notify you anytime a new posting that matches your parameters appears, via email. Why not just use the pre-existing alert system? Well, it's not the best and can sometimes lead to missed listings. Using this ensures that you recieve notification of a listing as soon as possible, giving you full autonomy and customization. 

Some reasons to use this –

  - Run the script locally or on the cloud
  - Modify it to suit your needs
  - Be the first to see new listings (ex, PS5 for less than $600)
  - No need to rely on craigslist servers & latency issues

## Installation
__________________________________

This tool requires [Python](https://python.org/) to run. Any version >= 2.7 should do however there may be packages that require Python3+ as a minimum in the future.

To get up and going –
    1. Launch a virtual environment (optional)
    2. Install the dependencies
    3. Create a Gmail account to send the emails from
    4. Modify the main script with your emails, credentials, and URL
    
```sh
$ cd craigslist-alert-system
$ pip install -r requirements.txt
$ python app.py
```

## File Structure Overview
__________________________________

### fetch_data/fetcher.py 
| Function(Parameters) | Return Value | Description |
| ------ | ------ | ------ |
| **init(url)** | None | constructor, takes in URL as param |
| **get_html_content()** | HTTP response content, in bytes | makes an HTTP request to craigslist.org to retrieve HTML |
| **parse_html_content(html_byte_content)** | BeautifulSoup traversable object |filters HTML for data and converts to a BeautifulSoup object |
| **convert_html_to_json(bs4_object)** | JSON / Python list of dictionaries |parses BS4 object for structured data and converts to a JSON delimited object |
| **fetch_data()** | JSON / Python list of dictionaries | main entry point for an instance of this class, accesses self methods to return a dictionary/JSON object of data |

### verify_data/verifier.py
| Function(Parameters) | Return Value | Description |
| ------ | ------ | ------ |
| **init()** | None | constructor, takes in no params |
| **get_data_from_file(file_path)** | Python Dictionary | Loads a JSON file into a Python dictionary that can live on memory temporarily |
| **filter_new_items(existing_data, new_data)** | JSON / Python list of dictionaries | Creates a set of the existing items, and then does a lookup with the new data to see if there's anything that is not in the existing data. If so return that, as its a new item that needs to be emailed |
| **write_to_json_file(json_data, file_path)** | None | Writes any Python dict to a JSON file using this interface |

### send_data/sender.py
| Function(Parameters) | Return Value | Description |
| ------ | ------ | ------ |
| **init(sender_email, sender_password, receiver_email)** | None | constructor, takes in the sender's email & pass as well as the receiver's email |
| **send_email(json_data):** | Status code, 2xx or 5xx | Sends structured JSON data to the receiver's email using the sender's credentials |

## License
__________________________________

Distributed under the MIT License. See LICENSE for more information.
**Free Software, Hell Yeah!**


