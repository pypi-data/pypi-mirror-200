import json

from cgdb.exceptions.EntityNotFound import EntityNotFoundException


class ManagerMix:
    def __init__(self, client):
        self._client = client

    def get(self, url=""):
        raw_content = self._client._session.get(url)

        if raw_content.status_code != 200:
            if raw_content.status_code == 404:
                content = json.loads(raw_content.content)
                raise EntityNotFoundException(content["code"], content["message"] + "\n Entity url: " + url)

        content = json.loads(raw_content.content)

        return content

    def post(self, url="", data=""):
        raw_content = self._client._session.post(url, data)
        print(raw_content.status_code)
        if raw_content.status_code != 200:
            if raw_content.status_code == 404:
                content = json.loads(raw_content.content)
                raise EntityNotFoundException(content["code"], content["message"] + "\n Entity url: " + url)

        return raw_content

    def delete(self, url=""):
        raw_content = self._client._session.delete(url)
        print(raw_content.status_code)
        if raw_content.status_code != 200:
            if raw_content.status_code == 404:
                content = json.loads(raw_content.content)
                raise EntityNotFoundException(content["code"], content["message"] + "\n Entity url: " + url)

        return raw_content
