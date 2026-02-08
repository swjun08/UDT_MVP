from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from schools.models import School


class HomePage(Page):
    hero_title = models.CharField(max_length=80, default="우리동네 직업계고 찾기")
    hero_subtitle = models.CharField(
        max_length=160,
        default="시도/군구로 검색하고, 특성화고·마이스터고를 한 번에 확인하세요."
    )
    notice = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("notice"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        sidos = School.objects.values_list("sido", flat=True).distinct().order_by("sido")
        context["sidos"] = sidos
        context["total_schools"] = School.objects.count()
        context["total_sidos"] = sidos.count()
        context["total_types"] = School.objects.values_list("school_type", flat=True).distinct().count()
        return context