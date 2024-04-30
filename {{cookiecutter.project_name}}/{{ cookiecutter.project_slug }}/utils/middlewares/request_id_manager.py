from contextvars import ContextVar


class RequestIdManager:
    def __init__(self):
        self.request_id = ContextVar('request_id', default=None)

    def get(self):
        return self.request_id.get()

    def set(self, request_id):
        self.request_id.set(request_id)

    def reset(self):
        try:
            self.request_id.set(None)
        except AttributeError:
            pass


request_id_manager = RequestIdManager()
