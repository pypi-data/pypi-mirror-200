from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.keygen_metric import KeygenMetric
from ...types import UNSET, Response, Unset


def _get_kwargs(
    pubkey: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/thorchain/metric/keygen/{pubkey}".format(client.base_url, pubkey=pubkey)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["KeygenMetric"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_keygen_metrics_response_item_data in _response_200:
            componentsschemas_keygen_metrics_response_item = KeygenMetric.from_dict(
                componentsschemas_keygen_metrics_response_item_data
            )

            response_200.append(componentsschemas_keygen_metrics_response_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["KeygenMetric"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pubkey: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Response[List["KeygenMetric"]]:
    """Returns keygen metrics for the provided vault pubkey.

    Args:
        pubkey (str):  Example:
            thorpub1addwnpepq068dr0x7ue973drmq4eqmzhcq3650n7nx5fhgn9gl207luxp6vaklu52tc.
        height (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['KeygenMetric']]
    """

    kwargs = _get_kwargs(
        pubkey=pubkey,
        client=client,
        height=height,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pubkey: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Optional[List["KeygenMetric"]]:
    """Returns keygen metrics for the provided vault pubkey.

    Args:
        pubkey (str):  Example:
            thorpub1addwnpepq068dr0x7ue973drmq4eqmzhcq3650n7nx5fhgn9gl207luxp6vaklu52tc.
        height (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['KeygenMetric']
    """

    return sync_detailed(
        pubkey=pubkey,
        client=client,
        height=height,
    ).parsed


async def asyncio_detailed(
    pubkey: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Response[List["KeygenMetric"]]:
    """Returns keygen metrics for the provided vault pubkey.

    Args:
        pubkey (str):  Example:
            thorpub1addwnpepq068dr0x7ue973drmq4eqmzhcq3650n7nx5fhgn9gl207luxp6vaklu52tc.
        height (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['KeygenMetric']]
    """

    kwargs = _get_kwargs(
        pubkey=pubkey,
        client=client,
        height=height,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pubkey: str,
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
) -> Optional[List["KeygenMetric"]]:
    """Returns keygen metrics for the provided vault pubkey.

    Args:
        pubkey (str):  Example:
            thorpub1addwnpepq068dr0x7ue973drmq4eqmzhcq3650n7nx5fhgn9gl207luxp6vaklu52tc.
        height (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['KeygenMetric']
    """

    return (
        await asyncio_detailed(
            pubkey=pubkey,
            client=client,
            height=height,
        )
    ).parsed
