from ..https import Methods
from .base import Client
from aiohttp import ClientSession
from aiohttp import BasicAuth


class AsyncClient(Client):
    def __init__(self, *args, **kwargs):
        super(AsyncClient, self).__init__(*args, **kwargs)
        self.session = None

    def send_request(self, request):
        url = self.make_url(request)

        async def handle_request(request):
            if not self.session:
                self.session = ClientSession()

            if request.method == Methods.POST:
                response = await self.session.post(
                    url,
                    params=request.params,
                    data=request.data,
                    headers=request.headers,
                    auth=BasicAuth(self.username, self.password)
                )
            elif request.method == Methods.GET:
                response = await self.session.get(
                    url,
                    params=request.params,
                    headers=request.headers,
                    auth=BasicAuth(self.username, self.password)
                )

            content = await response.read()

            if response.status == 500:
                return self.map_server_error(content)

            return request.map(content)

        print("Returning response")
        return handle_request(request)
