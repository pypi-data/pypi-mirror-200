import random
from string import ascii_uppercase, digits
from typing import Literal, Optional, Union, Callable
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from tortoise import fields, timezone

from fastapi_all_out.lazy import get_user_model_path
from fastapi_all_out.enums import TempCodeTriggers
from . import BaseModel, PermissionMixin, max_len_of


USER_GET_BY_FIELDS = Literal['id', 'email', 'username', 'phone']


class BaseUser(BaseModel):
    id: int
    uuid: UUID = fields.UUIDField(default=uuid4, unique=True)
    username: Optional[str] = fields.CharField(max_length=40, unique=True, null=True)
    email: Optional[str] = fields.CharField(max_length=256, unique=True, null=True)
    AUTH_FIELDS = ('email', 'username')
    IEXACT_FIELDS = ('email', 'username')
    EMAIL_FIELD = 'email'

    password_hash: str = fields.CharField(max_length=200)
    password_change_dt: datetime = fields.DatetimeField()
    password_salt: str = fields.CharField(max_length=50)

    is_superuser: bool = fields.BooleanField(default=False)
    is_active: bool = fields.BooleanField(default=True)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    temp_code: Union["BaseTempCode", fields.BackwardOneToOneRelation["BaseTempCode"]]

    class Meta:
        abstract = True


class UserWithPermissions(BaseUser, PermissionMixin):
    class Meta:
        abstract = True


def get_random_tempcode(code_len: int) -> Callable[[], str]:
    return lambda: ''.join(random.choices(ascii_uppercase + digits, k=code_len))


class BaseTempCode(BaseModel):
    id: int = fields.BigIntField(pk=True)
    user: UserWithPermissions | fields.OneToOneRelation[UserWithPermissions] = fields.OneToOneField(
        get_user_model_path(), related_name='temp_code', on_delete=fields.CASCADE
    )
    code: str = fields.CharField(max_length=6, default=get_random_tempcode(6))
    dt: datetime = fields.DatetimeField(auto_now=True)
    trigger: TempCodeTriggers = fields.CharEnumField(TempCodeTriggers)
    DURATION = timedelta(hours=1)
    DURATION_TEXT = '1 hour'

    async def update(self, trigger: TempCodeTriggers):
        self.code = get_random_tempcode(max_len_of(self.__class__)('code'))()
        self.dt = timezone.now()
        self.trigger = trigger
        await self.save(force_update=True, update_fields=('code', 'dt', 'trigger'))

    @property
    def expired_at(self) -> datetime:
        return self.dt + self.DURATION

    @property
    def expired(self) -> bool:
        return self.expired_at < timezone.now()

    def correct(self, code: str, trigger: TempCodeTriggers) -> bool:
        return code == self.code and trigger == self.trigger

    class Meta:
        abstract = True
