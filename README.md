# Telegram API Credentials Generator

A simple Python script to automatically retrieve your Telegram API credentials (API ID and API Hash) from my.telegram.org.

## Features

- Automatically installs required dependencies
- Retrieves API ID and Hash with minimal user interaction
- Saves credentials to a JSON file
- Works on Linux systems
- Handles errors gracefully

## Prerequisites

- Linux-based operating system
- Root access (for installing dependencies)
- Python 3.x

## Quick Start

```bash
sudo curl -s https://raw.githubusercontent.com/smaghili/getapikeytelegram/main/api.py | sudo python3
```

The script will automatically:
- Install required dependencies (if needed)
- Guide you through the credential generation process
- Save your API credentials to `telegram_credentials.json`

## Output Format

The script generates a JSON file with the following structure:
```json
{
    "api_id": "your_api_id",
    "api_hash": "your_api_hash",
    "created_at": "2024-11-11 12:34:56"
}
```

## Troubleshooting

- If you get "Too many tries" error, wait for a few hours before trying again
- Make sure you have a stable internet connection
- Verify that you're entering the correct phone number format (international format without '+')
- Ensure you have root privileges when running the script

## Security Notice

- Keep your API credentials secure and never share them
- The script stores credentials locally on your machine
- Use these credentials responsibly according to Telegram's Terms of Service

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Contributing

Feel free to submit issues and pull requests.

## Disclaimer

This tool is not affiliated with Telegram. Use it responsibly and at your own risk.
