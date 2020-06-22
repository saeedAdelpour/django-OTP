import jwt

class Token:
  _key = "my site is cool"
  _algorithm = "HS256"

  @classmethod
  def get_token(cls, payload):
    token = jwt.encode(payload, cls._key, cls._algorithm).decode("utf-8")
    return token

  @classmethod
  def decode_token(cls, token_header):
    token = token_header[len("berier "):]
    payload = jwt.decode(token, cls._key, cls._algorithm)
    return payload