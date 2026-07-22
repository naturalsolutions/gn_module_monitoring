import pytest

# Comme le conftest des tests d'import du cœur : réécrit les assertions de
# assert_import_errors pour obtenir le diff attendu/obtenu en cas d'échec.
pytest.register_assert_rewrite("geonature.tests.imports.utils")

from geonature.tests.fixtures import *
from geonature.tests.fixtures import _session, app, _app, users

pytest_plugins = [
    "gn_module_monitoring.tests.fixtures.generic",
    "gn_module_monitoring.tests.fixtures.module",
    "gn_module_monitoring.tests.fixtures.site",
    "gn_module_monitoring.tests.fixtures.sites_groups",
    "gn_module_monitoring.tests.fixtures.type_site",
    "gn_module_monitoring.tests.fixtures.visit",
]
