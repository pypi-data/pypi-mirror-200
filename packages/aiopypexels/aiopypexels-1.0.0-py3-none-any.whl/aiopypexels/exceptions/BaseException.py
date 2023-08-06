class AioPexelsBaseException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = f"Error message: {message}. Code: {code}"

    def __str__(self):
        return str(self.message)
