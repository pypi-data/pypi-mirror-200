from typing import List

from ._sessions import Session


class Queue:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            base_url: str = "https://queue.huddu.io",
    ) -> None:
        """
        This class provides a simple way to interface with the **Queue API** in python
        The endpoint for the queue api is: https://queue.huddu.io
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

    def push(
            self, topic: str, data: str
    ) -> None:
        """
        The put method allows you to add data to your queue.
        if safe is True (which it is by default), it will first check if an entry with the same name exists
        :param topic:
        :param data:
        :return:
        """

        self.session.request(
            "POST", "/push", data={"topic": topic, "data": data}
        )

    def acknowledge(
            self, topic: str, ids: List[str]
    ) -> None:
        """
        The put method allows you to add data to your queue.
        if safe is True (which it is by default), it will first check if an entry with the same name exists
        :param ids:
        :param topic:
        :return:
        """

        self.session.request(
            "POST", "/acknowledge", data={"topic": topic, "ids": ids}
        )

    def pull_all(self, topic: str) -> list:
        has_more = True
        skip = 0
        while has_more:
            events = self.pull(topic, limit=25, skip=skip)
            skip += 25
            if not events:
                has_more = False
            for i in events:
                yield i

    def pull(self, topic: str, limit: int = 25, skip: int = 0) -> list:
        """
        Returns a list of entries
        :param skip:
        :param limit:
        :param topic:
        :return:
        """

        events = self.session.request(
            "GET", "/pull", params={"topic": topic, "skip": skip, "limit": limit}
        )

        res = events["data"]
        formatted_res = []
        for i in res:
            formatted_res.append({**i["data"], **{"_id": i["id"], "_created": i["created"]}})

        return formatted_res
