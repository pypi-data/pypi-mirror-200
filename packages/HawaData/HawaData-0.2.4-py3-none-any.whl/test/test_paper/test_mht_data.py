from hawa.paper.mht import MhtData
from test.mock import prepare_test

prepare_test()


def test_mht_init():
    rows = [
        {"meta_unit_type": "school", "meta_unit_id": 4107110001,
         "target_year": 2022, "test_type": "mht"},
    ]
    for row in rows:
        md = MhtData(**row)
        assert len(md.scale_student_score) == 3
        assert len(md.sub_scale_score) == 3
        assert len(md.grade_scale_student_score) == 3
        assert len(md.grade_special_students) == 3

