class Sender:

    def __init__(self, sender_email, sender_password, receiver_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email
        return None

    def send_email(self, query_name, json_data):
        import smtplib, ssl, jinja2
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # Create message object to be sent in email
        message = MIMEMultipart("alternative")
        message["Subject"] = str(query_name)+" - New Listings!"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        # Simple Jinja2 template to render dynamic JSON in HTML
        email_template = jinja2.Template("""\
            <html>
                <body>
                    <h2 style="text-decoration: underline;">{{data|length}} new car(s) found. See below.</h2><br>
            
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

        # Turn these into HTML MIMEText objects, and then add HTML part to MIMEMultipart message
        content = MIMEText(final_html_message, "html")
        message.attach(content)

        # Attemp secure connection with server and send email, return 2xx status for success or 5xx otherwise
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            return 200
        except Exception as e:
            print(e)
            return 500