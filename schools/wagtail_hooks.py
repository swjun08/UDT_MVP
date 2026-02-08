from wagtail import hooks
from .admin_viewsets import program_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return program_viewset