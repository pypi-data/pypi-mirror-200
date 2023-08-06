from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.quote_swap_response import QuoteSwapResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
    from_asset: Union[Unset, None, str] = UNSET,
    to_asset: Union[Unset, None, str] = UNSET,
    amount: Union[Unset, None, int] = UNSET,
    destination: Union[Unset, None, str] = UNSET,
    from_address: Union[Unset, None, str] = UNSET,
    tolerance_bps: Union[Unset, None, int] = UNSET,
    affiliate_bps: Union[Unset, None, int] = UNSET,
    affiliate: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/thorchain/quote/swap".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["height"] = height

    params["from_asset"] = from_asset

    params["to_asset"] = to_asset

    params["amount"] = amount

    params["destination"] = destination

    params["from_address"] = from_address

    params["tolerance_bps"] = tolerance_bps

    params["affiliate_bps"] = affiliate_bps

    params["affiliate"] = affiliate

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[QuoteSwapResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QuoteSwapResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[QuoteSwapResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
    from_asset: Union[Unset, None, str] = UNSET,
    to_asset: Union[Unset, None, str] = UNSET,
    amount: Union[Unset, None, int] = UNSET,
    destination: Union[Unset, None, str] = UNSET,
    from_address: Union[Unset, None, str] = UNSET,
    tolerance_bps: Union[Unset, None, int] = UNSET,
    affiliate_bps: Union[Unset, None, int] = UNSET,
    affiliate: Union[Unset, None, str] = UNSET,
) -> Response[QuoteSwapResponse]:
    """Provide a quote estimate for the provided swap.

    Args:
        height (Union[Unset, None, int]):
        from_asset (Union[Unset, None, str]):  Example: BTC.BTC.
        to_asset (Union[Unset, None, str]):  Example: ETH.ETH.
        amount (Union[Unset, None, int]):  Example: 1000000.
        destination (Union[Unset, None, str]):  Example:
            0x1c7b17362c84287bd1184447e6dfeaf920c31bbe.
        from_address (Union[Unset, None, str]):  Example:
            thor1zupk5lmc84r2dh738a9g3zscavannjy3nzplwt.
        tolerance_bps (Union[Unset, None, int]):  Example: 100.
        affiliate_bps (Union[Unset, None, int]):  Example: 100.
        affiliate (Union[Unset, None, str]):  Example: t.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QuoteSwapResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        height=height,
        from_asset=from_asset,
        to_asset=to_asset,
        amount=amount,
        destination=destination,
        from_address=from_address,
        tolerance_bps=tolerance_bps,
        affiliate_bps=affiliate_bps,
        affiliate=affiliate,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
    from_asset: Union[Unset, None, str] = UNSET,
    to_asset: Union[Unset, None, str] = UNSET,
    amount: Union[Unset, None, int] = UNSET,
    destination: Union[Unset, None, str] = UNSET,
    from_address: Union[Unset, None, str] = UNSET,
    tolerance_bps: Union[Unset, None, int] = UNSET,
    affiliate_bps: Union[Unset, None, int] = UNSET,
    affiliate: Union[Unset, None, str] = UNSET,
) -> Optional[QuoteSwapResponse]:
    """Provide a quote estimate for the provided swap.

    Args:
        height (Union[Unset, None, int]):
        from_asset (Union[Unset, None, str]):  Example: BTC.BTC.
        to_asset (Union[Unset, None, str]):  Example: ETH.ETH.
        amount (Union[Unset, None, int]):  Example: 1000000.
        destination (Union[Unset, None, str]):  Example:
            0x1c7b17362c84287bd1184447e6dfeaf920c31bbe.
        from_address (Union[Unset, None, str]):  Example:
            thor1zupk5lmc84r2dh738a9g3zscavannjy3nzplwt.
        tolerance_bps (Union[Unset, None, int]):  Example: 100.
        affiliate_bps (Union[Unset, None, int]):  Example: 100.
        affiliate (Union[Unset, None, str]):  Example: t.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QuoteSwapResponse
    """

    return sync_detailed(
        client=client,
        height=height,
        from_asset=from_asset,
        to_asset=to_asset,
        amount=amount,
        destination=destination,
        from_address=from_address,
        tolerance_bps=tolerance_bps,
        affiliate_bps=affiliate_bps,
        affiliate=affiliate,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
    from_asset: Union[Unset, None, str] = UNSET,
    to_asset: Union[Unset, None, str] = UNSET,
    amount: Union[Unset, None, int] = UNSET,
    destination: Union[Unset, None, str] = UNSET,
    from_address: Union[Unset, None, str] = UNSET,
    tolerance_bps: Union[Unset, None, int] = UNSET,
    affiliate_bps: Union[Unset, None, int] = UNSET,
    affiliate: Union[Unset, None, str] = UNSET,
) -> Response[QuoteSwapResponse]:
    """Provide a quote estimate for the provided swap.

    Args:
        height (Union[Unset, None, int]):
        from_asset (Union[Unset, None, str]):  Example: BTC.BTC.
        to_asset (Union[Unset, None, str]):  Example: ETH.ETH.
        amount (Union[Unset, None, int]):  Example: 1000000.
        destination (Union[Unset, None, str]):  Example:
            0x1c7b17362c84287bd1184447e6dfeaf920c31bbe.
        from_address (Union[Unset, None, str]):  Example:
            thor1zupk5lmc84r2dh738a9g3zscavannjy3nzplwt.
        tolerance_bps (Union[Unset, None, int]):  Example: 100.
        affiliate_bps (Union[Unset, None, int]):  Example: 100.
        affiliate (Union[Unset, None, str]):  Example: t.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QuoteSwapResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        height=height,
        from_asset=from_asset,
        to_asset=to_asset,
        amount=amount,
        destination=destination,
        from_address=from_address,
        tolerance_bps=tolerance_bps,
        affiliate_bps=affiliate_bps,
        affiliate=affiliate,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    height: Union[Unset, None, int] = UNSET,
    from_asset: Union[Unset, None, str] = UNSET,
    to_asset: Union[Unset, None, str] = UNSET,
    amount: Union[Unset, None, int] = UNSET,
    destination: Union[Unset, None, str] = UNSET,
    from_address: Union[Unset, None, str] = UNSET,
    tolerance_bps: Union[Unset, None, int] = UNSET,
    affiliate_bps: Union[Unset, None, int] = UNSET,
    affiliate: Union[Unset, None, str] = UNSET,
) -> Optional[QuoteSwapResponse]:
    """Provide a quote estimate for the provided swap.

    Args:
        height (Union[Unset, None, int]):
        from_asset (Union[Unset, None, str]):  Example: BTC.BTC.
        to_asset (Union[Unset, None, str]):  Example: ETH.ETH.
        amount (Union[Unset, None, int]):  Example: 1000000.
        destination (Union[Unset, None, str]):  Example:
            0x1c7b17362c84287bd1184447e6dfeaf920c31bbe.
        from_address (Union[Unset, None, str]):  Example:
            thor1zupk5lmc84r2dh738a9g3zscavannjy3nzplwt.
        tolerance_bps (Union[Unset, None, int]):  Example: 100.
        affiliate_bps (Union[Unset, None, int]):  Example: 100.
        affiliate (Union[Unset, None, str]):  Example: t.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QuoteSwapResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            height=height,
            from_asset=from_asset,
            to_asset=to_asset,
            amount=amount,
            destination=destination,
            from_address=from_address,
            tolerance_bps=tolerance_bps,
            affiliate_bps=affiliate_bps,
            affiliate=affiliate,
        )
    ).parsed
