from pymongo import MongoClient
from settings.config import HOST, DB_NAME

class Mongo_db():
    _client: MongoClient | None = None
    _db = None

    def __init__(self) -> None:
        pass

    def connect_mongo(self) -> None:
        if HOST is None:
            raise ValueError("Host not found.")
        MONGO_URI = f'mongodb://{HOST}'

        self._client = MongoClient(MONGO_URI)

        if DB_NAME is None:
            raise ValueError("DB Name not found.")

        self._db = self._client[DB_NAME]

    def get_client_server(self, server_name: str) -> dict[str, str] | None:
        if self._client is None:
            raise ValueError("Client not connected.")

        if self._db is None:
            raise ValueError("DB not connected.")

        collection = self._db['servers']

        result: dict[str, str] | None = collection.find_one(
            {"name": f"{server_name}"})

        return result

    def add_client_server(self, name: str, language: str, channel: str) -> dict[str, str]:
        if self._client is None:
            raise ValueError("Client not connected.")

        if self._db is None:
            raise ValueError("DB not connected.")

        collection = self._db['servers']

        dict_to_insert: dict[str, str] = {
            "name": f"{name}",
            "language": f"{language}",
            "channel": f"{channel}"
        }

        collection.insert_one(dict_to_insert)

        return dict_to_insert

    def update_client_server(self, name: str, new_data: dict[str, str]) -> None:
        if self._client is None:
            raise ValueError("Client not connected.")

        if self._db is None:
            raise ValueError("DB not connected.")

        collection = self._db['servers']

        update_operation = {
            "$set": new_data
        }

        result = collection.update_one(
            {"name": name},
            update_operation
        )

        if result.modified_count == 0:
            raise ValueError("No server found to update.")

    def mongo_close(self) -> None:
        if self._client is None:
            raise ValueError("Client not connected.")
        self._client.close()
