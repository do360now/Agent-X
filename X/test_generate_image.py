import unittest
from unittest.mock import patch, MagicMock
import os
from generate_image import generate_image  # Replace with the actual module name


class TestGenerateImage(unittest.TestCase):

    @patch("generate_image.StableDiffusionPipeline.from_pretrained")
    @patch("generate_image.torch.cuda.is_available")
    @patch("generate_image.os.makedirs")
    @unittest.skip("Skipping test_generate_image_success")
    def test_generate_image_success(self, mock_makedirs, mock_cuda_available, mock_pipeline):
        """Test generate_image function when image generation is successful."""
        # Mock CUDA availability
        mock_cuda_available.return_value = True

        # Mock the StableDiffusionPipeline
        mock_pipe = MagicMock()
        mock_pipeline.return_value = mock_pipe

        # Mock the pipeline's `__call__` method to return a mock image
        mock_image = MagicMock()
        mock_pipe.return_value = mock_pipe  # Ensure the pipeline itself can be returned
        mock_pipe.__call__.return_value = MagicMock(images=[mock_image])

        # Mock the save method on the image
        mock_image.save = MagicMock()

        # Call the function
        topic = "Entrepreneurship"
        result = generate_image(topic)

        # Assertions
        self.assertEqual(result, "images/ai_gen_image.png")
        mock_makedirs.assert_called_once_with("images")
        mock_image.save.assert_called_once_with("images/ai_gen_image.png", format="PNG")



    @patch("generate_image.torch.cuda.is_available")
    def test_generate_image_no_cuda(self, mock_cuda_available):
        """Test generate_image function when CUDA is not available."""
        mock_cuda_available.return_value = False

        topic = "Entrepreneurship"

        # Call the function
        result = generate_image(topic)

        # Assertions
        self.assertIsNone(result)

    @patch("generate_image.StableDiffusionPipeline.from_pretrained")
    @patch("generate_image.torch.cuda.is_available")
    def test_generate_image_pipeline_error(self, mock_cuda_available, mock_pipeline):
        """Test generate_image function when an error occurs in loading the pipeline."""
        mock_cuda_available.return_value = True
        mock_pipeline.side_effect = Exception("Pipeline loading error")

        topic = "Entrepreneurship"

        # Call the function
        result = generate_image(topic)

        # Assertions
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
