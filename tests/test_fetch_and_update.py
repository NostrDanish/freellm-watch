import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fetch_and_update as watcher


class FakeResponse:
    status = 200
    headers = {"Content-Type": "application/json"}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, limit):
        return b'{"data":[{"id":"model-b"},{"id":"model-a"},{"id":"model-a"}]}'


class ProviderObservationTests(unittest.TestCase):
    def test_model_ids_are_deduplicated_and_sorted(self):
        self.assertEqual(
            watcher.extract_model_ids({"data": [{"id": "z"}, {"id": "a"}, {"id": "z"}]}),
            ["a", "z"],
        )

    def test_non_catalog_payload_does_not_invent_models(self):
        self.assertEqual(watcher.extract_model_ids({"models": [{"name": "x"}]}), [])

    @patch("fetch_and_update.urllib.request.urlopen", return_value=FakeResponse())
    def test_observation_does_not_claim_free_entitlement(self, _):
        result = watcher.observe("test", "https://example.invalid")
        self.assertEqual(result["status"], "catalog_observed")
        self.assertEqual(result["model_ids"], ["model-a", "model-b"])
        self.assertEqual(result["entitlement"], "unknown")

    @patch("fetch_and_update.urllib.request.urlopen", side_effect=OSError("offline"))
    def test_fetch_error_is_a_record_not_a_crash(self, _):
        result = watcher.observe("test", "https://example.invalid")
        self.assertEqual(result["status"], "fetch_error")
        self.assertEqual(result["entitlement"], "unknown")

    def test_atomic_json_output_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "snapshot.json"
            watcher.atomic_write_json(path, {"schema_version": 1, "observations": []})
            self.assertEqual(json.loads(path.read_text())["schema_version"], 1)
            self.assertEqual(list(path.parent.glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
