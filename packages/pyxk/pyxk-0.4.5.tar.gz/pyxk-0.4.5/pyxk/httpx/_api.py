from contextlib import contextmanager
from pyxk.httpx._client import Client


def request(
    method, url, *, params=None, content=None, data=None, files=None, json=None, headers=None, cookies=None, auth=None, proxies=None, timeout=5, follow_redirects=True, verify=True, cert=None, trust_env=True
):
    with Client(
        cookies=cookies, proxies=proxies, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    ) as client:
        return client.request(
            method=method, url=url, content=content, data=data, files=files, json=json, params=params, headers=headers, auth=auth, follow_redirects=follow_redirects
        )


def get(
    url, *, params=None, headers=None, cookies=None, auth=None, proxies=None, follow_redirects=True, cert=None, verify=True, timeout=5, trust_env=True
):
    return request(
        "GET", url, params=params, headers=headers, cookies=cookies, auth=auth, proxies=proxies, follow_redirects=follow_redirects, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    )


def options(
    url, *, params=None, headers=None, cookies=None, auth=None, proxies=None, follow_redirects=True, cert=None, verify=True, timeout=5, trust_env=True
):
    return request(
        "OPTIONS", url, params=params, headers=headers, cookies=cookies, auth=auth, proxies=proxies, follow_redirects=follow_redirects, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    )


def head(
    url, *, params=None, headers=None, cookies=None, auth=None, proxies=None, follow_redirects=False, cert=None, verify=True, timeout=5, trust_env=True
):
    return request(
        "HEAD", url, params=params, headers=headers, cookies=cookies, auth=auth, proxies=proxies, follow_redirects=follow_redirects, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    )


def post(
    url, *, content=None, data=None, files=None, json=None, params=None, headers=None, cookies=None, auth=None, proxies=None, follow_redirects=True, cert=None, verify=True, timeout=5, trust_env=True
):
    return request(
        "POST", url, content=content, data=data, files=files, json=json, params=params, headers=headers, cookies=cookies, auth=auth, proxies=proxies, follow_redirects=follow_redirects, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    )


def put(
    url, *, content=None, data=None, files=None, json=None, params=None, headers=None, cookies=None, auth=None, proxies=None, follow_redirects=True, cert=None, verify=True, timeout=5, trust_env=True
):
    return request(
        "PUT", url, content=content, data=data, files=files, json=json, params=params, headers=headers, cookies=cookies, auth=auth, proxies=proxies, follow_redirects=follow_redirects, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    )


def patch(
    url, *, content=None, data=None, files=None, json=None, params=None, headers=None, cookies=None, auth=None, proxies=None, follow_redirects=True, cert=None, verify=True, timeout=5, trust_env=True
):
    return request(
        "PATCH", url, content=content, data=data, files=files, json=json, params=params, headers=headers, cookies=cookies, auth=auth, proxies=proxies, follow_redirects=follow_redirects, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    )


def delete(
    url, *, params=None, headers=None, cookies=None, auth=None, proxies=None, follow_redirects=True, cert=None, verify=True, timeout=5, trust_env=True
):
    return request(
        "DELETE", url, params=params, headers=headers, cookies=cookies, auth=auth, proxies=proxies, follow_redirects=follow_redirects, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    )


@contextmanager
def stream(
    method, url, *, params=None, content=None, data=None, files=None, json=None, headers=None, cookies=None, auth=None, proxies=None, timeout=5, follow_redirects=True, verify=True, cert=None, trust_env=True
):
    with Client(
        cookies=cookies, proxies=proxies, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    ) as client:
        with client.stream(
            method=method, url=url, content=content, data=data, files=files, json=json, params=params, headers=headers, auth=auth, follow_redirects=follow_redirects
        ) as response:
            yield response


def wget(
    url, method="GET", *, params=None, content=None, data=None, files=None, json=None, headers=None, cookies=None, auth=None, proxies=None, timeout=5, follow_redirects=True, verify=True, cert=None, trust_env=True, output=None, resume=False
):
    with Client(
        cookies=cookies, proxies=proxies, cert=cert, verify=verify, timeout=timeout, trust_env=trust_env
    ) as client:
        return client.wget(
            method=method, url=url, content=content, data=data, files=files, json=json, params=params, headers=headers, auth=auth, follow_redirects=follow_redirects, output=output, resume=resume
        )
