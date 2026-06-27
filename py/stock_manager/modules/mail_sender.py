import smtplib
from email.message import EmailMessage
from pathlib import Path

from modules.logger import Logger
from modules.util import Util


class MailSender:

    def __init__(self, sender: str, password: str, tos: list[str], filename: str):

        self.config = Util.load_config(filename)

        self.logger = Logger.get_logger(
            self.config["log"]["filepath"],
            self.config["log"]["filename"]
        )

        self.sender = sender
        self.password = password
        self.tos = tos

    def _create_message(self, body: str) -> EmailMessage:

        mail_config = self.config["mail"]

        msg = EmailMessage()

        msg["Subject"] = mail_config["subject"]
        msg["From"] = self.sender
        msg["To"] = ",".join(self.tos)

        msg.set_content(body)

        return msg

    def _attach_files(
        self,
        msg: EmailMessage,
        attachment_files: list[str]
    ) -> None:

        for file_path in attachment_files:

            path = Path(file_path)

            with open(path, "rb") as f:

                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="pdf",
                    filename=path.name
                )

    def _send(
        self,
        msg: EmailMessage
    ) -> None:

        mail_config = self.config["mail"]

        with smtplib.SMTP(
            mail_config["smtp_server"],
            mail_config["smtp_port"]
        ) as smtp:

            smtp.starttls()

            smtp.login(
                self.sender,
                self.password
            )

            smtp.send_message(msg)

    def send_mail(
        self,
        body: str,
        attachment_files: list[str]
    ) -> None:

        self.logger.info("メール送信開始")

        if not self.password or not self.sender or not self.tos:
            self.logger.warning("password,sender,toを設定してください")
            return

        msg = self._create_message(body)

        self._attach_files(
            msg,
            attachment_files
        )

        self._send(msg)

        self.logger.info("メール送信終了")
