"""
custom URL patterns for otreeutils extension.

November 2019
Markus Konrad <markus.konrad@wzb.eu>
"""

from django.conf.urls import url
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from otreeutils.admin_extensions.urls import urlpatterns
from otreeutils.admin_extensions.views import get_hierarchical_data_for_apps


@login_required
def export_data_as_json(request):
    apps = ['iat']

    data = get_hierarchical_data_for_apps(apps)

    return JsonResponse(data, safe=False)  # safe=False is necessary for exporting array structures

urlpatterns.append(url(r"^custom_export/$", export_data_as_json, name='custom_export'))
