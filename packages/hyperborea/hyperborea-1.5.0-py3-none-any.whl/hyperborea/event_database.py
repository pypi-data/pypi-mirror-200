import logging
import re

import requests

logger = logging.getLogger(__name__)


def log_event(serial, category, description, **kwargs):
    sn_filtered = re.sub(r"[^\d]", "", serial)
    try:
        sn_int = int(sn_filtered)
    except Exception:
        raise ValueError("Non-numeric serial number")
    data = kwargs.copy()
    data["serialNumber"] = sn_int
    data["category"] = str(category)
    data["description"] = str(description)

    url = "https://api.suprocktech.com/events/create"

    logger.info(f'Submitting event "{description}"')

    try:
        response = requests.post(url, json=data)

        if not response.ok:
            logger.error("Error submitting event: %s", response.text)
    except Exception:
        msg = "Could not submit event!"
        logger.exception(msg)
