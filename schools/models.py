from django.db import models
from django.utils import timezone
from urllib.parse import urlparse

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


class School(models.Model):
    # CSV 컬럼과 1:1 매칭
    name = models.CharField(max_length=200)
    school_type = models.CharField(max_length=50)  # "특성화고" / "마이스터고"
    establishment = models.CharField(max_length=50, blank=True, default="")  # 공립/사립
    education_office = models.CharField(max_length=100, blank=True, default="")
    homepage = models.CharField(max_length=300, blank=True, default="")

    zipcode = models.CharField(max_length=20, blank=True, default="")
    address = models.CharField(max_length=300, blank=True, default="")
    address_detail = models.CharField(max_length=300, blank=True, default="")

    sido = models.CharField(max_length=30)       # 시/도
    sigungu = models.CharField(max_length=30)    # 군/구
    sublocal = models.CharField(max_length=60, blank=True, default="")

    departments = models.TextField(blank=True, default="")
    track_auto = models.CharField(max_length=50, blank=True, default="")

    school_code = models.CharField(max_length=30, unique=True)  # 예: B100000579

    phone_principal = models.CharField(max_length=50, blank=True, default="")
    phone_academic = models.CharField(max_length=50, blank=True, default="")
    phone_admin = models.CharField(max_length=50, blank=True, default="")
    phone_career = models.CharField(max_length=50, blank=True, default="")
    fax = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["sido", "sigungu", "school_type"]),
        ]
        ordering = ["sido", "sigungu", "name"]

    def __str__(self):
        return f"{self.name} ({self.sido} {self.sigungu})"

    @property
    def homepage_url(self):
        """Return a usable absolute URL even if CSV value omits scheme."""
        if not self.homepage:
            return ""
        parsed = urlparse(self.homepage)
        if parsed.scheme:
            return self.homepage
        return f"https://{self.homepage}"


@register_snippet
class Program(models.Model):
    class ProgramType(models.TextChoices):
        ORIENTATION = "ORIENTATION", "입학설명회"
        CAMP = "CAMP", "신입생 캠프"

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="programs")
    program_type = models.CharField(max_length=20, choices=ProgramType.choices)

    title = models.CharField(max_length=200)
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField(null=True, blank=True)

    location_or_link = models.CharField(max_length=300, blank=True, default="")
    description = models.TextField(blank=True, default="")
    is_published = models.BooleanField(default=True)

    panels = [
        FieldPanel("school"),
        FieldPanel("program_type"),
        FieldPanel("title"),
        FieldPanel("start_at"),
        FieldPanel("end_at"),
        FieldPanel("location_or_link"),
        FieldPanel("description"),
        FieldPanel("is_published"),
    ]

    class Meta:
        ordering = ["-start_at"]

    def __str__(self):
        return f"[{self.get_program_type_display()}] {self.title}"
