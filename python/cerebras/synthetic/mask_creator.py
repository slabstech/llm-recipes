from PIL import Image, ImageDraw

def create_circle_mask(width: int = 512, height: int = 512, radius: int = 200) -> Image:
    # Create a new image with RGBA mode (transparent background)
    mask_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # Create a drawing context
    draw = ImageDraw.Draw(mask_image)
    
    # Calculate the center and bounding box for the circle
    center_x, center_y = width // 2, height // 2
    left = center_x - radius
    top = center_y - radius
    right = center_x + radius
    bottom = center_y + radius
    
    # Draw a white circle (255, 255, 255, 255) on the transparent background
    draw.ellipse([left, top, right, bottom], fill=(255, 255, 255, 255))
    
    return mask_image

# Generate and save the mask
if __name__ == "__main__":
    mask = create_circle_mask(512, 512, 200)
    mask.save("circle_mask.png", "PNG")
    print("Mask image saved as 'circle_mask.png'")