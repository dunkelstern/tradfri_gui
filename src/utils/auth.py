import uuid
from pytradfri.api.libcoap_api import APIFactory

from utils.settings import Settings


def get_api(settings: Settings):
    """
    Fetch API-Instance from settings object, automatically requests new session

    :param settings: Settings object, will be modified if no session is active
    """
    if settings.identity is None:
        # create new identity
        if settings.security_key is None:
            # No security key, no api instance
            return None
        settings.identity = uuid.uuid4().hex
        api_factory = APIFactory(host=settings.gateway_ip, psk_id=settings.identity)
        settings.key = api_factory.generate_psk(settings.security_key)
        settings.save()
        return api_factory.request

    api_factory = APIFactory(host=settings.gateway_ip, psk_id=settings.identity, psk=settings.key)
    return api_factory.request
