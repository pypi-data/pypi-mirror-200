import requests
from PyOGC.utils.helpers import get_data
from PyOGC.utils.urls import base_url

def metadata(f="html"):
    """
    Retrieves the OGC API landing page for the service.

    :param format: The format of the response. If no value is provided,
        the accept header is used to determine the format. Accepted values
        are 'json', 'html'.
    :type format: str or None

    :return: A dictionary containing links to the API definition, the conformance statements
        and to the feature collections in the dataset.
    :rtype: dict
    :raises requests.exceptions.RequestException: If there was an error making the request.
    """
    try:
        response = get_data(base_url, f)
        return response
    except requests.exceptions.RequestException as e:
        raise e
