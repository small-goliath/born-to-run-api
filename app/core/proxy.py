from pydantic import BaseModel
from app.api.deps import SessionDep
from aiocache import cached, Cache
from app.models import CrewBase
import app.core.crew_service as crew_service
import app.core.login_service as login_service

def cache_key_builder(func, args=None):
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

@cache_decorator()
async def search_crews(session: SessionDep) -> CrewBase:
    return await crew_service.search_crews(session)

@cache_decorator()
async def get_kakao_auth_code() -> str:
    return await login_service.get_kakao_auth_code()