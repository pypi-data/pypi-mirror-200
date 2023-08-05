# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import AsyncGenerator

import fastapi

import cbra.core as cbra
from ..models import Client
from ..types import FatalAuthorizationException
from ..types import IAuthorizationServerStorage
from ..types import OIDCProvider
from .cookieclientidentifier import CookieClientIdentifier
from .localclientprovider import ClientProvider
from .localclientprovider import LocalClientProvider


__all__: list[str] = ['LocalOpenIdProvider']


async def get(
    client_id: str | None = CookieClientIdentifier,
    clients: ClientProvider = LocalClientProvider,
    storage: IAuthorizationServerStorage = cbra.instance(
        name='_AuthorizationServerStorage'
    ),
) -> AsyncGenerator[OIDCProvider, None]:
    if client_id is None:
        raise FatalAuthorizationException(
            "The 'client_id' cookie is not provided."
        )
    client = await clients.get(client_id)
    if client is not None:
        provider = client
    else:
        client = await storage.get(Client, client_id)
        if client is None:
            raise FatalAuthorizationException(
                "The client specified by the request does not exist."
            )
        provider = client.get_provider()
    async with provider:
        yield provider


LocalOpenIdProvider: OIDCProvider = fastapi.Depends(get)