#!/usr/bin/env python3
"""
Generate placeholder icons for the Weather App in multiple formats.
Requires: Pillow (add to pyproject.toml dependencies or run: uv add pillow)
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_weather_icon():
    """Create a simple weather-themed icon."""
    # Create a 512x512 image with a gradient blue background
    size = 512
    img = Image.new('RGBA', (size, size), (70, 130, 220, 255))  # Sky blue
    draw = ImageDraw.Draw(img)

    # Draw a sun in the top right
    sun_center = (size * 0.7, size * 0.3)
    sun_radius = size * 0.15
    draw.ellipse(
        [sun_center[0] - sun_radius, sun_center[1] - sun_radius,
         sun_center[0] + sun_radius, sun_center[1] + sun_radius],
        fill=(255, 220, 100, 255)
    )

    # Draw a cloud
    cloud_y = size * 0.6
    cloud_centers = [
        (size * 0.35, cloud_y),
        (size * 0.45, cloud_y - size * 0.05),
        (size * 0.55, cloud_y - size * 0.05),
        (size * 0.65, cloud_y),
    ]
    cloud_radius = size * 0.12

    for cx, cy in cloud_centers:
        draw.ellipse(
            [cx - cloud_radius, cy - cloud_radius,
             cx + cloud_radius, cy + cloud_radius],
            fill=(255, 255, 255, 255)
        )

    return img

def save_png(img, path):
    """Save as PNG."""
    img.save(path, 'PNG')
    print(f"Created: {path}")

def save_ico(img, path):
    """Save as Windows ICO with multiple sizes."""
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(path, format='ICO', sizes=sizes)
    print(f"Created: {path}")

def save_icns(img, path):
    """Save as macOS ICNS."""
    try:
        # Try using PIL's ICNS support
        img.save(path, 'ICNS')
        print(f"Created: {path}")
    except Exception as e:
        # Fallback: Create a PNG that can be converted later
        png_path = path.replace('.icns', '_icns_source.png')
        img.save(png_path, 'PNG')
        print(f"Created PNG source: {png_path}")
        print(f"Note: To create {path}, run:")
        print(f"  iconutil -c icns -o {path} <iconset_folder>")
        print(f"  Or use: sips -s format icns {png_path} --out {path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("Generating Weather App icons...")

    # Create the base icon
    icon = create_weather_icon()

    # Save in different formats
    save_png(icon, os.path.join(script_dir, 'icon.png'))
    save_ico(icon, os.path.join(script_dir, 'icon.ico'))
    save_icns(icon, os.path.join(script_dir, 'icon.icns'))

    print("\nIcon generation complete!")

if __name__ == '__main__':
    main()
