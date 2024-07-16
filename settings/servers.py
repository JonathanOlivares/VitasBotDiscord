import datetime

class Server():
    def __init__(self,
        name: str,
        language: str,
        channel: str,
    ) -> None:

        self._last_use = datetime.datetime.now()
        self.name = name
        self.language = language
        self.channel = channel

    def get_last_use(self) -> datetime.datetime:
        return self._last_use

    def get_name(self) -> str:
        self._update_last_use()
        return self.name

    def get_language(self) -> str:
        self._update_last_use()
        return self.language
    
    def get_channel(self) -> str:
        self._update_last_use()
        return self.channel
    
    def get_all_info(self) -> dict[str, str]:
        self._update_last_use()
        return {
            "name": self.name,
            "language": self.language,
            "channel": self.channel
        }
    
    def update_info(self, new_data: dict[str, str]) -> None:
        self._update_last_use()
        items = new_data.items()
        for _, key in items:
            if key in new_data:
                setattr(self, key, new_data[key])

    def _update_last_use(self):
        self._last_use = datetime.datetime.now()