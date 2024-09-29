from app.core.config import settings

async def get_kakao_auth_code() -> str:
    return settings.KAKAO_AUTH_CODE_URI