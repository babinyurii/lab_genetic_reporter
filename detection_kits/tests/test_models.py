from django.test import TestCase
from markers_detection_kits.models import DetectionKit
import datetime


class TestDetectionKitModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.detection_kit = DetectionKit.object.create(
            name='GeneKit',
            date_created=datetime.date(2023, 12, 31),
            created_by=None,
        )


    def test_detectionkit_model(self):
        self.assertEqual(self.detection_kit.name, 'GeneKit')
        self.assertEqual(self.detection_kit.date_created, datetime.date(2023, 12, 31))
        self.assertEqual(self.detection_kit.created_by, None)
