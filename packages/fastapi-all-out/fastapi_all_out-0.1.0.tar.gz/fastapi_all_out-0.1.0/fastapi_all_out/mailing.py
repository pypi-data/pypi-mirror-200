from datetime import timedelta
from typing import Any
from uuid import UUID

from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr, ValidationError

from fastapi_all_out.settings import MailingConfig
from fastapi_all_out.lazy import get_settings_obj


settings = get_settings_obj()


class MailSender:

    fast_mail: FastMail

    def __init__(self, conf: MailingConfig):
        self.fast_mail = FastMail(conf)

    async def send(self, to: EmailStr | str, data: dict[str, Any], template: str, subject: str):
        email_msg = MessageSchema(
            subject=subject,
            recipients=[to],
            template_body=data,
            subtype=MessageType.html
        )
        await self.fast_mail.send_message(email_msg, template_name=template)

    async def activation_email(
            self,
            to: EmailStr | str,
            username: str,
            uuid: UUID,
            temp_code: str,
            duration: timedelta,
            host: str = settings.HOST,
            template: str = 'activation.html',
            subject: str = 'Account activation'):
        await self.send(to=to, template=template, subject=subject, data={
            'username': username,
            'uuid': uuid,
            'temp_code': temp_code,
            'duration': duration,
            'host': host,
        })

    async def password_reset_email(
            self,
            to: EmailStr | str,
            username: str,
            uuid: UUID,
            temp_code: str,
            duration: timedelta,
            host: str = settings.HOST,
            template: str = 'password_reset.html',
            subject: str = 'Password reset'):
        await self.send(to=to, template=template, subject=subject, data={
            'username': username,
            'uuid': uuid,
            'temp_code': temp_code,
            'duration': duration,
            'host': host,
        })



try:
    mail_sender = MailSender(MailingConfig())
except ValidationError:
    mail_sender = None
