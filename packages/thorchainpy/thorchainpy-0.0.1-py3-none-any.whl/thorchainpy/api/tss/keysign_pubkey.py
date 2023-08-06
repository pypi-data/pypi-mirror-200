from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.keysign_response import KeysignResponse
from ...types import Response


def _get_kwargs(
    height: int,
    pubkey: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/thorchain/keysign/{height}/{pubkey}".format(client.base_url, height=height, pubkey=pubkey)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[KeysignResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = KeysignResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[KeysignResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    height: int,
    pubkey: str,
    *,
    client: Client,
) -> Response[KeysignResponse]:
    """Returns keysign information for the provided height and pubkey - the height being the block at which
    a tx out item is scheduled to be signed and moved from the scheduled outbound queue to the outbound
    queue.

    Args:
        height (int):
        pubkey (str):  Example:
            thorpub1addwnpepq068dr0x7ue973drmq4eqmzhcq3650n7nx5fhgn9gl207luxp6vaklu52tc.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[KeysignResponse]
    """

    kwargs = _get_kwargs(
        height=height,
        pubkey=pubkey,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    height: int,
    pubkey: str,
    *,
    client: Client,
) -> Optional[KeysignResponse]:
    """Returns keysign information for the provided height and pubkey - the height being the block at which
    a tx out item is scheduled to be signed and moved from the scheduled outbound queue to the outbound
    queue.

    Args:
        height (int):
        pubkey (str):  Example:
            thorpub1addwnpepq068dr0x7ue973drmq4eqmzhcq3650n7nx5fhgn9gl207luxp6vaklu52tc.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        KeysignResponse
    """

    return sync_detailed(
        height=height,
        pubkey=pubkey,
        client=client,
    ).parsed


async def asyncio_detailed(
    height: int,
    pubkey: str,
    *,
    client: Client,
) -> Response[KeysignResponse]:
    """Returns keysign information for the provided height and pubkey - the height being the block at which
    a tx out item is scheduled to be signed and moved from the scheduled outbound queue to the outbound
    queue.

    Args:
        height (int):
        pubkey (str):  Example:
            thorpub1addwnpepq068dr0x7ue973drmq4eqmzhcq3650n7nx5fhgn9gl207luxp6vaklu52tc.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[KeysignResponse]
    """

    kwargs = _get_kwargs(
        height=height,
        pubkey=pubkey,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    height: int,
    pubkey: str,
    *,
    client: Client,
) -> Optional[KeysignResponse]:
    """Returns keysign information for the provided height and pubkey - the height being the block at which
    a tx out item is scheduled to be signed and moved from the scheduled outbound queue to the outbound
    queue.

    Args:
        height (int):
        pubkey (str):  Example:
            thorpub1addwnpepq068dr0x7ue973drmq4eqmzhcq3650n7nx5fhgn9gl207luxp6vaklu52tc.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        KeysignResponse
    """

    return (
        await asyncio_detailed(
            height=height,
            pubkey=pubkey,
            client=client,
        )
    ).parsed
