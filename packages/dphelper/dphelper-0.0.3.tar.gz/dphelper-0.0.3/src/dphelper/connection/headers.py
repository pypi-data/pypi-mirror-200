"""
Experimental module for generating frequently used headers. 
Changes are likely to occur. 
Do not rely on it too much
"""

from .. import package_consts as __Const


def get_authority_headers(authority: str):
    headers = __Const.HEADERS_AUTHORITY.copy()
    headers["authority"] = authority
    return headers


def get_origin_referer_headers(origin: str, referer: str):
    headers = __Const.HEADERS_ORIGIN_REFERER.copy()
    headers["Origin"] = origin
    headers["Referer"] = referer
    return headers
