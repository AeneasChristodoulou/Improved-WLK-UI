# Improved WLK UI

Enhanced UI and speaker name management for WhisperLiveKit.

## Features

- **Streamlit-based GUI** for easy server configuration and launching
- **Custom speaker name assignment** - map "Speaker 1" → "Alice", "Speaker 2" → "Bob", etc.
- **Speaker names persist** and display in real-time transcription
- **Extended REST API** for managing speaker names programmatically
- **Full WhisperLiveKit compatibility** - uses WhisperLiveKit as a dependency

## Installation

```bash
pip install improved-wlk-ui
```

Or install from source:

```bash
git clone https://github.com/AeneasChristodoulou/Improved-WLK-UI.git
cd Improved-WLK-UI
pip install -e .
```

## Usage

### Launch Streamlit Interface (Recommended)

The easiest way to use Improved WLK UI is through the Streamlit interface:

```bash
streamlit run -m improved_wlk_ui.streamlit_app
```

This provides a user-friendly GUI to:
- Configure all WhisperLiveKit options
- Select models, languages, and features
- Enable/disable speaker diarization
- Start and stop the server
- View server logs in real-time

### Run the Enhanced Server Directly

You can also run the enhanced server directly from the command line:

```bash
# Basic usage with speaker diarization
improved-wlk-server --model large-v3-turbo --diarization

# Custom port and host
improved-wlk-server --model base --port 9000 --host 0.0.0.0

# With translation
improved-wlk-server --model medium --language fr --target-language en
```

All standard WhisperLiveKit command-line options are supported.

### Access the Web Interface

Once the server is running, open your browser and navigate to:

```
http://localhost:8000
```

You'll see the enhanced WhisperLiveKit interface with the speaker name editor button (👤 Speakers) in the top right.

### Managing Speaker Names

1. **Click the "👤 Speakers" button** in the web interface to open the speaker name editor
2. **Add custom names** for each speaker ID (e.g., Speaker 1 → "Alice")
3. **Save** your changes - names will persist for the duration of the server session
4. **View in transcript** - speaker names will appear automatically in the live transcription

## API Endpoints

The enhanced server provides REST API endpoints for managing speaker names:

### Get all speaker names

```bash
curl http://localhost:8000/api/speakers
```

Response:
```json
{
  "speakers": {
    "1": "Alice",
    "2": "Bob"
  }
}
```

### Set a speaker name

```bash
curl -X POST http://localhost:8000/api/speakers \
  -H "Content-Type: application/json" \
  -d '{"speaker_id": 1, "name": "Alice"}'
```

### Delete a speaker name

```bash
curl -X DELETE http://localhost:8000/api/speakers/1
```

### Clear all speaker names

```bash
curl -X DELETE http://localhost:8000/api/speakers
```

## Architecture

Improved WLK UI extends WhisperLiveKit by:

1. **Using WhisperLiveKit as a dependency** rather than forking the entire codebase
2. **Adding speaker name management** via a custom `SpeakerNameManager` class
3. **Injecting custom UI elements** (CSS and JavaScript) into the base WhisperLiveKit interface
4. **Enhancing WebSocket responses** to include `speaker_name` alongside `speaker` ID
5. **Providing a Streamlit GUI** for easy configuration and server management

## Development

To contribute or modify the code:

```bash
git clone https://github.com/AeneasChristodoulou/Improved-WLK-UI.git
cd Improved-WLK-UI
pip install -e ".[dev]"
```

## Credits

This project builds upon [WhisperLiveKit](https://github.com/QuentinFuxa/WhisperLiveKit) by Quentin Fuxa.

## License

Apache-2.0 License - see LICENSE file for details.
