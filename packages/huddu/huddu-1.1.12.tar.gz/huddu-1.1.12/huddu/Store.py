from typing import Union

from ._exceptions import StoreException
from ._sessions import Session


class Store:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            base_url: str = "https://store.huddu.io",
    ) -> None:
        """
        This class provides a simple way to interface with the **Store API** in python
        The endpoint for the store api is: https://store.huddu.io
        :param token:
        :param base_url:
        """

        self.session = Session(
            headers={
                "X-Client-ID": client_id,
                "X-Client-Secret": client_secret,
            },
            base_url=base_url,
        )

    def put(
            self, key: str, value: Union[list, str, dict, int, bool], safe: bool = True
    ) -> None:
        """
        The put method allows you to add data to your store.
        if safe is True (which it is by default), it will first check if an entry with the same name exists
        :param key:
        :param value:
        :param safe:
        :return:
        """
        if safe:
            if self.get(key):
                raise StoreException("Another entry with the same id already exists")

        self.session.request(
            "POST", "/documents", data={"key": key, "value": value}
        )

    def list(self, limit: int = 25, skip: int = 0) -> list:
        """
        Returns a list of entries
        :return:
        """

        documents = self.session.request(
            "GET", "/documents", params={"skip": skip, "limit": limit}
        )

        res = []
        for i in documents["data"]:
            try:
                res.append(eval(i["value"]))
            except Exception:
                res.append(i["value"])
        return res

    def update(self, id: str, data: str) -> None:
        """
        Updates an entry by id

        :param id:
        :param data:
        :return:
        """
        self.put(id, data, safe=False)

    def delete(self, key: str) -> None:
        """
        Delete an entry by id
        :param key:
        :return:
        """
        self.session.request("DELETE", "/documents", data={"key": key})

    def get(self, key: str):
        """
        Retrieve an entry by id
        :param key:
        :return:
        """
        res = self.session.request("GET", "/documents", params={"key": key})

        if not res:
            return None

        try:
            res = eval(res["value"])
        except Exception:
            res = res["value"]
        return res
