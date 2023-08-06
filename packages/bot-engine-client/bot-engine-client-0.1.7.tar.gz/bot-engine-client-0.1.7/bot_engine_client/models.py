from typing import Dict
from bot_engine_client.enums import BotType, TradeType, TradingPlatform
from datetime import datetime as DateTime


class Bot:
    def __init__(
        self, id: str, description: str, type: BotType, platform: TradingPlatform
    ) -> None:
        self.__id = id
        self.__description = description
        self.__type = type
        self.__platform = platform

    def __repr__(self) -> str:
        return f"{self.id} | {self.description} | {self.type} | {self.platform}"

    @property
    def id(self) -> str:
        return self.__id

    @property
    def description(self) -> str:
        return self.__description

    @property
    def type(self) -> BotType:
        return self.__type

    @property
    def platform(self) -> TradingPlatform:
        return self.__platform

    @classmethod
    def from_json(cls, json: Dict) -> "Bot":
        return cls(
            json.get("id", ""),
            json.get("description", ""),
            json.get("type", ""),
            json.get("platform", ""),
        )


class Execution:
    def __init__(
        self,
        datetime: DateTime,
        trade_type: TradeType,
        symbol: str,
        quantity: float,
        price: float,
        bot_id: str,
    ) -> None:
        self.__datetime = datetime
        self.__trade_type = trade_type
        self.__symbol = symbol
        self.__quantity = quantity
        self.__price = price
        self.__bot_id = bot_id

    def __repr__(self) -> str:
        return f"{self.trade_type} {self.symbol} {self.quantity}@{self.price}"

    @property
    def datetime(self) -> DateTime:
        return self.__datetime

    @property
    def trade_type(self) -> TradeType:
        return self.__trade_type

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def quantity(self) -> float:
        return self.__quantity

    @property
    def price(self) -> float:
        return self.__price

    @property
    def bot_id(self) -> str:
        return self.__bot_id

    @classmethod
    def from_json(cls, json: Dict) -> "Execution":
        """"""
        return cls(
            DateTime.fromtimestamp(json.get("timestamp", 0)),
            TradeType(json.get("tradeType", "")),
            json.get("symbol", ""),
            json.get("quantity", 0.0),
            json.get("price", 0.0),
            json.get("botId", ""),
        )

    @classmethod
    def from_output_string(cls, string: str) -> "Execution":
        """ """
        fields = string.split(",")

        datetime = DateTime.strptime(f"{fields[0]} {fields[1]}", "%Y-%m-%d %H:%M:%S")
        symbol = fields[2]
        trade_type = TradeType(fields[3])
        quantity = float(fields[4])
        price = float(fields[5])
        bot_id = fields[6]
        return cls(
            datetime,
            trade_type,
            symbol,
            quantity,
            price,
            bot_id,
        )

    def to_notification_message(self) -> str:
        datetime_string = self.datetime.strftime("%Y-%m-%d %H:%M:%S")

        notification_message = "\n"
        notification_message += f"{datetime_string}\n"
        notification_message += f"BotID: {self.bot_id}"
        notification_message += (
            f"{self.trade_type.value} {self.symbol} {self.quantity}@{self.price}"
        )
        return notification_message
