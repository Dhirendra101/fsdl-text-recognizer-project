"""Tests for LinePredictor class."""
import os
from pathlib import Path
import unittest

import editdistance
import numpy as np

import text_recognizer.util as util
from text_recognizer.line_predictor import LinePredictor

# Hide lines below until Lab 4
from text_recognizer.datasets import IamLinesDataset

# Hide lines above until Lab 4

SUPPORT_DIRNAME = Path(__file__).parents[0].resolve() / "support"

os.environ["CUDA_VISIBLE_DEVICES"] = ""


class TestEmnistLinePredictor(unittest.TestCase):
    """Test LinePredictor class on the EmnistLines dataset."""

    def test_filename(self):
        """Test that LinePredictor correctly predicts on single images, for several test images."""
        predictor = LinePredictor()

        for filename in (SUPPORT_DIRNAME / "emnist_lines").glob("*.png"):
            pred, conf = predictor.predict(str(filename))
            true = str(filename.stem)
            edit_distance = editdistance.eval(pred, true) / len(pred)
            print(f'Pred: "{pred}" | Confidence: {conf} | True: {true} | Edit distance: {edit_distance}')
            self.assertLess(edit_distance, 0.2)


class TestEmnistLinePredictorVariableImageWidth(unittest.TestCase):
    """Test LinePredictor class on the EmnistLines dataset, with variable images."""

    def test_filename(self):
        """Test that LinePredictor correctly predicts on single images, for several test images."""
        predictor = LinePredictor()
        for filename in SUPPORT_DIRNAME.glob("*.png"):
            image = util.read_image(str(filename), grayscale=True)
            print("Saved image shape:", image.shape)
            image = image[:, : -np.random.randint(1, 150)]  # pylint: disable=invalid-unary-operand-type
            print("Randomly cropped image shape:", image.shape)
            pred, conf = predictor.predict(image)
            true = str(filename.stem)
            edit_distance = editdistance.eval(pred, true) / len(pred)
            print(f'Pred: "{pred}" | Confidence: {conf} | True: {true} | Edit distance: {edit_distance}')
            self.assertLess(edit_distance, 0.2)


# Hide lines below until Lab 4
class TestIamLinePredictor(unittest.TestCase):
    """Test LinePredictor class on the IamLines dataset, with variable images."""

    def test_filename(self):  # pylint: disable=R0201
        """Test that LinePredictor correctly predicts on single images, for several test images."""
        predictor = LinePredictor(IamLinesDataset)

        for filename in (SUPPORT_DIRNAME / "iam_lines").glob("*.png"):
            pred, conf = predictor.predict(str(filename))
            true = filename.stem
            if pred:
                edit_distance = editdistance.eval(pred, true) / len(pred)
            else:
                edit_distance = 0
            print(f'Pred: "{pred}" | Confidence: {conf} | True: {true} | Edit distance: {edit_distance}')
            # self.assertLess(edit_distance, 0.2)


# Hide lines above until Lab 4
