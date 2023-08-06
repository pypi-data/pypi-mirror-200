from loguru import logger

from hawa.paper.health import HealthReportData
from test.mock import prepare_test

prepare_test()


def test_health_init():
    rows = [
        {"meta_unit_type": "school", "meta_unit_id": 3707030003, "target_year": 2021},
        # {"meta_unit_type": "district", "meta_unit_id": 370703, "target_year": 2021},
        # {"meta_unit_type": "city", "meta_unit_id": 331100, "target_year": 2021},
        # {"meta_unit_type": "province", "meta_unit_id": 410000, "target_year": 2021},
    ]
    for row in rows:
        logger.info(row)
        HealthReportData(**row)


def test_cache_year_data():
    # HealthReportData.cache_year_data(year=2022)
    pass
