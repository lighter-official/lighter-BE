from datetime import datetime, timezone

import jwt

from backend.core.config.env import env


def generate_access_token(nickname, picture):
    payload = {
        'iss': 'Gloo',
        "iat": datetime.now(tz=timezone.utc),
        'nickname': nickname,
        'picture': picture,
    }
    encoded = jwt.encode(payload, env.JWT_SECRET, algorithm="HS256")
    return encoded

if __name__ == '__main__':
    result = generate_access_token('철수','http://k.kakaocdn.net/dn/1G9kp/btsAot8liOn/8CWudi3uy07rvFNUkk3ER0/img_110x110.jpg')
    print(result)

