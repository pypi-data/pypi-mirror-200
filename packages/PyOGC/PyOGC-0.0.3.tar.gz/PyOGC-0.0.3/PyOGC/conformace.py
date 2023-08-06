from PyOGC.utils.helpers import get_data

def get_conformance(f="json"):
    """Retrieve the set of OGC API conformance classes that are supported by this service.
    Args:
        f (str, optional): The format of the response. If no value is provided, the accept header is used to determine the format. Accepted values are 'json', 'econ' or 'html'.
            `Available values : json, econ, html`
    Returns:
        dict: The set of OGC API conformance classes supported by this service.
    Raises:
        None
    """

    endpoint = "https://maps.gnosis.earth/ogcapi/conformance"
    data = get_data(endpoint, f)
    return data