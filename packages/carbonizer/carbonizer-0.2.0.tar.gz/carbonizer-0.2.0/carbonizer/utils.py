import dataclasses

from carbonizer import options


@dataclasses.dataclass
class RGBA:
    r: int
    g: int
    b: int
    a: int


def validate_body(body) -> dict:
    validated_body = {}
    if not body['code']:
        raise Exception("code is required for creating carbon")

    for option in body:
        if option in options.ignored:
            print(f"Unsupported option: {option} found. Ignoring!")
            continue
        if not (option in options.default):
            continue
            # print(f"Unexpected option: {option} found. Ignoring!")
            # raise Exception(f"Unexpected option: {option}")
        validated_body[option] = body[option]
    return validated_body


def create_url(validated_body) -> str:
    base_url = "https://carbon.now.sh/"
    first = True
    url = ""
    try:
        if validated_body['backgroundColor'].startswith('#') or check_hex(validated_body['backgroundColor'].upper()) == True:
            validated_body['backgroundColor'] = hex2rgb(
                validated_body['backgroundColor'])
    except KeyError:
        pass
    for option in validated_body:
        if first:
            first = False
            url = base_url + \
                f"?{options.query_param[option]}={validated_body[option]}"
        else:
            url = url + \
                f"&{options.query_param[option]}={validated_body[option]}"
    return url


def hex2rgb(h):
    h = h.lstrip('#')
    return ('rgb'+str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4))))


def check_hex(s):
    for ch in s:
        if ((ch < '0' or ch > '9') and (ch < 'A' or ch > 'F')):  
            return False
    return True