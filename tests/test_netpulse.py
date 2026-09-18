import tempfile
import unittest
from pathlib import Path

from src.netpulse.models import CheckResult, classify_latency
from src.netpulse.report import summarize
from src.netpulse.storage import append_results, load_results


class ClassificationTests(unittest.TestCase):
    def test_classifies_expected_latency_ranges(self) -> None:
        self.assertEqual(classify_latency(40, True), "ONLINE")
        self.assertEqual(classify_latency(150, True), "ATENCAO")
        self.assertEqual(classify_latency(280, True), "CRITICO")
        self.assertEqual(classify_latency(None, False), "OFFLINE")


class StorageAndSummaryTests(unittest.TestCase):
    def test_round_trip_and_summary(self) -> None:
        samples = [
            CheckResult("API", "localhost", 8000, "ONLINE", 40.0, "2026-01-01T10:00:00+00:00"),
            CheckResult("API", "localhost", 8000, "OFFLINE", None, "2026-01-01T10:05:00+00:00"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checks.csv"
            append_results(path, samples)
            loaded = load_results(path)

        self.assertEqual(loaded, samples)
        result = summarize(loaded)[0]
        self.assertEqual(result["availability"], 50.0)
        self.assertEqual(result["average_latency"], 40.0)
        self.assertEqual(result["status"], "OFFLINE")


if __name__ == "__main__":
    unittest.main()
