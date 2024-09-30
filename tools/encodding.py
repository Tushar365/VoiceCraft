from PIL import Image
import io
import base64

def encode_image(bytes_data):
    """Encodes image bytes to base64."""
    try:
        # Use BytesIO to handle bytes data directly
        image = Image.open(io.BytesIO(bytes_data)) 
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")  # Or whichever format is appropriate
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    except Exception as e:  # Handle encoding errors
        print(f"Error encoding image: {e}")  # Print for debugging
        return None
