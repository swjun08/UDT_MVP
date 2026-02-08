from django.test import TestCase
from django.urls import reverse

from schools.models import School

class SearchViewTests(TestCase):
    def setUp(self):
        School.objects.create(
            name="검색테스트고",
            school_type="특성화고",
            establishment="공립",
            education_office="서울시교육청",
            homepage="example.com",
            zipcode="00000",
            address="서울 어딘가",
            address_detail="1층",
            sido="서울특별시",
            sigungu="강남구",
            sublocal="",
            departments="테스트학과",
            track_auto="일반",
            school_code="S000000001",
            phone_principal="02-0000-0000",
            phone_academic="",
            phone_admin="",
            phone_career="",
            fax="",
        )

    def test_search_whitespace_query_does_not_crash(self):
        response = self.client.get(reverse("search"), {"query": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "학교 + 페이지 통합 검색")

    def test_search_invalid_page_param_does_not_crash(self):
        response = self.client.get(reverse("search"), {"query": "home", "page": "abc"})
        self.assertEqual(response.status_code, 200)

    def test_search_returns_school_results(self):
        response = self.client.get(reverse("search"), {"query": "검색테스트"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "검색테스트고")
