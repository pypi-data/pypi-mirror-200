# MODULES
from pathlib import Path

# UNITTEST
import unittest

# KLARF_READER
from klarf_reader.klarf import Klarf
from klarf_reader.models.klarf_content import (
    DieOrigin,
    DiePitch,
    KlarfContent,
    SampleCenterLocation,
    SamplePlanTest,
    SetupId,
    Summary,
    Wafer,
    SingleKlarfContent,
)

# UTILS
from klarf_reader.utils import klarf_convert


ASSETS_PATH: Path = Path(__file__).parent / "assets"


class TestKlarf(unittest.TestCase):
    def setUp(self) -> None:
        self.path_klarf_single_wafer = ASSETS_PATH / "J052SBN_8196_J052SBN-01.000"
        self.path_klarf_multi_wafers = ASSETS_PATH / "J237DTA_3236.000"

        self.expected_klarf_single_wafer = KlarfContent(
            file_version=1.2,
            file_timestamp="02-23-21 06:17:41",
            inspection_station_id="KLA7",
            result_timestamp="02-23-21 06:10:02",
            lot_id="J052SBN",
            device_id="B601",
            sample_size=200,
            setup_id=SetupId(name="B601_8196", date="02-08-21 14:16:40"),
            step_id="8196",
            orientation_mark_location="DOWN",
            die_pitch=DiePitch(x=4109.939, y=4327.942),
            has_sample_test_plan=True,
            sample_plan_test=SamplePlanTest(x=[], y=[]),
            wafers=[
                Wafer(
                    id="01",
                    slot=2,
                    die_origin=DieOrigin(x=0.0, y=0.0),
                    sample_center_location=SampleCenterLocation(
                        x=11856.855, y=1263.472
                    ),
                    defects=[],
                    summary=Summary(
                        defect_density=89.889358521,
                        number_of_defects=12263,
                        number_of_def_dies=17,
                        number_of_dies=808,
                    ),
                ),
            ],
        )

        self.expected_klarf_multi_wafers = KlarfContent(
            file_version=1.2,
            file_timestamp="10-06-22 18:10:00",
            inspection_station_id="AIT4",
            result_timestamp="10-06-22 13:57:02",
            lot_id="J237DTA",
            device_id="WREO",
            sample_size=200,
            setup_id=SetupId(name="WREO", date="10-06-22 13:57:02"),
            step_id="3236",
            orientation_mark_location="DOWN",
            die_pitch=DiePitch(x=2459.878, y=2659.947),
            has_sample_test_plan=True,
            sample_plan_test=SamplePlanTest(x=[], y=[]),
            wafers=[
                Wafer(
                    id="02",
                    slot=1,
                    die_origin=DieOrigin(x=0.0, y=0.0),
                    sample_center_location=SampleCenterLocation(x=6902.0, y=3568.0),
                    defects=[],
                    summary=Summary(
                        defect_density=0.27869999409,
                        number_of_defects=56,
                        number_of_def_dies=37,
                        number_of_dies=4306,
                    ),
                ),
                Wafer(
                    id="06",
                    slot=5,
                    die_origin=DieOrigin(x=0.0, y=0.0),
                    sample_center_location=SampleCenterLocation(x=6902.0, y=3568.0),
                    defects=[],
                    summary=Summary(
                        defect_density=0.17910000682,
                        number_of_defects=36,
                        number_of_def_dies=22,
                        number_of_dies=4306,
                    ),
                ),
                Wafer(
                    id="01",
                    slot=25,
                    die_origin=DieOrigin(x=0.0, y=0.0),
                    sample_center_location=SampleCenterLocation(x=6902.0, y=3568.0),
                    defects=[],
                    summary=Summary(
                        defect_density=0.47279998660,
                        number_of_defects=95,
                        number_of_def_dies=58,
                        number_of_dies=4306,
                    ),
                ),
            ],
        )

        self.expected_single_klarf_content_wafer_index_1 = SingleKlarfContent(
            file_version=1.2,
            file_timestamp="10-06-22 18:10:00",
            inspection_station_id="AIT4",
            result_timestamp="10-06-22 13:57:02",
            lot_id="J237DTA",
            device_id="WREO",
            sample_size=200,
            setup_id=SetupId(name="WREO", date="10-06-22 13:57:02"),
            step_id="3236",
            orientation_mark_location="DOWN",
            die_pitch=DiePitch(x=2459.878, y=2659.947),
            has_sample_test_plan=True,
            sample_plan_test=SamplePlanTest(x=[], y=[]),
            wafer=Wafer(
                id="02",
                slot=1,
                die_origin=DieOrigin(x=0.0, y=0.0),
                sample_center_location=SampleCenterLocation(x=6902.0, y=3568.0),
                defects=[],
                summary=Summary(
                    defect_density=0.27869999409,
                    number_of_defects=56,
                    number_of_def_dies=37,
                    number_of_dies=4306,
                ),
            ),
        )

    def test_klarf_single_wafer(self) -> None:
        # Given
        expected_klarf_content = self.expected_klarf_single_wafer

        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_single_wafer)

        # Then
        self.assertEqual(content.file_timestamp, expected_klarf_content.file_timestamp)
        self.assertEqual(
            content.result_timestamp, expected_klarf_content.result_timestamp
        )
        self.assertEqual(
            content.inspection_station_id,
            expected_klarf_content.inspection_station_id,
        )
        self.assertEqual(content.lot_id, expected_klarf_content.lot_id)
        self.assertEqual(content.device_id, expected_klarf_content.device_id)
        self.assertEqual(content.sample_size, expected_klarf_content.sample_size)
        self.assertEqual(content.setup_id, expected_klarf_content.setup_id)
        self.assertEqual(content.step_id, expected_klarf_content.step_id)
        self.assertEqual(
            content.orientation_mark_location,
            expected_klarf_content.orientation_mark_location,
        )
        self.assertEqual(content.die_pitch, expected_klarf_content.die_pitch)
        self.assertEqual(
            content.has_sample_test_plan,
            expected_klarf_content.has_sample_test_plan,
        )
        for index, wafer in enumerate(expected_klarf_content.wafers):
            self.assertEqual(content.wafers[index].id, wafer.id)
            self.assertEqual(content.wafers[index].slot, wafer.slot)
            self.assertEqual(content.wafers[index].die_origin, wafer.die_origin)
            self.assertEqual(
                content.wafers[index].sample_center_location,
                wafer.sample_center_location,
            )
            self.assertEqual(
                content.wafers[index].summary.defect_density,
                wafer.summary.defect_density,
            )
            self.assertEqual(
                content.wafers[index].summary.number_of_def_dies,
                wafer.summary.number_of_def_dies,
            )
            self.assertEqual(
                content.wafers[index].summary.number_of_dies,
                wafer.summary.number_of_dies,
            )
            self.assertEqual(
                content.wafers[index].summary.number_of_defects,
                wafer.summary.number_of_defects,
            )

    def test_klarf_multi_wafers(self) -> None:
        # Given
        expected_klarf_content = self.expected_klarf_multi_wafers

        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_multi_wafers)

        # Then
        self.assertEqual(content.file_timestamp, expected_klarf_content.file_timestamp)
        self.assertEqual(
            content.result_timestamp, expected_klarf_content.result_timestamp
        )
        self.assertEqual(
            content.inspection_station_id,
            expected_klarf_content.inspection_station_id,
        )
        self.assertEqual(content.lot_id, expected_klarf_content.lot_id)
        self.assertEqual(content.device_id, expected_klarf_content.device_id)
        self.assertEqual(content.sample_size, expected_klarf_content.sample_size)
        self.assertEqual(content.setup_id, expected_klarf_content.setup_id)
        self.assertEqual(content.step_id, expected_klarf_content.step_id)
        self.assertEqual(
            content.orientation_mark_location,
            expected_klarf_content.orientation_mark_location,
        )
        self.assertEqual(content.die_pitch, expected_klarf_content.die_pitch)
        self.assertEqual(
            content.has_sample_test_plan,
            expected_klarf_content.has_sample_test_plan,
        )
        for index, wafer in enumerate(expected_klarf_content.wafers):
            self.assertEqual(content.wafers[index].id, wafer.id)
            self.assertEqual(content.wafers[index].slot, wafer.slot)
            self.assertEqual(content.wafers[index].die_origin, wafer.die_origin)
            self.assertEqual(
                content.wafers[index].sample_center_location,
                wafer.sample_center_location,
            )
            self.assertEqual(
                content.wafers[index].summary.defect_density,
                wafer.summary.defect_density,
            )
            self.assertEqual(
                content.wafers[index].summary.number_of_def_dies,
                wafer.summary.number_of_def_dies,
            )
            self.assertEqual(
                content.wafers[index].summary.number_of_dies,
                wafer.summary.number_of_dies,
            )
            self.assertEqual(
                content.wafers[index].summary.number_of_defects,
                wafer.summary.number_of_defects,
            )

    def test_convert_single_klarf_content(self) -> None:
        # Given
        expected_single_klarf_content = self.expected_single_klarf_content_wafer_index_1

        # When
        content = Klarf.load_from_file(filepath=self.path_klarf_multi_wafers)
        single_klarf_content = klarf_convert.convert_to_single_klarf_content(
            klarf_content=content, wafer_index=0
        )

        # Then
        self.assertEqual(
            single_klarf_content.file_timestamp,
            expected_single_klarf_content.file_timestamp,
        )
        self.assertEqual(
            single_klarf_content.result_timestamp,
            expected_single_klarf_content.result_timestamp,
        )
        self.assertEqual(
            single_klarf_content.inspection_station_id,
            expected_single_klarf_content.inspection_station_id,
        )
        self.assertEqual(
            single_klarf_content.lot_id, expected_single_klarf_content.lot_id
        )
        self.assertEqual(
            single_klarf_content.device_id, expected_single_klarf_content.device_id
        )
        self.assertEqual(
            single_klarf_content.sample_size, expected_single_klarf_content.sample_size
        )
        self.assertEqual(
            single_klarf_content.setup_id, expected_single_klarf_content.setup_id
        )
        self.assertEqual(
            single_klarf_content.step_id, expected_single_klarf_content.step_id
        )
        self.assertEqual(
            single_klarf_content.orientation_mark_location,
            expected_single_klarf_content.orientation_mark_location,
        )
        self.assertEqual(
            single_klarf_content.die_pitch, expected_single_klarf_content.die_pitch
        )
        self.assertEqual(
            single_klarf_content.has_sample_test_plan,
            expected_single_klarf_content.has_sample_test_plan,
        )

        self.assertEqual(
            single_klarf_content.wafer.id, expected_single_klarf_content.wafer.id
        )
        self.assertEqual(
            single_klarf_content.wafer.slot, expected_single_klarf_content.wafer.slot
        )
        self.assertEqual(
            single_klarf_content.wafer.die_origin,
            expected_single_klarf_content.wafer.die_origin,
        )
        self.assertEqual(
            single_klarf_content.wafer.sample_center_location,
            expected_single_klarf_content.wafer.sample_center_location,
        )
        self.assertEqual(
            single_klarf_content.wafer.summary.defect_density,
            expected_single_klarf_content.wafer.summary.defect_density,
        )
        self.assertEqual(
            single_klarf_content.wafer.summary.number_of_def_dies,
            expected_single_klarf_content.wafer.summary.number_of_def_dies,
        )
        self.assertEqual(
            single_klarf_content.wafer.summary.number_of_dies,
            expected_single_klarf_content.wafer.summary.number_of_dies,
        )
        self.assertEqual(
            single_klarf_content.wafer.summary.number_of_defects,
            expected_single_klarf_content.wafer.summary.number_of_defects,
        )


if __name__ == "__main__":
    unittest.main()
