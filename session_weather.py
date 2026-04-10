from typing import Optional, Any
import asyncio
from aiohttp import (ClientSession, ClientTimeout, ClientError,
                     ClientConnectorError, ServerDisconnectedError, InvalidURL,
                     ContentTypeError, TCPConnector)

from config import Config

_session: Optional[ClientSession] = None


async def get_session() -> ClientSession:
    global _session
    if _session is None or _session.closed:
        connector = TCPConnector()
        _session = ClientSession(
            connector=connector,
            timeout=ClientTimeout(total=30)
        )
    return _session


async def close_session() -> None:
    global _session
    if _session and not _session.closed:
        await _session.close()
        _session = None


async def request(
    session: ClientSession,
    url: str,
    setting: Config,
    attempt: int = 1,
) -> dict[str, Any]:
    try:
        async with session.get(url) as resp:
            try:
                data = await resp.json()
            except ContentTypeError:
                data = await resp.text()

            if resp.status >= 400:
                retryable = resp.status in [429, 502, 503, 504]
                if retryable and attempt <= setting.MAX_RETRIES:
                    await asyncio.sleep(setting.RETRY_DELAY * attempt)
                    return await request(session, url, setting, attempt + 1)

                return {
                    "ok": False,
                    "data": data,
                    "status": resp.status,
                    "retryable": retryable
                }

            return {"ok": True, "data": data, "status": resp.status}

    except (ServerDisconnectedError, asyncio.TimeoutError):
        if attempt <= setting.MAX_RETRIES:
            await asyncio.sleep(setting.RETRY_DELAY)
            return await request(session, url, setting, attempt + 1)
        return {"ok": False, "data": None, "status": None, "retryable": False,
                "error": "Сервер не отвечает"}

    except ClientConnectorError as e:
        return {"ok": False, "data": None, "status": None, "retryable": False,
                "error": f"Не удалось подключиться: {e.strerror}"}

    except InvalidURL:
        return {"ok": False, "data": None, "status": None, "retryable": False,
                "error": "Неизвестный город"}

    except ClientError as e:
        return {"ok": False, "data": None, "status": None, "retryable": False,
                "error": f"Неизвестная ошибка: {type(e).__name__}"}