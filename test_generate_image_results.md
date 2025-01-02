============================= test session starts ==============================
platform linux -- Python 3.8.10, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/flynn/git/Agent-X
plugins: anyio-4.5.2
collected 3 items

X/test_generate_image.py ..F

=================================== FAILURES ===================================
________________ TestGenerateImage.test_generate_image_success _________________

self = <test_generate_image.TestGenerateImage testMethod=test_generate_image_success>
mock_makedirs = <MagicMock name='makedirs' id='139869349879872'>
mock_cuda_available = <MagicMock name='is_available' id='139869349895952'>
mock_pipeline = <MagicMock name='from_pretrained' id='139869349908000'>

    @patch("generate_image.StableDiffusionPipeline.from_pretrained")
    @patch("generate_image.torch.cuda.is_available")
    @patch("generate_image.os.makedirs")
    def test_generate_image_success(self, mock_makedirs, mock_cuda_available, mock_pipeline):
        """Test generate_image function when image generation is successful."""
        # Mock CUDA availability
        mock_cuda_available.return_value = True
    
        # Mock the StableDiffusionPipeline
        mock_pipe = MagicMock()
        mock_image = MagicMock()
>       mock_pipe.__call__.return_value.images = [mock_image]  # Ensure proper return value for images
E       AttributeError: 'function' object has no attribute 'return_value'

X/test_generate_image.py:19: AttributeError
=========================== short test summary info ============================
FAILED X/test_generate_image.py::TestGenerateImage::test_generate_image_success
========================= 1 failed, 2 passed in 2.85s ==========================
