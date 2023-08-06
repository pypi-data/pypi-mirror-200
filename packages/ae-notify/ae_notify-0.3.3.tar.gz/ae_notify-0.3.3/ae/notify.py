"""
send notifications via email, telegram or whatsapp
==================================================

this pure python module depends mainly on the Standard Python Libraries :mod:`email` and :mod:`smtplib` and the external
:mod:`requests` module.

an instance of the :class:`Notifications` has to be created for each notification sender in your app, providing the
sender's credentials for each used notification channel (service).

the notification channels and the receiver(s) can be specified individually for each notification message to send.

"""
import re
import requests                                     # type: ignore

from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL
from typing import Tuple


__version__ = '0.3.3'


# default service names and ports of the SMTP protocol
DEF_ENC_PORT = 25                       #: standard SMTP port
DEF_ENC_SERVICE_NAME = 'smtp'           #: standard SMTP service name
SSL_ENC_PORT = 465                      #: port to use SMTP via SSL
SSL_ENC_SERVICE_NAME = 'smtps'          #: service name in :paramref:`Notifications.smtp_server_uri` of SMTP via SSL
TLS_ENC_PORT = 587                      #: port to use SMTP via TLS
TLS_ENC_SERVICE_NAME = 'smtpTLS'        #: service name in :paramref:`Notifications.smtp_server_uri` of SMTP via TLS

#: message length maximum restrictions
TELEGRAM_MESSAGE_MAX_LEN = 4096         #: maximum length of Telegram notification message body
WHATSAPP_MESSAGE_MAX_LEN = 65536        #: maximum length of Whatsapp notification message body


def _body_mime_type_conversion(msg_body: str, mime_type: str) -> Tuple[str, str]:
    """ convert content of notification message body.

    :param msg_body:            message body string.
    :param mime_type:           mime type to convert to, if it has the "to" prefix in front of the resulting mime type.
    :return:                    tuple of converted message body and resulting mime type (removing the "to" prefix).
    """
    if mime_type == 'to_html':
        msg_body = msg_body.replace('\n', '<br>')
        mime_type = 'html'
    elif mime_type == 'to_plain':
        msg_body = msg_body.replace('<br>', '\n')
        mime_type = 'plain'
    return msg_body, mime_type


class Notifications:
    """ a single instance of this class can be used to handle all notifications of an app/service. """
    def __init__(self,
                 smtp_server_uri: str = "", mail_from: str = "", local_mail_host: str = '',
                 telegram_token: str = "",
                 whatsapp_token: str = "", whatsapp_sender: str = ""):
        """ initialize one or more different services for a sender of multiple notifications to individual receivers.

        :param smtp_server_uri: host and optional port and user credentials of email SMTP server to use, in the format
                                [service://][user[:password]@]mail_server_host[:mail_server_port]. default SMTP ports:
                                25/DEF_ENC_PORT, port 587/TSL_ENC_PORT for E-SMTP/TLS or 465/SSL_ENC_PORT for smtps/SSL.
        :param mail_from:       email sender address.
        :param local_mail_host: FQDN of the local email host in the SMTP HELO/EHLO command.

        :param telegram_token:  token for the Telegram cloud API obtained from the BotFather.

        :param whatsapp_token:  token for the WhatsApp cloud API obtained from the developer portal.
        :param whatsapp_sender: sender phone number id for the WhatsApp cloud API obtained from the developer portal.
        """

        # split smtp server URI into service, host, user, pw and port (all apart from the host address are optional)
        if '://' in smtp_server_uri:
            self._mail_service, smtp_server_uri = smtp_server_uri.split("://")
        else:
            self._mail_service = DEF_ENC_SERVICE_NAME

        if '@' in smtp_server_uri:
            pos = smtp_server_uri.rindex("@")
            user_info = smtp_server_uri[:pos]
            mail_host = smtp_server_uri[pos + 1:]
            if ':' in user_info:
                pos = user_info.index(":")
                self._user_name = user_info[:pos]
                self._user_password = user_info[pos + 1:]
            else:
                self._user_name = user_info
                self._user_password = ""
        else:
            mail_host = smtp_server_uri
            self._user_name = ""
            self._user_password = ""

        if ':' in mail_host:
            pos = mail_host.rindex(":")
            self._mail_host = mail_host[:pos]
            self._mail_port = int(mail_host[pos + 1:])
            if self._mail_service == DEF_ENC_SERVICE_NAME:
                if self._mail_port == SSL_ENC_PORT:
                    self._mail_service = SSL_ENC_SERVICE_NAME
                elif self._mail_port == TLS_ENC_PORT:
                    self._mail_service = TLS_ENC_SERVICE_NAME
        else:
            self._mail_host = mail_host
            self._mail_port = SSL_ENC_PORT if self._mail_service == SSL_ENC_SERVICE_NAME \
                else (TLS_ENC_PORT if self._mail_service == TLS_ENC_SERVICE_NAME
                      else DEF_ENC_PORT)

        self._mail_from = mail_from
        self._local_mail_host = local_mail_host or self._mail_host

        self._telegram_token = telegram_token

        self._whatsapp_token = whatsapp_token
        self._whatsapp_sender_id = whatsapp_sender

    def send_notification(self, msg_body: str, receiver: str, subject: str = "", mime_type: str = "to_html") -> str:
        """ send a notification message with optional subject to receiver via the specified service.

        :param msg_body:        message body. line breaks are converted (br-tag <-> newline character) in accordance
                                with mime_type.
        :param receiver:        receiver address in the format ``service:address=name``, where ``service`` is mailto,
                                telegram or whatsapp, ``address`` is an email address, a chat id or phone number and
                                ``name`` is the name of the receiving person.
        :param subject:         optional subject text. added to the top of the msg_body for messenger services,
                                separated by an empty line. if not specified or specified as empty string or as
                                a single space character, then it will not be added to the top of the message body.
        :param mime_type:       mime type ('html' or 'plain'), and optional conversion to it (if starts with 'to').
        :return:                error message on error or empty string if notification got send successfully.
        """
        service, addr_name = receiver.split(':')
        address, name = addr_name.split('=')
        if subject and subject != " " and service != 'mailto' and not subject.endswith('\n'):
            subject = f"{subject}\n\n"

        if service == 'mailto':
            err_msg = self.send_email(msg_body, address, subject, name, mime_type)
        elif service == 'telegram':
            err_msg = self.send_telegram(f"{subject}{msg_body}", address, name, mime_type)
        elif service == 'whatsapp':
            err_msg = self.send_whatsapp(f"{subject}{msg_body}", address, name, mime_type)
        else:
            err_msg = f"'{service}' notification service is not supported/implemented"

        return err_msg

    def send_email(self, msg_body: str, address: str, subject: str, name: str, mime_type: str = 'to_html') -> str:
        """ send email to the passed address.

        :param msg_body:        message body text. for new lines use newline char in plain and <br> in html mime_type.
        :param address:         email address of the receiver.
        :param subject:         email subject text.
        :param name:            name of the receiver.
        :param mime_type:       mime type ('html' or 'plain'), and optional conversion to it (if starts with 'to').
        :return:                error message on error or empty string if notification email got send successfully.
        """
        err_prefix = f"error sending {mime_type} email to {name}: "

        if not self._mail_host:
            return f"{err_prefix}mail server not configured"

        msg_body, mime_type = _body_mime_type_conversion(msg_body, mime_type)

        err_msg = ""
        try:
            message = MIMEText(msg_body, _subtype=mime_type)
            message['Subject'] = subject
            message['From'] = self._mail_from
            message['To'] = address
            # Oracle P_SENDMAIL() is using smtp server as local host
            # SMTP_SSL could throw "SSL:UNKNOWN_PROTOCOL" error
            srv = SMTP_SSL if self._mail_port == SSL_ENC_PORT or self._mail_service == SSL_ENC_SERVICE_NAME else SMTP
            with srv(self._mail_host, self._mail_port, local_hostname=self._local_mail_host) as session:
                # session.set_debuglevel(1)
                session.ehlo()
                # using session.starttls() could throw error "STARTTLS extension not supported by server."
                if self._mail_service == TLS_ENC_SERVICE_NAME:
                    session.starttls()
                if self._user_name:
                    session.login(self._user_name, self._user_password)
                unreached_recipients = session.send_message(message, self._mail_from, address)
                if unreached_recipients:
                    err_msg = f"{err_prefix}unreached email recipient '{unreached_recipients}'"
        except Exception as mex:
            err_msg = f"{err_prefix}email send exception '{mex}'"

        return err_msg

    def send_telegram(self, msg_body: str, chat_id: str, name: str, mime_type: str = 'to_html') -> str:
        """ send message to the passed telegram chat id.

        :param msg_body:        message body text. in 'html' mime_type message texts are only a few tags support by
                                Telegram (see https://core.telegram.org/bots/api#html-style). on top of that you can
                                also include the following tags, which will be either converted or removed:
                                * br: will be converted into a new line character.
                                * div: will be removed.
        :param chat_id:         chat id of the telegram receiver or group.
        :param name:            name of the receiver.
        :param mime_type:       mime type ('html' or 'plain'), and optional conversion to it (if starts with 'to').
        :return:                error message on error or empty string if notification got send successfully.
        """
        err_prefix = f"error sending '{mime_type}' Telegram message to '{name}': "

        if not self._telegram_token:
            return f"{err_prefix}missing token or sender id"

        msg_body, mime_type = _body_mime_type_conversion(msg_body, mime_type)
        if mime_type == 'html':
            msg_body = msg_body.replace('<br>', '\n').replace('<br />', '\n').replace('<br/>', '\n')
            msg_body = re.sub(r'<div[^<]+?>', "", msg_body.replace('</div>', ""))

        post_data = {'chat_id': chat_id, 'text': msg_body[:TELEGRAM_MESSAGE_MAX_LEN]}
        if mime_type == 'html':
            post_data['parse_mode'] = 'HTML'    # https://core.telegram.org/bots/update56kabdkb12ibuisabdubodbasbdaosd

        err_msg = ""
        try:
            response = requests.post(f"https://api.telegram.org/bot{self._telegram_token}/sendMessage", json=post_data)
            if response.status_code != 200:
                err_msg = f"{err_prefix}{response.json()}"
        except Exception as tex:
            err_msg = f"{err_prefix}{tex}"

        return err_msg

    def send_whatsapp(self, msg_body: str, receiver_id: str, name: str, mime_type: str = 'to_html') -> str:
        """ send message to the passed WhatsApp user/group.

        :param msg_body:        message body text. for new lines use newline char in plain and <br> in html mime_type.
        :param receiver_id:     phone number with country code (and a leading '+') of the WhatsApp receiver or the
                                id of the WA group (last part of the URL to invite somebody into the group).
        :param name:            name of the receiver.
        :param mime_type:       mime type ('html' or 'plain'), and optional conversion to it (if starts with 'to').
                                recognized/converted html tags are b, br, i and pre.
        :return:                error message on error or empty string if notification got send successfully.

        using WA Business API (see: https://developers.facebook.com/docs/whatsapp/on-premises/reference/messages and
        https://github.com/Neurotech-HQ/heyoo/blob/58ad576c3dfaf05bad5f342bc8614cf0ba02e6ae/heyoo/__init__.py#L43)
        has the restriction that the receiver has first to send a message to the sender to get a window of 24 hours.
        and using pyWhatKit's webbrowser-based approach will not work on PythonAnywhere because web.whatsapp.com is not
        in their whitelist (https://www.pythonanywhere.com/whitelist/)
        """
        err_prefix = f"error sending '{mime_type}' WhatsApp message to '{name}': "

        if not self._whatsapp_token or not self._whatsapp_sender_id:
            return f"{err_prefix}missing token or sender id"

        is_group = not receiver_id.startswith('+')
        msg_body, mime_type = _body_mime_type_conversion(msg_body, mime_type)
        if mime_type == 'html':
            msg_body = msg_body\
                .replace('<b>', '*').replace('</b>', '*') \
                .replace('<br>', '\n').replace('<br />', '\n').replace('<br/>', '\n') \
                .replace('<i>', '_').replace('</i>', '_') \
                .replace('<pre>', '```').replace('</pre>', '```')

        err_msg = ""
        try:
            response = requests.post(
                f"https://graph.facebook.com/v15.0/{self._whatsapp_sender_id}/messages",
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f"Bearer {self._whatsapp_token}"},
                json={
                    'messaging_product': 'whatsapp',
                    'recipient_type': 'group' if is_group else 'individual',
                    'to': receiver_id if is_group else receiver_id[1:].translate({ord(char): None for char in " /-"}),
                    'type': 'text',
                    'text': {'preview_url': True, 'body': msg_body[:WHATSAPP_MESSAGE_MAX_LEN]}})
            if response.status_code != 200:
                err_msg = f"{err_prefix}{response.json()}"
        except Exception as wex:
            err_msg = f"{err_prefix}{wex}"

        return err_msg
