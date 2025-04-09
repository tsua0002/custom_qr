#!/usr/bin/env python3
"""
Custom QR Code Generator

A flexible tool for generating QR codes with different design styles.
"""

import argparse
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import qrcode

class QRGenerator:
    """Base class for QR code generators."""
    
    def __init__(self, url, output_file="qr.png", title="", subtitle="", footer=""):
        self.url = url
        self.output_file = output_file
        self.title = title
        self.subtitle = subtitle
        self.footer = footer
        
    def generate(self):
        """Generate the QR code. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement generate()")
    
    def _create_qr_code(self, fill_color=(0, 0, 0), back_color="white"):
        """Create a basic QR code image."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2
        )
        qr.add_data(self.url)
        qr.make(fit=True)
        return qr.make_image(fill_color=fill_color, back_color=back_color)
    
    def _get_font(self, font_path, size):
        """Get a font with fallback options."""
        try:
            return ImageFont.truetype(font_path, size)
        except IOError:
            print(f"Warning: Font {font_path} not found. Using default font.")
            return ImageFont.load_default()


class GoogleQRGenerator(QRGenerator):
    """Google-style QR code generator with colored rectangles."""
    
    def __init__(self, url, output_file="google_qr.png", title="Google", subtitle="Review", footer="TEAM <3"):
        super().__init__(url, output_file, title, subtitle, footer)
        self.img_size = 800
        
    def generate(self):
        # Create base image
        img = Image.new('RGB', (self.img_size, self.img_size), 'white')
        
        # Draw colored rectangles
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, self.img_size, self.img_size//4], fill=(66, 133, 244))  # Top
        d.rectangle([0, 0, self.img_size//4, self.img_size], fill=(234, 67, 53))   # Left
        d.rectangle([self.img_size - self.img_size//4, 0, self.img_size, self.img_size], fill=(251, 188, 5))  # Right
        d.rectangle([0, self.img_size - self.img_size//4, self.img_size, self.img_size], fill=(52, 168, 83))  # Bottom
        
        # Generate QR code
        qr_img = self._create_qr_code(fill_color=(66, 133, 244), back_color="white")
        
        # Scale and overlay QR code
        qr_size = self.img_size//2
        qr_img = qr_img.resize((qr_size, qr_size))
        pos = ((self.img_size - qr_size) // 2, (self.img_size - qr_size) // 2)
        img.paste(qr_img, pos)
        
        # Add text
        draw = ImageDraw.Draw(img)
        
        # Title
        if self.title:
            font_google = self._get_font("fonts/PatchworkStitchlings.ttf", 50)
            draw.text((10, 10), self.title, font=font_google, fill=(255, 255, 255))
        
        # Subtitle
        if self.subtitle:
            font_review = self._get_font("fonts/ORGANICAL.ttf", 50)
            draw.text((20, 110), self.subtitle, font=font_review, fill=(255, 255, 255))
        
        # Footer
        if self.footer:
            font_team = self._get_font("fonts/PatchworkStitchlings.ttf", 40)
            draw.text((self.img_size/4, self.img_size-150), self.footer, font=font_team, fill=(255, 255, 255))
        
        # Save the image
        img.save(self.output_file)
        return self.output_file


class MulticoloredQRGenerator(QRGenerator):
    """Multicolored QR code generator with colored rectangles."""
    
    def __init__(self, url, output_file="multicolor_qr.png", title="", subtitle="", footer=""):
        super().__init__(url, output_file, title, subtitle, footer)
        self.img_size = 500
        
    def generate(self):
        # Create base image
        img = Image.new('RGB', (self.img_size, self.img_size), 'white')
        
        # Draw colored rectangles
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, self.img_size, self.img_size//4], fill=(66, 133, 244))  # Top
        d.rectangle([0, 0, self.img_size//4, self.img_size], fill=(234, 67, 53))   # Left
        d.rectangle([self.img_size - self.img_size//4, 0, self.img_size, self.img_size], fill=(251, 188, 5))  # Right
        d.rectangle([0, self.img_size - self.img_size//4, self.img_size, self.img_size], fill=(52, 168, 83))  # Bottom
        
        # Generate QR code
        qr_img = self._create_qr_code(fill_color=(66, 133, 244), back_color="white")
        
        # Scale and overlay QR code
        qr_size = 250
        qr_img = qr_img.resize((qr_size, qr_size))
        pos = ((self.img_size - qr_size) // 2, (self.img_size - qr_size) // 2)
        img.paste(qr_img, pos)
        
        # Add text
        draw = ImageDraw.Draw(img)
        
        # Title
        if self.title:
            font = self._get_font("fonts/CaviarDreams.ttf", 40)
            draw.text((10, 10), self.title, font=font, fill=(255, 255, 255))
        
        # Subtitle
        if self.subtitle:
            font_review = self._get_font("fonts/ORGANICAL.ttf", 50)
            draw.text((20, 90), self.subtitle, font=font_review, fill=(0, 0, 0))
        
        # Footer
        if self.footer:
            font = self._get_font("fonts/CaviarDreams.ttf", 40)
            draw.text((60, 390), self.footer, font=font, fill=(255, 255, 255))
        
        # Save the image
        img.save(self.output_file)
        return self.output_file


class CustomQRGenerator(QRGenerator):
    """Custom QR code generator with gradient background and rounded corners."""
    
    def __init__(self, url, output_file="custom_qr.png", title="", subtitle="", footer=""):
        super().__init__(url, output_file, title, subtitle, footer)
        
    def generate(self):
        # Generate QR code
        img = self._create_qr_code(fill_color=(0, 200, 230), back_color="white")
        img = img.convert('RGBA')
        
        # Create background
        base_size = img.size[0] + 200
        background_color = (2, 4, 10)  # Dark background
        final_img = Image.new('RGBA', (int(base_size*1.2), int(base_size*1.6)), background_color)
        
        # Add gradient
        gradient = Image.new('RGBA', final_img.size, (0, 0, 0, 0))
        gradient_draw = ImageDraw.Draw(gradient)
        for i in range(final_img.size[1]):
            alpha = int(255 * (1 - i/final_img.size[1]))
            gradient_draw.line([(0, i), (final_img.size[0], i)], 
                              fill=(0, 230, 255, int(alpha * 0.05)))
        
        final_img = Image.alpha_composite(final_img, gradient)
        
        # Create rounded rectangle mask
        qr_size = img.size[0]
        padding = 40
        mask_size = (qr_size + padding, qr_size + padding)
        rounded_mask = Image.new('L', mask_size, 0)
        mask_draw = ImageDraw.Draw(rounded_mask)
        
        # Draw rounded rectangle
        corner_radius = 30
        mask_draw.rounded_rectangle([(0, 0), (mask_size[0], mask_size[1])],
                                  radius=corner_radius, fill=255)
        
        # Create white background
        white_bg = Image.new('RGBA', mask_size, 'white')
        white_bg.putalpha(rounded_mask)
        
        # Calculate positions
        qr_position = ((final_img.size[0] - mask_size[0]) // 2,
                      (final_img.size[1] - mask_size[1]) // 2 + 30)
        
        # Paste white background
        final_img.paste(white_bg, qr_position, rounded_mask)
        
        # Paste QR code
        qr_offset = (padding // 2, padding // 2)
        final_img.paste(img, 
                      (qr_position[0] + qr_offset[0], 
                       qr_position[1] + qr_offset[1]))
        
        # Add text
        draw = ImageDraw.Draw(final_img)
        
        # Title
        if self.title:
            title_font_size = 120
            title_font = self._get_font("fonts/CaviarDreams.ttf", title_font_size)
            title_bbox = draw.textbbox((0, 0), self.title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (final_img.size[0] - title_width) // 2
            draw.text((title_x, 80), self.title, font=title_font, fill=(0, 230, 255))
        
        # Subtitle
        if self.subtitle:
            subtitle_font_size = 45
            subtitle_font = self._get_font("fonts/CaviarDreams.ttf", subtitle_font_size)
            subtitle_bbox = draw.textbbox((0, 0), self.subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (final_img.size[0] - subtitle_width) // 2
            draw.text((subtitle_x, 220), self.subtitle, font=subtitle_font, fill=(255, 255, 255, 220))
        
        # Footer
        if self.footer:
            footer_font_size = 35
            footer_font = self._get_font("fonts/CaviarDreams.ttf", footer_font_size)
            footer_bbox = draw.textbbox((0, 0), self.footer, font=footer_font)
            footer_width = footer_bbox[2] - footer_bbox[0]
            footer_x = (final_img.size[0] - footer_width) // 2
            draw.text((footer_x, final_img.size[1] - 100), self.footer, font=footer_font, fill=(0, 230, 255, 200))
        
        # Apply sharpening
        enhancer = ImageEnhance.Sharpness(final_img)
        final_img = enhancer.enhance(1.3)
        
        # Save the image
        os.makedirs(os.path.dirname(self.output_file) or '.', exist_ok=True)
        final_img.save(self.output_file, 'PNG', quality=95, optimize=False)
        return self.output_file


def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)


def main():
    """Main entry point for the QR code generator."""
    parser = argparse.ArgumentParser(description="Generate custom QR codes")
    parser.add_argument("--link", required=True, help="URL to encode in QR code")
    parser.add_argument("--design", choices=["google", "multicolored", "custom"], default="custom", 
                        help="Design style for the QR code")
    parser.add_argument("--output", default="qr.png", help="Output filename")
    parser.add_argument("--title", help="Title text for the QR code")
    parser.add_argument("--subtitle", help="Subtitle text for the QR code")
    parser.add_argument("--footer", help="Footer text for the QR code")
    parser.add_argument("--config", help="Path to configuration file")
    
    args = parser.parse_args()
    
    # Load configuration if provided
    if args.config:
        config = load_config(args.config)
        # Override command-line arguments with config values
        for key, value in config.items():
            if hasattr(args, key) and getattr(args, key) is None:
                setattr(args, key, value)
    
    # Create appropriate generator based on design
    if args.design == "google":
        generator = GoogleQRGenerator(args.link, args.output, args.title, args.subtitle, args.footer)
    elif args.design == "multicolored":
        generator = MulticoloredQRGenerator(args.link, args.output, args.title, args.subtitle, args.footer)
    else:
        generator = CustomQRGenerator(args.link, args.output, args.title, args.subtitle, args.footer)
    
    try:
        output_file = generator.generate()
        print(f"QR code saved to {output_file}")
    except Exception as e:
        print(f"Error generating QR code: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 