from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class NotificationService(object):
    def __init__(
        self,
        content: dict,
        recipients: list,
        sender: str,
        subject: str,
        reply: str = None,
        files: list = None,
        template=None,
    ):
        self._content = content
        self._recipients = recipients
        self._subject = subject
        self._sender = sender
        self._template = template
        self._reply = reply
        self._files = files

    @classmethod
    def create(
        cls,
        content: dict,
        recipients: list,
        sender: str,
        subject: str,
        reply: str = None,
        files: list = None,
        template=None,
    ) -> 'NotificationService':
        return NotificationService(content, recipients, sender, subject, reply, files, template)

    @property
    def message(self) -> dict:
        return self._content

    @property
    def recipients(self) -> list:
        return self._recipients

    def send_email(self):
        if self._reply:
            email_headers = {'Reply-To': self._reply}
        else:
            email_headers = {}

        content = self._content
        message = content['message']
        content.pop('message')
        message = message.format_map(content)

        mail = EmailMultiAlternatives(
            subject=self._subject,
            body=message,
            from_email=self._sender,
            to=self._recipients,
            headers=email_headers
        )

        if self._template:
            mail_template = get_template(self._template)
            mail_template = mail_template.render(self._content)
            mail.attach_alternative(mail_template, 'text/html')

        if self._files:
            for file in self._files:
                if isinstance(file, MIMEImage):
                    mail.attach(file)
                elif isinstance(file, str):
                    mail.attach_file(file)
        mail.send()
