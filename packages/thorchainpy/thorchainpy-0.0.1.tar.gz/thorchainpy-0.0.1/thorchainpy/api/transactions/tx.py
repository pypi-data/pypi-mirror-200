from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.tx_response import TxResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    hash_: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/thorchain/tx/{hash}".format(client.base_url, hash=hash_)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["height"] = height

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[TxResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TxResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[TxResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    hash_: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Response[TxResponse]:
    """Returns the observed transaction for a provided inbound or outbound hash.

    Args:
        hash_ (str):  Example: CF524818D42B63D25BBA0CCC4909F127CAA645C0F9CD07324F2824CC151A64C7.
        height (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TxResponse]
    """

    kwargs = _get_kwargs(
        hash_=hash_,
        client=client,
        height=height,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    hash_: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Optional[TxResponse]:
    """Returns the observed transaction for a provided inbound or outbound hash.

    Args:
        hash_ (str):  Example: CF524818D42B63D25BBA0CCC4909F127CAA645C0F9CD07324F2824CC151A64C7.
        height (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TxResponse
    """

    return sync_detailed(
        hash_=hash_,
        client=client,
        height=height,
    ).parsed


async def asyncio_detailed(
    hash_: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Response[TxResponse]:
    """Returns the observed transaction for a provided inbound or outbound hash.

    Args:
        hash_ (str):  Example: CF524818D42B63D25BBA0CCC4909F127CAA645C0F9CD07324F2824CC151A64C7.
        height (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TxResponse]
    """

    kwargs = _get_kwargs(
        hash_=hash_,
        client=client,
        height=height,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    hash_: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Optional[TxResponse]:
    """Returns the observed transaction for a provided inbound or outbound hash.

    Args:
        hash_ (str):  Example: CF524818D42B63D25BBA0CCC4909F127CAA645C0F9CD07324F2824CC151A64C7.
        height (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TxResponse
    """

    return (
        await asyncio_detailed(
            hash_=hash_,
            client=client,
            height=height,
        )
    ).parsed
