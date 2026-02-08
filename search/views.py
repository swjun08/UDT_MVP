from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.template.response import TemplateResponse

from schools.models import School
from wagtail.models import Page

# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

# from wagtail.contrib.search_promotions.models import Query


def search(request):
    search_query = request.GET.get("query", "").strip()
    page = request.GET.get("page", 1)
    search_error = ""
    school_results = School.objects.none()

    # Search
    if search_query:
        school_results = School.objects.filter(
            Q(name__icontains=search_query)
            | Q(sido__icontains=search_query)
            | Q(sigungu__icontains=search_query)
            | Q(departments__icontains=search_query)
            | Q(track_auto__icontains=search_query)
        )[:12]

        try:
            search_results = Page.objects.live().search(search_query)
        except Exception:
            # Database search backend can raise for malformed / empty-like tokens.
            search_results = Page.objects.none()
            search_error = "검색 처리 중 오류가 발생했어요. 검색어를 다시 입력해 주세요."

        # To log this query for use with the "Promoted search results" module:

        # query = Query.get(search_query)
        # query.add_hit()

    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "school_results": school_results,
            "search_results": search_results,
            "search_error": search_error,
        },
    )
