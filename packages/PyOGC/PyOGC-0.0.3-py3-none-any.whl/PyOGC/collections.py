from typing import Optional
from PyOGC.utils.helpers import get_data_collections
from PyOGC.utils.urls import base_url

def get_collections(datetime: Optional[str] = None, limit: Optional[int] = 10000, f: str = "json") -> dict:
    """
    Retrieve the set of OGC API collections that are supported by this service.

    Args:
        datetime (str, optional): Either a date-time or an interval, open or closed. Date and time expressions adhere to RFC 3339.
            Open intervals are expressed using double-dots. Examples:
                - A date-time: "2018-02-12T23:20:50Z"
                - A closed interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                - Open intervals: "2018-02-12T00:00:00Z/.." or "../2018-03-18T12:31:12Z"
            Only features that have a temporal property that intersects the value of datetime are selected.
            If a feature has multiple temporal properties, it is the decision of the server whether only a single
            temporal property is used to determine the extent or all relevant temporal properties. (default: None)

        limit (int, optional): Limits the number of collections returned in the response document. Minimum = 1. Maximum = 10000.
            (default: 10000)

        f (str, optional): The format of the response. If no value is provided, the accept header is used to determine
            the format. Accepted values are 'json', 'econ' or 'html'. (default: "json")
            `Available values : json, econ, html`

    Returns:
        dict: A dictionary containing information about the collections supported by the service.

    Raises:
        None
    """
    endpoint = f"{base_url}/collections"
    params = {}
    if datetime:
        params["datetime"] = datetime
    if limit:
        params["limit"] = limit
    data = get_data_collections(endpoint, datetime=datetime, limit=limit, response_format=f)
    return data
