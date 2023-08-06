from .PexelsNotFound import PexelsNotFoundError
from .PexelsUnauthorised import PexelsUnauthorisedError

EXCEPTIONS_ENUM = {404: PexelsNotFoundError, 401: PexelsUnauthorisedError}
