import asyncio
import gc 
import datetime
from settings.servers import Server
from settings.lang import Language
from lang import LANG_CODES
from settings.db import Mongo_db
TIME_LIMIT_SERVER = 30
TIME_LIMIT_LANGUAGE = 60

class Cache():
    _instance = None

    def __init__(self):
        self.servers: dict[str, Server] = {}
        self.ordered_servers: list[Server] = []
        self.languages: dict[str, Language] = {}
        self.ordered_languages: list[Language] = []

    def add_server(
        self,
        server_name: str,
        language: str = LANG_CODES[0],
        channel: str = "default"
    ) -> Server:
        mongo = Mongo_db()
        mongo.connect_mongo()
        server_db = mongo.get_client_server(server_name)
        if server_db is None:
            server_db = mongo.add_client_server(server_name, language, channel)
        
        mongo.mongo_close()
        server = Server(**server_db)

        self.servers[server_name] = server
        self.ordered_servers.append(server)
        return server

    def add_language(self, language_code: str) -> Language:
        lang = Language(language_code)
        self.languages[language_code] = lang
        self.ordered_languages.append(lang)
        return lang

    def get_server(self, server_name: str) -> Server | None:
        return self.servers[server_name]

    def get_language(self, language_code: str) -> Language | None:
        return self.languages[language_code]

    def update_server(
        self,
        data: dict[str,str],
        new_data: dict[str,str]
    ) -> Server:

        name = data["name"]

        items = data.items()
        for _, key in items:
            if key in new_data:
                data[key] = new_data[key]

        mongo = Mongo_db()
        mongo.connect_mongo()
        mongo.update_client_server(name, data)
        mongo.mongo_close()

        server = self.get_server(name)
        if server is None:
            raise ValueError("Error, server not found. Server need to exist to update.")

        server.update_info(data)

        return server

    async def _timer_cache_server(self):
        while True:
            flag_end = False
            count = 0
            while not flag_end and len(self.ordered_servers) > 0:
                time_diference = datetime.datetime.now() - self.ordered_servers[0].get_last_use()
                if time_diference > datetime.timedelta(minutes=TIME_LIMIT_SERVER - 5):
                    server_name = self.ordered_servers[0].get_name()
                    del self.ordered_servers[0]
                    del self.servers[server_name]
                    count += 1
                else:
                    flag_end = True

            if count > 0:
                gc.collect()

            minutes = lambda x: x * 60
            await asyncio.sleep(minutes(TIME_LIMIT_SERVER))

    async def _timer_cache_language(self):
        while True:
            flag_end = False
            count = 0
            while not flag_end and len(self.ordered_languages) > 0:
                time_diference = datetime.datetime.now() - self.ordered_languages[0].get_last_use()
                if time_diference > datetime.timedelta(minutes=TIME_LIMIT_SERVER - 5):
                    language_code = self.ordered_languages[0].get_language()
                    del self.ordered_languages[0]
                    del self.languages[language_code]
                    count += 1
                else:
                    flag_end = True

            if count > 0:
                gc.collect()
            minutes = lambda x: x * 60
            await asyncio.sleep(minutes(TIME_LIMIT_LANGUAGE))

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
