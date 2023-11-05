
"""Send an email message from the user's account.
"""

from django.core.mail import EmailMessage
# from django.conf import settings
# import base64
# import httplib2
#
# from email.mime.text import MIMEText
#
# from apiclient.discovery import build
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.file import Storage
# from oauth2client import tools
# from sparkpost import SparkPost

import logging
logger = logging.getLogger(__name__)


def send_mail(recipient, subject, message):
    try:
        email = EmailMessage(subject, message, to=recipient)
        email.send()
    except Exception as e:
        logger.error(e)


# def send_mail_message(to, subject, message_text):
#
#     # Path to the client_secret.json file downloaded from the Developer Console
#     CLIENT_SECRET_FILE = settings.BASE_DIR+'/core/client_secret_gmail.json'
#
#     # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
#     OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'
#
#     # Location of the credentials storage file
#     STORAGE = Storage('gmail.storage')
#
#     # Start the OAuth flow to retrieve credentials
#     flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
#     http = httplib2.Http()
#
#     # Try to retrieve credentials from storage or run the flow to generate them
#     credentials = STORAGE.get()
#     if credentials is None or credentials.invalid:
#         flags = tools.argparser.parse_args(args=[])
#         credentials = tools.run_flow(flow, STORAGE, flags)
#
#     # Authorize the httplib2.Http object with our credentials
#     http = credentials.authorize(http)
#
#     # Build the Gmail service from discovery
#     gmail_service = build('gmail', 'v1', http=http)
#
#     # create a message to send
#     message = MIMEText(message_text)
#     message['to'] = to
#     message['from'] = settings.EMAIL_HOST_USER
#     message['subject'] = subject
#     body = {'raw': base64.b64encode(message.as_string())}
#
#     # send it
#     try:
#         message = (gmail_service.users().messages().send(userId='me', body=body).execute())
#     except Exception as error:
#         logger.error(error)
#
#
# def send_mail_using_sparkpost(to, subject, message_text):
#     try:
#         sp = SparkPost(settings.SPARKPOST_API_KEY)
#         response = sp.transmissions.send(
#             use_sandbox=True,
#             recipients=to,
#             html='<p>'+message_text+'</p>',
#             from_email=settings.EMAIL_HOST_USER,
#             subject=subject
#         )
#         print(response)
#     except Exception as e:
#         print e
#         logger.error(e)