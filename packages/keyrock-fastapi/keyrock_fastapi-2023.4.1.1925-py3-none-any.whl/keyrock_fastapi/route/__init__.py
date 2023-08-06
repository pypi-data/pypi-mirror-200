import logging
logger = logging.getLogger(__name__)

try:
    import fastapi
except:
    fastapi = None
    logger.warning('fastapi not installed')

if fastapi is not None:
    from .standard_response_route import StandardResponseRoute
