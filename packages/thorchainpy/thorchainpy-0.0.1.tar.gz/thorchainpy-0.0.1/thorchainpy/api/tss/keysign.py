from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.keysign_response import KeysignResponse
from ...types import Response


def _get_kwargs(
    height: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/thorchain/keysign/{height}".format(client.base_url, height=height)

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
    *,
    client: Client,
) -> Response[KeysignResponse]:
    """Returns keysign information for the provided height - the height being the first block a tx out item
    appears in the signed-but-unobserved outbound queue.

    Args:
        height (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[KeysignResponse]
    """

    kwargs = _get_kwargs(
        height=height,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    height: int,
    *,
    client: Client,
) -> Optional[KeysignResponse]:
    """Returns keysign information for the provided height - the height being the first block a tx out item
    appears in the signed-but-unobserved outbound queue.

    Args:
        height (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        KeysignResponse
    """

    return sync_detailed(
        height=height,
        client=client,
    ).parsed


async def asyncio_detailed(
    height: int,
    *,
    client: Client,
) -> Response[KeysignResponse]:
    """Returns keysign information for the provided height - the height being the first block a tx out item
    appears in the signed-but-unobserved outbound queue.

    Args:
        height (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[KeysignResponse]
    """

    kwargs = _get_kwargs(
        height=height,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    height: int,
    *,
    client: Client,
) -> Optional[KeysignResponse]:
    """Returns keysign information for the provided height - the height being the first block a tx out item
    appears in the signed-but-unobserved outbound queue.

    Args:
        height (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        KeysignResponse
    """

    return (
        await asyncio_detailed(
            height=height,
            client=client,
        )
    ).parsed
