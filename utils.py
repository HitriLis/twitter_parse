import re
from datetime import date
from datetime import datetime, timedelta
from json import JSONEncoder
import pydantic



class JwtDecodeError(Exception):
    pass


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, enum.Enum):
            return o.value
        if isinstance(o, pydantic.BaseModel):
            return o.dict()
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return super().default(o)


def get_name_from_link(link: str) -> str:
    result = re.search(r"^https?:\/\/(?:www\.)?twitter\.com\/(?:#!\/)?@?([^/?#]*)(?:[?#].*)?$", link, re.M)
    return result.group(1) if result else None
