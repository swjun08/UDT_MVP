from wagtail.admin.viewsets.model import ModelViewSet
from .models import Program


class ProgramViewSet(ModelViewSet):
    model = Program
    icon = "date"
    add_to_admin_menu = True
    menu_label = "Programs"
    menu_name = "programs"

    list_display = ("title", "program_type", "school", "start_at", "is_published")
    list_filter = ("program_type", "is_published", "school__sido", "school__school_type")
    search_fields = ("title", "school__name")


program_viewset = ProgramViewSet("programs")  # /admin/programs/ 경로의 베이스