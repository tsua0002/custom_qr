# Custom QR Code Generator 🐍

A flexible and customizable QR code generator that allows you to create beautiful QR codes with different design styles.

## Features

- Multiple design styles: Google, Multicolored, and Custom
- Customizable text (title, subtitle, footer)
- Command-line interface for easy use
- Configuration file support
- Fallback font handling
- Proper error handling and logging

## Installation & Setup

### Using pipenv (Recommended)

1. Install pipenv if you haven't already:
```bash
pip install pipenv
```

2. Clone the repository and navigate to it:
```bash
git clone <repository-url>
cd custom_qr
```

3. Install dependencies using pipenv:
```bash
pipenv install
```

4. Activate the virtual environment:
```bash
pipenv shell
```

### Using pip (Alternative)

If you prefer not to use pipenv, you can install dependencies directly:
```bash
pip install -r requirements.txt
```

## Usage

### Important: Always Run Inside pipenv Shell

Make sure you're in the virtual environment before running commands:
```bash
pipenv shell
```

### Basic Usage

Generate a QR code with the default design (custom):

```bash
# Inside pipenv shell
python main.py --url="https://example.com"
```

### Design Examples

1. Google-style QR code:
```bash
# Inside pipenv shell
python main.py --url="https://example.com" \
               --design="google" \
               --title="Google" \
               --subtitle="Review" \
               --footer="TEAM <3"
```

2. Multicolored QR code:
```bash
# Inside pipenv shell
python main.py --url="https://www.linkedin.com/in/thomas-suau-92932889/" \
               --design="multicolored" \
               --title="My LinkedIn" \
               --subtitle="Review" \
               --footer="Thomas"
```

3. Custom QR code with gradient:
```bash
# Inside pipenv shell
python main.py --url="https://example.com" \
               --design="custom" \
               --title="Your Title" \
               --subtitle="Your Subtitle" \
               --footer="scan to visit example.com"
```

### Using Configuration Files

You can also use a JSON configuration file:

```bash
# Inside pipenv shell
python main.py --config="sample_config.json"
```

Example configuration file (`sample_config.json`):
```json
{
    "url": "https://example.com",
    "design": "google",
    "output": "my_google_qr.png",
    "title": "My Company",
    "subtitle": "Visit Us",
    "footer": "TEAM <3"
}
```

### Command Line Arguments

The following arguments are available:

- `--url`: URL to encode in the QR code (required)
- `--design`: Design style for the QR code (choices: "google", "multicolored", "custom", default: "custom")
- `--output`: Output filename (will be saved in the outputs directory)
- `--title`: Title text for the QR code
- `--subtitle`: Subtitle text for the QR code
- `--footer`: Footer text for the QR code
- `--config`: Path to a configuration file

## Project Structure

```
custom_qr/
├── outputs/          # Generated QR codes are saved here
├── fonts/           # Required fonts for text rendering
│   ├── CaviarDreams.ttf
│   ├── ORGANICAL.ttf
│   └── PatchworkStitchlings.ttf
├── main.py          # Main entry point
├── qr_generator.py  # QR code generator classes
├── requirements.txt # Python dependencies for pip
├── Pipfile         # Python dependencies for pipenv
└── sample_config.json
```

## Fonts

The generator uses custom fonts for better aesthetics. If the fonts are not available, it will fall back to the default system font.

Default font paths:
- `fonts/CaviarDreams.ttf`
- `fonts/PatchworkStitchlings.ttf`
- `fonts/ORGANICAL.ttf`

## Logging

The application logs information and errors to both the console and a log file (`qr_generator.log`). This helps with debugging and tracking the generation process.

## Error Handling

The application includes proper error handling for common issues:
- Invalid URLs
- Unsupported designs
- Missing configuration files
- Font loading errors
- File system errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Run

```
pipenv shell
> pipenv install --ignore-pipfile
```

Example : 
```
> python3 custom_qr.py
```

Everything is happening on the python code. 

Check data variable. 

## Info about files

> `custom_qr.py` : One color around the qr, and text message.

> `multicolored_qr.py`: Close to Google graphics around QR code with Text.

 

