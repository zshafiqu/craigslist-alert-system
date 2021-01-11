class Sender:

    def __init__(self, sender_email, sender_password, receiver_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email
        return None

    def send_email(self, json_data):
        import smtplib, ssl, jinja2
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        message = MIMEMultipart("alternative")
        message["Subject"] = "Craigslist Alert - New Listing(s)!"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        email_template = jinja2.Template("""\
            <html>
                <body>
                    <h2 style="text-decoration: underline;">New car(s) found. See below.</h2><br>
            
                    {% for item in data %}
                    <div style="border-style: double; padding: 10px; margin: 5px">
                        <p><b>ID: </b>{{item['post-id']}}</p>
                        <p><b>Date/Time: </b>{{item['datetime']}}</p>
                        <p><b>Title: </b>{{item['title']}}</p>
                        <p><b>Price: </b>{{item['price']}}</p>
                        <a href="{{item['url']}}">Click to see posting</a><br>
                        <img src="{{item['thumbnail-url']}}" alt="Car" style="margin-top: 10px;"> 
                    </div>
                    {% endfor %}
                </body>
            </html>
        """)

        final_html_message = email_template.render( {'data': json_data} )

        # Turn these into plain/html MIMEText objects
        # part1 = MIMEText(plain_text, "plain")
        content = MIMEText(final_html_message, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(content)

        # Create secure connection with server and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(
                    self.sender_email, self.receiver_email, message.as_string()
                )
                
            return 200
        except Exception as e:
            print(e)




if __name__ == "__main__":
    import os
    data = [
        {
            "post-id":"7259938926",
            "datetime":"2021-01-10 10:57",
            "title":"2015 Chevrolet Corvette Stingray Z06",
            "price":"$76,999",
            "url":"https://sfbay.craigslist.org/sby/ctd/d/sherman-2015-chevrolet-corvette/7259938926.html",
            "thumbnail-url":"https://images.craigslist.org/00u0u_kjVjN7fikt6z_0ak06T_300x300.jpg"
        },
                {
            "post-id":"7259938926",
            "datetime":"2021-01-10 10:57",
            "title":"2015 Chevrolet Corvette Stingray Z06",
            "price":"$76,999",
            "url":"https://sfbay.craigslist.org/sby/ctd/d/sherman-2015-chevrolet-corvette/7259938926.html",
            "thumbnail-url":"https://images.craigslist.org/00u0u_kjVjN7fikt6z_0ak06T_300x300.jpg"
        },
                {
            "post-id":"7259938926",
            "datetime":"2021-01-10 10:57",
            "title":"2015 Chevrolet Corvette Stingray Z06",
            "price":"$76,999",
            "url":"https://sfbay.craigslist.org/sby/ctd/d/sherman-2015-chevrolet-corvette/7259938926.html",
            "thumbnail-url":"https://images.craigslist.org/00u0u_kjVjN7fikt6z_0ak06T_300x300.jpg"
        }
    ]

    sender_email = os.environ.get('SENDER_EMAIL')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    password = os.environ.get('SENDER_PASS')

    sender_test = Sender(sender_email, password, receiver_email)

    print(sender_test.send_email(data))


# import smtplib, ssl, jinja2, os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart


# data = [
#         {
#             "post-id":"7259938926",
#             "datetime":"2021-01-10 10:57",
#             "title":"2015 Chevrolet Corvette Stingray Z06",
#             "price":"$76,999",
#             "url":"https://sfbay.craigslist.org/sby/ctd/d/sherman-2015-chevrolet-corvette/7259938926.html",
#             "thumbnail-url":"https://images.craigslist.org/00u0u_kjVjN7fikt6z_0ak06T_300x300.jpg"
#         },
#                 {
#             "post-id":"7259938926",
#             "datetime":"2021-01-10 10:57",
#             "title":"2015 Chevrolet Corvette Stingray Z06",
#             "price":"$76,999",
#             "url":"https://sfbay.craigslist.org/sby/ctd/d/sherman-2015-chevrolet-corvette/7259938926.html",
#             "thumbnail-url":"https://images.craigslist.org/00u0u_kjVjN7fikt6z_0ak06T_300x300.jpg"
#         },
#                 {
#             "post-id":"7259938926",
#             "datetime":"2021-01-10 10:57",
#             "title":"2015 Chevrolet Corvette Stingray Z06",
#             "price":"$76,999",
#             "url":"https://sfbay.craigslist.org/sby/ctd/d/sherman-2015-chevrolet-corvette/7259938926.html",
#             "thumbnail-url":"https://images.craigslist.org/00u0u_kjVjN7fikt6z_0ak06T_300x300.jpg"
#         }
#     ]


# sender_email = os.environ.get('SENDER_EMAIL')
# receiver_email = os.environ.get('RECEIVER_EMAIL')
# password = os.environ.get('SENDER_PASS')

# message = MIMEMultipart("alternative")
# message["Subject"] = "Craigslist Alert - New Listing(s)!"
# message["From"] = sender_email
# message["To"] = receiver_email

# # Create the plain-text and HTML version of your message
# # plain_text = """"""

# html_message = jinja2.Template("""\
#     <html>
#         <body>
#             <h2 style="text-decoration: underline;">New car(s) found. See below.</h2><br>
    
#             {% for item in data %}
#             <div style="border-style: double; padding: 10px; margin: 5px">
#                 <p><b>ID: </b>{{item['post-id']}}</p>
#                 <p><b>Date/Time: </b>{{item['datetime']}}</p>
#                 <p><b>Title: </b>{{item['title']}}</p>
#                 <p><b>Price: </b>{{item['price']}}</p>
#                 <a href="{{item['url']}}">Click to see posting</a><br>
#                 <img src="{{item['thumbnail-url']}}" alt="Car" style="margin-top: 10px;"> 
#             </div>
#             {% endfor %}
#         </body>
#     </html>
# """)

# html_message = html_message.render({'data': data})

# # Turn these into plain/html MIMEText objects
# # part1 = MIMEText(plain_text, "plain")
# part2 = MIMEText(html_message, "html")

# # Add HTML/plain-text parts to MIMEMultipart message
# message.attach(part2)

# # Create secure connection with server and send email
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(
#         sender_email, receiver_email, message.as_string()
#     )
