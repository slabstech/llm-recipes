from PIL import Image, ImageDraw

def create_square_mask(
    width: int = 1200, 
    height: int = 692, 
    square_size: int = 300, 
    center_x: int = None, 
    center_y: int = None
) -> Image:
    """
    Create a square mask for an image of given size.
    
    Args:
        width (int): Width of the image (default: 1536)
        height (int): Height of the image (default: 1024)
        square_size (int): Size of the square mask (default: 512)
        center_x (int): X-coordinate of the square's center (default: image center)
        center_y (int): Y-coordinate of the square's center (default: image center)
    
    Returns:
        Image: A PIL Image with a white square mask on a transparent background
    """
    # Create a new image with RGBA mode (transparent background)
    mask_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # Create a drawing context
    draw = ImageDraw.Draw(mask_image)
    
    # Determine the center of the square
    if center_x is None:
        center_x = width // 2
    if center_y is None:
        center_y = height // 2
    
    # Calculate the bounding box for the square
    half_size = square_size // 2
    left = center_x - half_size
    top = center_y - half_size
    right = center_x + half_size
    bottom = center_y + half_size
    
    # Ensure the square stays within image bounds
    left = max(0, left)
    top = max(0, top)
    right = min(width, right)
    bottom = min(height, bottom)
    
    # Draw a white square (fully opaque) on the transparent background
    draw.rectangle([left, top, right, bottom], fill=(255, 255, 255, 255))
    
    return mask_image

# Generate and save the mask
if __name__ == "__main__":
    # Create a square mask centered in the image
    mask = create_square_mask(
        width=1536,
        height=1024,
        square_size=512,  # A 512x512 square
        center_x=768,     # Center of 1536
        center_y=512      # Center of 1024
    )
    mask.save("square_mask_tank.png", "PNG")
    print("Square mask image saved as 'square_mask.png'")