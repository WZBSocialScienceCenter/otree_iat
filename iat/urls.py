"""
This adds URLs for custom admin views (session data and export) from otreeutils (when otreeutils is installed).

March 2021, Markus Konrad <markus.konrad@wzb.eu>
"""

import importlib.util


if importlib.util.find_spec('otreeutils') and importlib.util.find_spec('pandas'):
    from otreeutils.admin_extensions.urls import urlpatterns
