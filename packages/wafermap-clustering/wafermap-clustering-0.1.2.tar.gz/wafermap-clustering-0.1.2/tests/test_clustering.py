# MODULES
from pathlib import Path
from collections import Counter

# UNITTEST
import unittest

# LIBS
from wafermap_clustering.wafermap_clustering import Clustering

# CONFIGS
from wafermap_clustering.configs.config import Config, ClusteringConfig, KlarfFormat

ASSETS_PATH: Path = Path(__file__).parent / "assets"
ASSETS_OUPUT_PATH: Path = ASSETS_PATH / "clustering" / "output"


def compare_files(file1_path, file2_path):
    with open(file1_path, "r") as file1, open(file2_path, "r") as file2:
        for i, (line1, line2) in enumerate(zip(file1, file2)):
            if line1 != line2:
                return False

    return True


class TestClustering(unittest.TestCase):
    def setUp(self) -> None:
        self.path_klarf_single_wafer = ASSETS_PATH / "J052SBN_8196_J052SBN-01.000"
        self.path_klarf_multi_wafers = ASSETS_PATH / "J237DTA_3236.000"

        self.config = Config(
            platform="windows",
            attribute="DYN_CLUSTER_ID",
            clustering=ClusteringConfig(eps=4, min_samples=3),
        )

    def test_clustering_single_wafer(self):
        # GIVEN
        expected_summary = [
            {
                "result_timestamp": "02-23-21 06:10:02",
                "lot_id": "J052SBN",
                "step_id": "8196",
                "wafer_id": "01",
                "clusters": 3,
                "clustering": {
                    -1: 13,
                    0: 10580,
                    1: 1670,
                },
            }
        ]

        # WHEN
        clustering = Clustering(config=self.config)
        results = clustering.apply(self.path_klarf_single_wafer)

        summary = [
            {
                "result_timestamp": res.result_timestamp,
                "lot_id": res.lot_id,
                "step_id": res.step_id,
                "wafer_id": res.wafer_id,
                "clusters": res.clusters,
                "clustering": dict(
                    Counter([cluster.bin for cluster in res.clustered_defects])
                ),
            }
            for res in results
        ]

        # THEN
        self.assertEqual(summary, expected_summary)

    def test_clustering_mutli_wafers(self):
        # GIVEN
        expected_summary = [
            {
                "result_timestamp": "10-06-22 13:57:02",
                "lot_id": "J237DTA",
                "step_id": "3236",
                "wafer_id": "02",
                "clusters": 6,
                "clustering": {-1: 12, 0: 22, 1: 3, 2: 4, 3: 11, 4: 4},
            },
            {
                "result_timestamp": "10-06-22 13:57:02",
                "lot_id": "J237DTA",
                "step_id": "3236",
                "wafer_id": "06",
                "clusters": 3,
                "clustering": {
                    -1: 9,
                    0: 14,
                    1: 13,
                },
            },
            {
                "result_timestamp": "10-06-22 13:57:02",
                "lot_id": "J237DTA",
                "step_id": "3236",
                "wafer_id": "01",
                "clusters": 8,
                "clustering": {
                    -1: 34,
                    0: 17,
                    1: 7,
                    2: 7,
                    3: 3,
                    4: 19,
                    5: 5,
                    6: 3,
                },
            },
        ]

        # WHEN
        clustering = Clustering(config=self.config)
        results = clustering.apply(self.path_klarf_multi_wafers)

        summary = [
            {
                "result_timestamp": res.result_timestamp,
                "lot_id": res.lot_id,
                "step_id": res.step_id,
                "wafer_id": res.wafer_id,
                "clusters": res.clusters,
                "clustering": dict(
                    Counter(sorted([cluster.bin for cluster in res.clustered_defects]))
                ),
            }
            for res in results
        ]

        # THEN
        self.assertEqual(summary, expected_summary)

    def test_clustering_single_wafer_with_baby_klarf_returned(self):
        # GIVEN
        output_path = ASSETS_OUPUT_PATH / "J237DTA_3236_clustered.000"
        saved_klarf_path = ASSETS_PATH / "saved" / "J237DTA_3236_baby_clustered.000"

        # WHEN
        clustering = Clustering(config=self.config)
        clustering.apply(
            klarf_path=self.path_klarf_multi_wafers,
            output_path=output_path,
            klarf_format=KlarfFormat.BABY.value,
        )

        # THEN
        self.assertEqual(
            compare_files(saved_klarf_path, output_path),
            True,
        )

    def test_clustering_single_wafer_with_full_klarf_returned(self):
        # GIVEN
        output_path = ASSETS_OUPUT_PATH / "J237DTA_3236_clustered.000"
        saved_klarf_path = ASSETS_PATH / "saved" / "J237DTA_3236_full_clustered.000"

        # WHEN
        clustering = Clustering(config=self.config)
        clustering.apply(
            klarf_path=self.path_klarf_multi_wafers,
            output_path=output_path,
            klarf_format=KlarfFormat.FULL.value,
        )

        # THEN
        self.assertEqual(
            compare_files(saved_klarf_path, output_path),
            True,
        )
