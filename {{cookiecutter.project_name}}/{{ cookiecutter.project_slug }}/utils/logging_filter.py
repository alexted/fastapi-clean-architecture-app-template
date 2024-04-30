import logging

from {{ cookiecutter.project_slug }}.utils.middlewares.request_id_manager import request_id_manager


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_manager.get()
        return True
