""" ae.notify unit tests """
from unittest.mock import MagicMock, Mock, patch

from ae.notify import (
    DEF_ENC_PORT, DEF_ENC_SERVICE_NAME, SSL_ENC_PORT, SSL_ENC_SERVICE_NAME, TLS_ENC_PORT, TLS_ENC_SERVICE_NAME,
    Notifications)


class TestNotificationsClassInit:
    def test_init_all_defaults(self):
        instance = Notifications()

        assert instance._mail_service == DEF_ENC_SERVICE_NAME
        assert instance._user_name == ""
        assert instance._user_password == ""
        assert instance._mail_host == ""
        assert instance._mail_port == DEF_ENC_PORT
        assert instance._mail_from == ""
        assert instance._local_mail_host == ""

        assert instance._telegram_token == ""

        assert instance._whatsapp_token == ""
        assert instance._whatsapp_sender_id == ""

    def test_init_email(self):
        service = "service"
        usr = "user"
        pw = "password"
        host = "mail host"
        port = 999
        sender = "mail from"
        local_host = "local mail host"
        uri = service + "://" + usr + ":" + pw + "@" + host + ":" + str(port)

        instance = Notifications(uri)

        assert instance._mail_service == service
        assert instance._user_name == usr
        assert instance._user_password == pw
        assert instance._mail_host == host
        assert instance._mail_port == port
        assert instance._mail_from == ""
        assert instance._local_mail_host == host

        instance = Notifications(uri, mail_from=sender, local_mail_host=local_host)

        assert instance._mail_service == service
        assert instance._user_name == usr
        assert instance._user_password == pw
        assert instance._mail_host == host
        assert instance._mail_port == port
        assert instance._mail_from == sender
        assert instance._local_mail_host == local_host

        uri = service + "://" + usr + "@" + host + ":" + str(port)

        instance = Notifications(uri)

        assert instance._mail_service == service
        assert instance._user_name == usr
        assert instance._user_password == ""
        assert instance._mail_host == host
        assert instance._mail_port == port
        assert instance._mail_from == ""
        assert instance._local_mail_host == host

    def test_init_telegram(self):
        token = "token string"

        instance = Notifications(telegram_token=token)

        assert instance._telegram_token == token

    def test_init_whatsapp(self):
        sender = "sender name"
        token = "token string"

        instance = Notifications(whatsapp_token=token, whatsapp_sender=sender)

        assert instance._whatsapp_token == token
        assert instance._whatsapp_sender_id == sender

    def test_unsupported_notify_service(self):
        instance = Notifications()
        assert "not supported" in instance.send_notification("msg body", "unsupported_service" + ":" + "y" + "=" + "x")


class TestNotificationEmail:
    def test_send_email_host_err(self):
        instance = Notifications()

        err_msg = instance.send_email("body", "addr", "subject", "name")

        assert "mail server not configured" in err_msg

    def test_send_email_host_exception(self):
        instance = Notifications(smtp_server_uri="host")

        err_msg = instance.send_email("body", "addr", "subject", "name")

        assert "email send exception" in err_msg

    @patch('ae.notify.SMTP')
    def test_send_email_unreached_recipient_error(self, mocked_smtp):
        mocked_session = mocked_smtp.return_value.__enter__
        mocked_session.return_value = Mock(send_message=lambda *args: "unreached")
        instance = Notifications(smtp_server_uri="smtp.host")

        assert "unreached" in instance.send_email("mail body", "receiver addr", "subject", "receiver name")

    @patch('ae.notify.SMTP')
    def test_send_email_simple(self, mocked_smtp):
        mocked_session = mocked_smtp.return_value.__enter__
        mocked_session.return_value = Mock(send_message=lambda *args: "")
        instance = Notifications(smtp_server_uri="smtp.host")

        assert instance.send_email("mail body", "receiver addr", "subject", "receiver name") == ""

    @patch('ae.notify.SMTP')
    def test_send_email_simple_via_send_notification(self, mocked_smtp):
        mocked_session = mocked_smtp.return_value.__enter__
        mocked_session.return_value = Mock(send_message=lambda *args: "")
        instance = Notifications(smtp_server_uri="smtp.host")

        assert instance.send_notification("mail body", "mailto" + ":" + "receiver addr" + "=" + "name", "subject") == ""

    # noinspection DuplicatedCode
    @patch('ae.notify.SMTP')
    def test_send_email_send_message_args(self, mocked_smtp):
        body = "mail body"
        addr = "address of receiver"
        subject = "mail subject"
        name = "name of receiver"
        mocked_session = mocked_smtp.return_value.__enter__
        mocked_session.return_value = MagicMock()
        instance = Notifications(smtp_server_uri="smtp.host")

        err_msg = instance.send_email(body, addr, subject, name)

        assert name in err_msg
        assert ('Subject', subject) in mocked_session.return_value.send_message.call_args.args[0]._headers
        assert ('From', instance._mail_from) in mocked_session.return_value.send_message.call_args.args[0]._headers
        assert ('To', addr) in mocked_session.return_value.send_message.call_args.args[0]._headers
        assert mocked_session.return_value.send_message.call_args.args[0]._payload == body
        assert mocked_session.return_value.send_message.call_args.args[1] == instance._mail_from
        assert mocked_session.return_value.send_message.call_args.args[2] == addr

    # noinspection DuplicatedCode
    @patch('ae.notify.SMTP_SSL')
    def test_send_email_send_message_args_ssl(self, mocked_smtp):
        body = "mail body"
        addr = "address of receiver"
        subject = "mail subject"
        name = "name of receiver"
        mocked_session = mocked_smtp.return_value.__enter__
        mocked_session.return_value = MagicMock()
        instance = Notifications(smtp_server_uri="smtp.host:" + str(SSL_ENC_PORT))

        err_msg = instance.send_email(body, addr, subject, name)

        assert instance._mail_service == SSL_ENC_SERVICE_NAME
        assert name in err_msg
        assert ('Subject', subject) in mocked_session.return_value.send_message.call_args.args[0]._headers
        assert ('From', instance._mail_from) in mocked_session.return_value.send_message.call_args.args[0]._headers
        assert ('To', addr) in mocked_session.return_value.send_message.call_args.args[0]._headers
        assert mocked_session.return_value.send_message.call_args.args[0]._payload == body
        assert mocked_session.return_value.send_message.call_args.args[1] == instance._mail_from
        assert mocked_session.return_value.send_message.call_args.args[2] == addr

    # noinspection DuplicatedCode
    @patch('ae.notify.SMTP')
    def test_send_email_send_message_and_login_args_tls(self, mocked_smtp):
        body = "mail body"
        addr = "address of receiver"
        subject = "mail subject"
        name = "name of receiver"
        usr = "user name"
        pw = "password"
        mocked_session = mocked_smtp.return_value.__enter__
        mocked_session.return_value = MagicMock()
        instance = Notifications(smtp_server_uri=usr + ":" + pw + "@" + "smtp.host" + ":" + str(TLS_ENC_PORT))

        err_msg = instance.send_email(body, addr, subject, name)

        assert instance._mail_service == TLS_ENC_SERVICE_NAME
        assert name in err_msg
        assert ('Subject', subject) in mocked_session.return_value.send_message.call_args.args[0]._headers
        assert ('From', instance._mail_from) in mocked_session.return_value.send_message.call_args.args[0]._headers
        assert ('To', addr) in mocked_session.return_value.send_message.call_args.args[0]._headers
        assert mocked_session.return_value.send_message.call_args.args[0]._payload == body
        assert mocked_session.return_value.send_message.call_args.args[1] == instance._mail_from
        assert mocked_session.return_value.send_message.call_args.args[2] == addr
        assert mocked_session.return_value.login.call_args.args[0] == usr
        assert mocked_session.return_value.login.call_args.args[1] == pw


class TestNotificationTelegram:
    def test_send_telegram_empty_token_err(self):
        receiver_name = "name"
        instance = Notifications()

        err_msg = instance.send_telegram("msg_body", "chat id", receiver_name)

        assert err_msg != ""
        assert "error" in err_msg
        assert "missing token" in err_msg
        assert receiver_name in err_msg

    @patch('requests.post')
    def test_send_telegram_host_err(self, mocked_post):
        msg_body = "message body"
        chat_id = "chat id"
        receiver_name = "name"
        returned_err_json = "returned error detail"
        mocked_post.return_value = Mock(status_code=501, json=lambda: returned_err_json)
        instance = Notifications(telegram_token="some token string")

        err_msg = instance.send_telegram(msg_body, chat_id, receiver_name)

        assert err_msg != ""
        assert "error" in err_msg
        assert receiver_name in err_msg
        assert returned_err_json in err_msg

    @patch('requests.post')
    def test_send_telegram_missing_json_mock_exception(self, mocked_post):
        msg_body = "message body"
        chat_id = "chat id"
        receiver_name = "name"
        mocked_post.return_value = Mock(status_code=501, json="not a callable to raise exception")
        instance = Notifications(telegram_token="some token string")

        err_msg = instance.send_telegram(msg_body, chat_id, receiver_name)

        assert err_msg != ""
        assert "error" in err_msg
        assert receiver_name in err_msg
        assert "is not callable" in err_msg

    @patch('requests.post')
    def test_send_telegram_simple_via_send_notification(self, mocked_post):
        subject = "subject"
        msg_body = "message body"
        chat_id = "chat id"
        mocked_post.return_value = Mock(status_code=200)
        instance = Notifications(telegram_token="dummy-telegram-token")

        assert instance.send_notification(msg_body, "telegram" + ":" + chat_id + "=" + "name", subject=subject) == ""

        assert mocked_post.call_args.kwargs['json']['text'] == subject + "\n\n" + msg_body
        assert mocked_post.call_args.kwargs['json']['chat_id'] == chat_id
        assert mocked_post.call_args.kwargs['json']['parse_mode'] == "HTML"

    @patch('requests.post')
    def test_send_telegram_to_html(self, mocked_post):
        msg_body = "message\nbody"
        chat_id = "chat ei-di"
        mocked_post.return_value = Mock(status_code=200)
        instance = Notifications(telegram_token="dummy_telegram_token")

        assert instance.send_telegram(msg_body, chat_id, "name", mime_type="to_" + "html") == ""

        assert mocked_post.call_args.kwargs['json']['text'] == msg_body     # Telegram don't support <br>
        assert mocked_post.call_args.kwargs['json']['chat_id'] == chat_id
        assert mocked_post.call_args.kwargs['json']['parse_mode'] == "HTML"

    @patch('requests.post')
    def test_send_telegram_to_plain_body(self, mocked_post):
        msg_body = "<br>send html as <br> plain message body<br>"
        chat_id = "chat identifier"
        mocked_post.return_value = Mock(status_code=200)
        instance = Notifications(telegram_token="dummy_telegram_token")

        assert instance.send_telegram(msg_body, chat_id, "name", mime_type='to_plain') == ""

        assert mocked_post.call_args.kwargs['json']['text'] == msg_body.replace("<br>", "\n")
        assert mocked_post.call_args.kwargs['json']['chat_id'] == chat_id
        assert 'parse_mode' not in mocked_post.call_args.kwargs['json']


class TestNotificationWhatsapp:
    def test_send_whatsapp_empty_token_err(self):
        receiver_name = "name"
        instance = Notifications()

        err_msg = instance.send_whatsapp("msg_body", "chat id", receiver_name)

        assert err_msg != ""
        assert "error" in err_msg
        assert "missing token" in err_msg
        assert receiver_name in err_msg

    @patch('requests.post')
    def test_send_whatsapp_host_err(self, mocked_post):
        msg_body = "message body"
        chat_id = "chat id"
        receiver_name = "name"
        returned_err_json = "returned error detail"
        mocked_post.return_value = Mock(status_code=501, json=lambda: returned_err_json)
        instance = Notifications(whatsapp_token="some token string", whatsapp_sender="sender id")

        err_msg = instance.send_whatsapp(msg_body, chat_id, receiver_name)

        assert err_msg != ""
        assert "error" in err_msg
        assert receiver_name in err_msg
        assert returned_err_json in err_msg

    @patch('requests.post')
    def test_send_whatsapp_missing_json_mock_exception(self, mocked_post):
        msg_body = "message body"
        chat_id = "chat id"
        receiver_name = "name"
        mocked_post.return_value = Mock(status_code=501, json="not a callable to raise exception")
        instance = Notifications(whatsapp_token="some token string", whatsapp_sender="sender id")

        err_msg = instance.send_whatsapp(msg_body, chat_id, receiver_name)

        assert err_msg != ""
        assert "error" in err_msg
        assert receiver_name in err_msg
        assert "is not callable" in err_msg

    @patch('requests.post')
    def test_send_whatsapp_simple_via_send_notification(self, mocked_post):
        subject = "subject"
        msg_body = "message body"
        chat_id = "chat id"
        mocked_post.return_value = Mock(status_code=200)
        instance = Notifications(whatsapp_token="dummy-whatsapp-token", whatsapp_sender="sender id")

        assert instance.send_notification(msg_body, "whatsapp" + ":" + chat_id + "=" + "name", subject=subject) == ""

        assert mocked_post.call_args.kwargs['json']['text']['body'] == subject + "\n\n" + msg_body
        assert mocked_post.call_args.kwargs['json']['to'] == chat_id
        assert mocked_post.call_args.kwargs['json']['type'] == "text"

    @patch('requests.post')
    def test_send_whatsapp_to_html(self, mocked_post):
        msg_body = "message\nbody"
        chat_id = "chat ei-di"
        mocked_post.return_value = Mock(status_code=200)
        instance = Notifications(whatsapp_token="dummy_whatsapp_token", whatsapp_sender="sender id")

        assert instance.send_whatsapp(msg_body, chat_id, "name", mime_type="to_" + "html") == ""

        assert mocked_post.call_args.kwargs['json']['text']['body'] == msg_body     # Whatsapp don't support <br>
        assert mocked_post.call_args.kwargs['json']['to'] == chat_id
        assert mocked_post.call_args.kwargs['json']['type'] == "text"

    @patch('requests.post')
    def test_send_whatsapp_to_plain_body(self, mocked_post):
        msg_body = "<br>send html as <br> plain message body<br>"
        chat_id = "chat identifier"
        mocked_post.return_value = Mock(status_code=200)
        instance = Notifications(whatsapp_token="dummy_whatsapp_token", whatsapp_sender="sender id")

        assert instance.send_whatsapp(msg_body, chat_id, "name", mime_type='to_plain') == ""

        assert mocked_post.call_args.kwargs['json']['text']['body'] == msg_body.replace("<br>", "\n")
        assert mocked_post.call_args.kwargs['json']['to'] == chat_id
        assert mocked_post.call_args.kwargs['json']['type'] == "text"
