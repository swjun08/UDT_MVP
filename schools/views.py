from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import School, Program


def school_list(request):
    q = request.GET.get("q", "").strip()
    sido = request.GET.get("sido", "").strip()
    sigungu = request.GET.get("sigungu", "").strip()
    t = request.GET.get("type", "").strip()  # "", "특성화고", "마이스터고"
    page = request.GET.get("page", 1)

    qs = School.objects.all()

    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(sido__icontains=q)
            | Q(sigungu__icontains=q)
            | Q(departments__icontains=q)
            | Q(track_auto__icontains=q)
        )

    if sido:
        qs = qs.filter(sido=sido)
    if sigungu:
        qs = qs.filter(sigungu=sigungu)
    if t in ("특성화고", "마이스터고"):
        qs = qs.filter(school_type=t)

    total_count = qs.count()
    paginator = Paginator(qs, 24)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 드롭다운 구성용(현재 데이터 기준)
    sidos = School.objects.values_list("sido", flat=True).distinct().order_by("sido")
    sigungus = (
        School.objects.filter(sido=sido).values_list("sigungu", flat=True).distinct().order_by("sigungu")
        if sido else []
    )

    query_params = request.GET.copy()
    query_params.pop("page", None)

    context = {
        "schools": page_obj.object_list,
        "page_obj": page_obj,
        "total_count": total_count,
        "query_string": query_params.urlencode(),
        "sidos": sidos,
        "sigungus": sigungus,
        "selected": {"q": q, "sido": sido, "sigungu": sigungu, "type": t},
    }
    return render(request, "schools/school_list.html", context)


def school_detail(request, school_code):
    school = get_object_or_404(School, school_code=school_code)
    programs = school.programs.filter(is_published=True).order_by("-start_at")

    context = {"school": school, "programs": programs}
    return render(request, "schools/school_detail.html", context)

from django.http import JsonResponse

def sigungu_api(request):
    sido = request.GET.get("sido", "").strip()
    if not sido:
        return JsonResponse({"sigungus": []})
    sigungus = (
        School.objects.filter(sido=sido)
        .values_list("sigungu", flat=True)
        .distinct()
        .order_by("sigungu")
    )
    return JsonResponse({"sigungus": list(sigungus)})
