from richillcapital_http import HttpClient, HttpMethod, HttpRequest, HttpResponse
import json
from typing import Dict, List, Optional
from bot_engine_client.enums import BotType, TradingPlatform

from bot_engine_client.models import Bot


class BotEngineClient(object):
    """ """

    def __init__(self) -> None:
        self.__http_client = HttpClient("http://localhost:3001")

    async def ping_async(self) -> int:
        """ """
        response_bdoy = await self.__send_request(HttpMethod.GET, "/api/v1/ping")
        return response_bdoy.get("time", 0)

    async def get_bots_async(self) -> List[Bot]:
        """ """
        response_body = await self.__send_request(HttpMethod.GET, "/api/v1/bots")
        data = response_body.get("data", [])
        return [Bot.from_json(json) for json in data]
    
    async def create_bot_async(self, id: str, description: str, type: BotType, platform: TradingPlatform) -> None:
        """
        """
        request_body = {
            "id": id,
            "description": description,
            type: BotType,
            platform: TradingPlatform
        }
        response_body = await self.__send_request(HttpMethod.POST, "/api/v1/bots", body=request_body)

    async def delete_bot_async(self, id: str) -> None:
        """
        """
        response_body = await self.__send_request(HttpMethod.DELETE, f"/api/v1/bots/{id}")

    async def get_bot_async(self, id: str) -> Bot:
        """
        """
        response_body = await self.__send_request(HttpMethod.GET, f"/api/v1/bots/{id}")
        return Bot.from_json(response_body.get("bot", {}))


    async def __send_request(
        self,
        method: HttpMethod,
        endpoint: str,
        headers: Optional[Dict] = None,
        body: Optional[Dict] = None,
    ) -> Dict:
        """ """
        request = HttpRequest(method, endpoint, headers, body)
        response = await self.__http_client.send_async((request))
        response.ensure_success_status_code()

        return await self.__parse_response(response)

    async def __parse_response(self, response: HttpResponse) -> Dict:
        """ """
        content = await response.content.read_as_string_async()
        return json.loads(content)
