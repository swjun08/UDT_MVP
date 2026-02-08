from django.test import TestCase
from django.urls import reverse

from .models import School


class SchoolViewsTests(TestCase):
    def setUp(self):
        self.school = self._create_school(
            school_code="T000000001",
            name="테스트고",
            departments="테스트학과",
            track_auto="일반",
        )

    def _create_school(self, **overrides):
        defaults = {
            "name": "기본학교",
            "school_type": "특성화고",
            "establishment": "공립",
            "education_office": "서울시교육청",
            "homepage": "example.com",
            "zipcode": "00000",
            "address": "서울 어딘가",
            "address_detail": "1층",
            "sido": "서울특별시",
            "sigungu": "강남구",
            "sublocal": "",
            "departments": "기본학과",
            "track_auto": "일반",
            "school_code": "T999999999",
            "phone_principal": "02-0000-0000",
            "phone_academic": "",
            "phone_admin": "",
            "phone_career": "",
            "fax": "",
        }
        defaults.update(overrides)
        return School.objects.create(**defaults)

    def test_sigungu_api_returns_json(self):
        response = self.client.get(reverse("schools:sigungu_api"), {"sido": "서울특별시"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sigungus"], ["강남구"])

    def test_school_detail_uses_safe_homepage_url(self):
        response = self.client.get(reverse("schools:detail", args=[self.school.school_code]))
        self.assertContains(response, 'href="https://example.com"')

    def test_school_list_keyword_filter_works(self):
        self._create_school(
            school_code="T000000002",
            name="다른학교",
            departments="디자인학과",
            track_auto="예체능",
        )
        response = self.client.get(reverse("schools:list"), {"q": "테스트"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "테스트고")
        self.assertNotContains(response, "다른학교")

    def test_school_list_pagination_works(self):
        for idx in range(2, 31):
            self._create_school(
                school_code=f"T{idx:09d}",
                name=f"테스트고{idx}",
                departments="테스트학과",
            )

        response = self.client.get(reverse("schools:list"), {"q": "테스트고", "page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(response.context["total_count"], 30)
