from email.message import EmailMessage
from unittest.mock import Mock, mock_open, patch

from modules.mail_sender import MailSender


def test_create_message():

    sender = MailSender.__new__(MailSender)

    sender.sender = "from@test.com"
    sender.tos = ["to@test.com"]

    sender.config = {
        "mail": {
            "subject": "テスト件名"
        }
    }

    msg = sender._create_message("本文")

    assert msg["Subject"] == "テスト件名"
    assert msg["From"] == "from@test.com"
    assert msg["To"] == "to@test.com"
    assert msg.get_content().strip() == "本文"


@patch("builtins.open", new_callable=mock_open, read_data=b"dummy")
def test_attach_files(mock_file):

    sender = MailSender.__new__(MailSender)

    msg = EmailMessage()

    sender._attach_files(
        msg,
        [
            "a.pdf",
            "b.pdf"
        ]
    )

    assert len(list(msg.iter_attachments())) == 2
    assert mock_file.call_count == 2


@patch("modules.mail_sender.smtplib.SMTP")
def test_send(mock_smtp):

    sender = MailSender.__new__(MailSender)

    sender.sender = "from@test.com"
    sender.password = "password"

    sender.config = {
        "mail": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587
        }
    }

    msg = EmailMessage()

    sender._send(msg)

    smtp = mock_smtp.return_value.__enter__.return_value

    smtp.starttls.assert_called_once()

    smtp.login.assert_called_once_with(
        "from@test.com",
        "password"
    )

    smtp.send_message.assert_called_once_with(msg)


def test_send_mail():

    sender = MailSender.__new__(MailSender)

    sender.logger = Mock()

    sender.sender = "from@test.com"
    sender.password = "password"
    sender.tos = ["to@test.com"]

    sender._create_message = Mock(return_value=Mock())
    sender._attach_files = Mock()
    sender._send = Mock()

    sender.send_mail(
        body="本文",
        attachment_files=["a.pdf"]
    )

    sender._create_message.assert_called_once_with("本文")

    sender._attach_files.assert_called_once()

    sender._send.assert_called_once()
