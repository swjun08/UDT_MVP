from django.conf import settings
from django.urls import include, path
from django.contrib import admin
import re

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("schools/", include("schools.urls")),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif getattr(settings, "SERVE_STATIC_IN_APP", False):
    from django.urls import re_path
    from django.views.static import serve

    static_prefix = settings.STATIC_URL.strip("/")
    media_prefix = settings.MEDIA_URL.strip("/")

    if static_prefix:
        urlpatterns += [
            re_path(
                rf"^{re.escape(static_prefix)}/(?P<path>.*)$",
                serve,
                {"document_root": settings.STATIC_ROOT},
            )
        ]
    if media_prefix:
        urlpatterns += [
            re_path(
                rf"^{re.escape(media_prefix)}/(?P<path>.*)$",
                serve,
                {"document_root": settings.MEDIA_ROOT},
            )
        ]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
