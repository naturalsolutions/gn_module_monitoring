import pytest
from geonature.utils.env import db

from gn_module_monitoring.monitoring.models import TMonitoringModules


@pytest.mark.usefixtures("temporary_transaction")
class TestModule:
    def test_module(self, monitoring_module, types_site):
        types = monitoring_module.types_site
        assert types == list(types_site.values())

    def test_remove_categorie_from_module(self, monitoring_module, types_site):
        with db.session.begin_nested():
            monitoring_module.types_site.pop(0)

        mon = TMonitoringModules.query.filter_by(id_module=monitoring_module.id_module).one()

        assert len(mon.types_site) == len(types_site) - 1
