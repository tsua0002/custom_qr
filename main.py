#!/usr/bin/env python3
"""
Custom QR Code Generator - Main Entry Point

This script serves as the main entry point for the QR code generator application.
It provides a clean interface for generating QR codes with different designs.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Optional

from qr_generator import (
    QRGenerator,
    GoogleQRGenerator,
    MulticoloredQRGenerator,
    CustomQRGenerator
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('qr_generator.log')
    ]
)
logger = logging.getLogger(__name__)

class QRCodeGenerator:
    """Main class for QR code generation."""
    
    DESIGN_MAPPING = {
        'google': GoogleQRGenerator,
        'multicolored': MulticoloredQRGenerator,
        'custom': CustomQRGenerator
    }
    
    def __init__(self):
        """Initialize the QR code generator."""
        self.output_dir = Path('outputs')
        self.output_dir.mkdir(exist_ok=True)
    
    def load_config(self, config_path: str) -> Dict:
        """Load configuration from a JSON file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dict containing the configuration
            
        Raises:
            FileNotFoundError: If the configuration file doesn't exist
            json.JSONDecodeError: If the configuration file is not valid JSON
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file: {config_path}")
            raise
    
    def create_generator(
        self,
        design: str,
        url: str,
        output_file: str,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        footer: Optional[str] = None
    ) -> QRGenerator:
        """Create a QR code generator instance based on the design.
        
        Args:
            design: Design style for the QR code
            url: URL to encode in the QR code
            output_file: Path to save the generated QR code
            title: Title text for the QR code
            subtitle: Subtitle text for the QR code
            footer: Footer text for the QR code
            
        Returns:
            An instance of the appropriate QRGenerator subclass
            
        Raises:
            ValueError: If the design is not supported
        """
        if design not in self.DESIGN_MAPPING:
            raise ValueError(f"Unsupported design: {design}. Supported designs: {', '.join(self.DESIGN_MAPPING.keys())}")
        
        generator_class = self.DESIGN_MAPPING[design]
        return generator_class(
            url=url,
            output_file=output_file,
            title=title or "",
            subtitle=subtitle or "",
            footer=footer or ""
        )
    
    def generate_qr_code(
        self,
        url: str,
        design: str = 'custom',
        output_file: Optional[str] = None,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        footer: Optional[str] = None,
        config_file: Optional[str] = None
    ) -> str:
        """Generate a QR code with the specified parameters.
        
        Args:
            url: URL to encode in the QR code
            design: Design style for the QR code
            output_file: Path to save the generated QR code
            title: Title text for the QR code
            subtitle: Subtitle text for the QR code
            footer: Footer text for the QR code
            config_file: Path to a configuration file
            
        Returns:
            Path to the generated QR code
            
        Raises:
            ValueError: If the URL is empty or the design is not supported
            FileNotFoundError: If the configuration file doesn't exist
            json.JSONDecodeError: If the configuration file is not valid JSON
        """
        # Validate URL
        if not url:
            raise ValueError("URL cannot be empty")
        
        # Load configuration if provided
        if config_file:
            config = self.load_config(config_file)
            # Override parameters with config values if not provided
            url = config.get('url', url)
            design = config.get('design', design)
            output_file = config.get('output', output_file)
            title = config.get('title', title)
            subtitle = config.get('subtitle', subtitle)
            footer = config.get('footer', footer)
        
        # Set default output file if not provided
        if not output_file:
            output_file = str(self.output_dir / f"{design}_qr.png")
        else:
            # Ensure output file is in the outputs directory
            output_file = str(self.output_dir / Path(output_file).name)
        
        # Create generator and generate QR code
        try:
            generator = self.create_generator(
                design=design,
                url=url,
                output_file=output_file,
                title=title,
                subtitle=subtitle,
                footer=footer
            )
            output_path = generator.generate()
            logger.info(f"QR code generated successfully: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating QR code: {str(e)}")
            raise

def main():
    """Main entry point for the QR code generator."""
    parser = argparse.ArgumentParser(
        description="Generate custom QR codes with different designs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL to encode in the QR code"
    )
    parser.add_argument(
        "--design",
        choices=["google", "multicolored", "custom"],
        default="custom",
        help="Design style for the QR code"
    )
    parser.add_argument(
        "--output",
        help="Output filename (will be saved in the outputs directory)"
    )
    parser.add_argument(
        "--title",
        help="Title text for the QR code"
    )
    parser.add_argument(
        "--subtitle",
        help="Subtitle text for the QR code"
    )
    parser.add_argument(
        "--footer",
        help="Footer text for the QR code"
    )
    parser.add_argument(
        "--config",
        help="Path to a configuration file"
    )
    
    args = parser.parse_args()
    
    try:
        generator = QRCodeGenerator()
        output_path = generator.generate_qr_code(
            url=args.url,
            design=args.design,
            output_file=args.output,
            title=args.title,
            subtitle=args.subtitle,
            footer=args.footer,
            config_file=args.config
        )
        print(f"QR code saved to: {output_path}")
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 