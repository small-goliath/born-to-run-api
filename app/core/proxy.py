from pydantic import BaseModel
from app.api.deps import SessionDep
from aiocache import cached, Cache
from app.api.routes.schemas import ModifyUserRequest, SignInRequest, SignUpRequest
from app.models import CrewBase, SignInResult, SignUpResult, UserGlobal, UserPrivacyGlobal
import app.core.crew_service as crew_service
import app.core.join_service as join_service
import app.core.user_service as user_service
import app.core.user_privacies_service as user_privacies_service
import app.core.converter as converter

def cache_key_builder(func, *args):
    key_parts = [func.__name__]

    if args is None:
        return "".join(key_parts)

    for arg in args:  
        if isinstance(arg, BaseModel):  
            # BaseModel을 상속받는 경우, 속성을 사전 형태로 가져와서 정렬  
            arg_dump = arg.model_dump()  
            # 각 키-값 쌍을 "key=value" 형태로 문자열 리스트에 추가  
            key_parts.extend(f"{key}={value}" for key, value in sorted(arg_dump.items()))  
        else:  
            # BaseModel이 아닌 객체에 대해서는 문자열로 변환  
            key_parts.append(str(arg))  

    # 최종 키는 프로세스된 모든 부분을 '_'로 결합  
    return "".join(key_parts)
# })

def cache_decorator(ttl=60*60):
    return cached(ttl=ttl, cache=Cache.MEMORY, key_builder=cache_key_builder)

def clear_cache_decorator(func):
    async def wrapper(*args, **kwargs):
        await clear_cache()
        return await func(*args, **kwargs)
    return wrapper

async def clear_cache():
    cache = Cache(Cache.MEMORY)
    await cache.clear()



@cache_decorator()
async def search_crews(session: SessionDep) -> CrewBase:
    return await crew_service.search_crews(session)

@cache_decorator()
async def get_kakao_auth_code() -> str:
    return await join_service.get_kakao_auth_code()

@clear_cache_decorator
async def sign_in(request: SignInRequest) -> SignInResult:
    command = converter.to_signInCommand(request)
    return await join_service.sign_in(command)

@clear_cache_decorator
async def sign_up(session: SessionDep, request: SignUpRequest, my_user_id: int) -> SignUpResult:
    command = converter.to_signUpCommand(request, my_user_id)
    return await join_service.sign_up(session, command)

@cache_decorator()
async def get_user_detail(session: SessionDep, user_id: int) -> UserGlobal:
    return await user_service.search_user_detail(session, user_id)

@clear_cache_decorator
async def modify_user(session: SessionDep, user_id: int, request: ModifyUserRequest) -> str:
    command = converter.to_modifyUserCommand(request, user_id)
    return await user_service.modify_user(session, command)

@clear_cache_decorator
async def modify_user_privacy(session: SessionDep, request: ModifyUserRequest, my_user_id: int):
    command = converter.ModifyUserPrivacyCommand(request, my_user_id)
    return await user_privacies_service.modify_user_privacy(session, command)

@cache_decorator()
async def search_user_privacy(session: SessionDep, my_user_id: int) -> UserPrivacyGlobal:
    return await user_privacies_service.search_user_privacy(session, my_user_id)