import os
from email.message import EmailMessage
from smtplib import SMTP
from typing import List


class MailClient:
    def __init__(self, username, password, smtp_server, smtp_port):
        self.username = username
        self.password = password
        self.server = smtp_server
        self.port = int(smtp_port)

    def build_message(self, content, subject, to, _from=None, subtype='html'):
        msg = EmailMessage()
        msg.set_charset('UTF-8')
        msg['Subject'] = subject
        _from = _from or self.username
        msg['From'] = _from
        msg['to'] = to
        msg.set_content(content, subtype=subtype)
        return msg

    @staticmethod
    def smtp_context_wrapper(func):
        def wrapper(self: 'MailClient', *args, **kwargs):
            with SMTP(self.server, self.port) as smtp_context:
                smtp_context.ehlo()
                smtp_context.starttls()
                smtp_context.login(self.username, self.password)
                func(self, smtp_context, *args, **kwargs)

        return wrapper

    @smtp_context_wrapper
    def send_mail(self, smtp_context: SMTP, to: List[str], subject, body, attachments=None):
        """

        :param smtp_context:
        :param to:
        :param subject:
        :param body:
        :param attachments:  [{"name": "name", "path": "file_path"}]
        :return:
        """

        msg = self.build_message(content=body, subject=subject, to=','.join(to))
        if attachments:
            for attachment in attachments:
                with open(attachment['file_path'], 'rb') as f:
                    content = f.read()
                file_name = attachment.get('name', os.path.basename(attachment['file_path']))
                msg.add_attachment(content, maintype='application', subtype='octet-stream', filename=file_name)
        smtp_context.send_message(msg=msg)
