from loguru import logger

from hawa.common.data import CommonData
from test.mock import prepare_test

prepare_test()


def test_common_init():
    rows = [
        {"meta_unit_type": "school", "meta_unit_id": 3707030003, "target_year": 2021},
        # {"meta_unit_type": "district", "meta_unit_id": 370703, "target_year": 2021},
        # {"meta_unit_type": "city", "meta_unit_id": 331100, "target_year": 2021},
        # {"meta_unit_type": "province", "meta_unit_id": 410000, "target_year": 2021},
    ]
    for row in rows:
        logger.info(row)
        # common data without default  test_types and code_word_list
        CommonData(
            **row, test_types=['publicWelfare', 'ZjpublicWelfare'],
            code_word_list={'dimension', 'field'}
        )
