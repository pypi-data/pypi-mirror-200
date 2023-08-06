from random import choices
from string import hexdigits
from typing import TypeVar, Any, Type, Literal
from uuid import UUID

from fastapi import Request, BackgroundTasks
from tortoise import timezone

from fastapi_all_out.auth.user_service import BaseUserService
from fastapi_all_out.schemas import PasswordsPair
from fastapi_all_out.lazy import get_user_model, get_mail_sender
from fastapi_all_out.enums import TempCodeTriggers
from .models import UserWithPermissions, ContentType, BaseTempCode, get_field_param, max_len_of


UNUSED_PASSWORD_PREFIX = '!'
USER_MODEL = TypeVar("USER_MODEL", bound=UserWithPermissions)
UserModel: Type[UserWithPermissions] = get_user_model()
mail_sender = get_mail_sender()


class TortoiseUserService(BaseUserService):

    @classmethod
    async def create_user(
            cls,
            data: PasswordsPair,
            exclude: set[str] = None,
            defaults: dict[str, Any] = None
    ) -> USER_MODEL:
        data_dict = data.dict(include=UserModel._meta.db_fields.difference(exclude))
        if defaults:
            data_dict.update(defaults)
        self = cls(user=UserModel(**data_dict))
        self.set_password(data.password)
        await self.user.save(force_create=True)
        return self.user

    async def post_registration(self, request: Request, background_tasks: BackgroundTasks) -> None:
        self.add_send_activation_email_task(background_tasks)

    @property
    def pk(self) -> int | UUID:
        return self.user.pk

    @property
    def is_user_active(self) -> bool:
        return self.user.is_active

    @property
    def is_superuser(self) -> bool:
        return self.user.is_superuser

    @property
    def uuid(self) -> UUID:
        return self.user.uuid

    def token_expired(self, iat: int) -> bool:
        return self.user.password_change_dt.timestamp() > iat

    def set_password(self, password: str) -> None:
        user = self.user
        user.password_change_dt = timezone.now()
        user.password_salt = ''.join(choices(hexdigits, k=max_len_of(UserModel)('password_salt')))
        if password:
            user.password_hash = self.get_password_hash(password)
        else:
            user.password_hash = UNUSED_PASSWORD_PREFIX + self.get_password_hash(''.join(choices(hexdigits, k=30)))

    def get_fake_password(self, password: str) -> str:
        user = self.user
        return password + str(user.password_change_dt.timestamp()) + user.password_salt

    def verify_password(self, password: str) -> bool:
        if self.user.password_hash.startswith(UNUSED_PASSWORD_PREFIX):
            return False
        return self.pwd_context.verify(self.get_fake_password(password), self.user.password_hash)

    def get_permissions(self) -> tuple[tuple[int, str], ...]:
        return tuple((perm.content_type_id, perm.name) for perm in self.user.all_permissions)

    def has_permissions(self, *permissions: tuple[str, str]) -> bool:
        if not permissions:
            return True
        user_perms = self.get_permissions()
        has = True
        for model, perm_name in permissions:
            content_type_id = ContentType.get_by_name(model).id
            if (content_type_id, perm_name) not in user_perms:
                has = False
                break
        return has

    async def get_or_create_temp_code(self, trigger: TempCodeTriggers) -> tuple[BaseTempCode, bool]:
        await self.user.fetch_related('temp_code')
        temp_code = self.user.temp_code
        created = False
        if temp_code:
            if trigger != temp_code.trigger:
                await temp_code.update(trigger)
                created = True
        else:
            temp_code = await get_field_param(UserModel, 'temp_code', 'related_model') \
                .create(user=self.user, trigger=trigger)
            created = True
        return temp_code, created

    async def update_or_create_temp_code(self, trigger: TempCodeTriggers) -> BaseTempCode:
        temp_code, created = await self.get_or_create_temp_code(trigger)
        if not created:
            await temp_code.update(trigger)
        return temp_code

    async def send_activation_email(self) -> None:
        temp_code = await self.update_or_create_temp_code(trigger=TempCodeTriggers.EmailActivation)
        await mail_sender.activation_email(
            to=self.user.email,
            username=self.user.username,
            uuid=self.user.uuid,
            temp_code=temp_code.code,
            duration=temp_code.DURATION_TEXT,
        )

    async def send_password_reset_email(self) -> None:
        temp_code = await self.update_or_create_temp_code(trigger=TempCodeTriggers.PwdReset)
        await mail_sender.password_reset_email(
            to=self.user.email,
            username=self.user.username,
            uuid=self.user.uuid,
            temp_code=temp_code.code,
            duration=temp_code.DURATION_TEXT,
        )

    def check_temp_code_error(self, code: str, trigger: TempCodeTriggers) -> Literal['expired', 'incorrect'] | None:
        tc = self.user.temp_code
        if tc.expired:
            return 'expired'
        if not tc.correct(code, trigger):
            return 'incorrect'

    async def activate(self) -> None:
        self.user.is_active = True
        await self.user.temp_code.delete()
        await self.user.save(force_update=True)
