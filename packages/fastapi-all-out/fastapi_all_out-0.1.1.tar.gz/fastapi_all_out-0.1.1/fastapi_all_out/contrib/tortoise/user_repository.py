from fastapi_all_out.lazy import get_user_model, get_user_service
from .repository import TortoiseRepository

UserService = get_user_service()


class TortoiseUserRepository(TortoiseRepository):
    model = get_user_model()

    create_handlers = {
        '': UserService.create_user
    }
