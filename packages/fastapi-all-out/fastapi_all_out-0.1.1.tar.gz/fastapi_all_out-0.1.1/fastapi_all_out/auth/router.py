from uuid import uuid4, UUID

from fastapi import Request, BackgroundTasks, Depends, Body, Query

from fastapi_all_out.enums import TempCodeTriggers
from fastapi_all_out.lazy import get_user_repository, get_user_service, get_schema, get_codes, get_auth_backend
from fastapi_all_out.routers import CRUDRouter
from fastapi_all_out.routers.exceptions import ObjectErrors, ItemNotFound
from fastapi_all_out.schemas import UserRead, UserMeRead, UserEdit, UserMeEdit, UserCreate, UserRegistration


auth_backend = get_auth_backend()
UserRepository = get_user_repository()
UserService = get_user_service()
Codes = get_codes()
UserRead = get_schema(UserRead)
UserEdit = get_schema(UserEdit)
UserCreate = get_schema(UserCreate)
UserRegistration = get_schema(UserRegistration)


def create_users_router(
        add_get_me_route: bool = True,
        add_edit_me_route: bool = True,
        add_registration_route: bool = True,
        add_account_activation_route: bool = True,
        complete_auto_routes: bool = True,
        **kwargs
) -> CRUDRouter:

    kwargs.setdefault('read_schema', UserRead)
    kwargs.setdefault('read_many_schema', UserRead)
    kwargs.setdefault('read_list_item_schema', UserRead)
    kwargs.setdefault('create_schema', UserCreate)
    kwargs.setdefault('edit_schema', UserEdit)

    router = CRUDRouter(repo=UserRepository, complete_auto_routes=False, **kwargs)

    if add_get_me_route:
        @router.get('/me', response_model=UserMeRead, responses=Codes.responses(*Codes.auth_errors()))
        async def get_me(user_service: UserService = Depends(auth_backend.get_auth())):
            return UserMeRead.from_orm(user_service.user)

    if add_edit_me_route:
        @router.patch('/me', response_model=UserMeRead, responses=Codes.responses(
            *Codes.auth_errors(),
            router.field_errors_response_example()
        ))
        async def edit_me(
                request: Request,
                background_tasks: BackgroundTasks,
                user_service: UserService = Depends(),
                data: UserMeEdit = Body(...),
        ):
            repository = router.repo(request=request, background_tasks=background_tasks)
            try:
                instance = await repository.edit(user_service.user, data)
            except ObjectErrors as e:
                raise router.field_errors(e)
            return UserMeRead.from_orm(instance)

    if add_registration_route:
        @router.post('/registration', status_code=201, responses=Codes.responses(
            (Codes.activation_email, {'uuid': uuid4()}),
            router.field_errors_response_example()
        ))
        async def registration(
                request: Request,
                background_tasks: BackgroundTasks,
                data: get_schema(UserRegistration) = Body(...)
        ):
            try:
                repository = router.repo(request=request, background_tasks=background_tasks)
                user = await repository.create(data)
            except ObjectErrors as e:
                raise router.field_errors(e)
            user_service = UserService(user)
            await user_service.post_registration(request=request, background_tasks=background_tasks)
            return Codes.activation_email.resp_detail(uuid=user_service.uuid)

    if add_account_activation_route:
        @router.get('/activation', response_model=auth_backend.strategy.authorize_response_model, responses=Codes.responses(
            router.not_found_error_instance(),
            Codes.activation_email_resend,
            Codes.activation_email_code_incorrect,
            Codes.already_active,
        ))
        async def activate_account(
                request: Request,
                background_tasks: BackgroundTasks,
                uuid: UUID = Query(...),
                code: str = Query(..., min_length=6, max_length=6)
        ):
            try:
                repository = router.repo(request=request, background_tasks=background_tasks)
                user = await repository.get_one(uuid, field_name='uuid')
            except ItemNotFound:
                raise router.not_found_error()
            user_service = UserService(user)
            if user_service.is_user_active:
                raise Codes.already_active.err()
            temp_code_error = user_service.check_temp_code_error(code, trigger=TempCodeTriggers.EmailActivation)
            if temp_code_error:
                if temp_code_error == 'expired':
                    user_service.add_send_activation_email_task(background_tasks=background_tasks)
                    raise Codes.activation_email_resend.err(background=background_tasks)
                if temp_code_error == 'incorrect':
                    raise Codes.activation_email_code_incorrect.err()
            await user_service.activate()
            return auth_backend.strategy.authorize(user_service.user)

    if complete_auto_routes:
        router.complete_auto_routes()

    return router
