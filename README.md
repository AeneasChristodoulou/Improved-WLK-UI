# Improved WLK UI

Enhanced UI and speaker name management for WhisperLiveKit. Exposes all Options from the Terminal in a streamlit-based GUI.<br/>
Developed by a backend-dude for end users, not too pretty but decent and functional. 

## Features

- **Streamlit-based GUI** for easy server configuration and launching
- **Custom speaker name assignment** - map "Speaker 1" → "Alice", "Speaker 2" → "Bob", etc.
- **Speaker names persist** and display in real-time live transcription
- **Extended REST API** for managing speaker names programmatically
- **Full WhisperLiveKit compatibility** - uses WhisperLiveKit as a dependency

## Installation
~~Use pip~~ **_(to be implemented):_**
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
streamlit run streamlit_app.py
```

This provides a user-friendly GUI to:
- Configure all WhisperLiveKit options
- Select models, languages, and features
- Enable/disable speaker diarization
- Start and stop the server
- View server logs in real-time

It also sets quite a bunch of default values. They are all adjustable, currently inside of ```streamlit_app.py```.<br />
The values are set to what I found works best for my usage scenario. Your milage may vary! <br />

Hardware used to test this tool:
HP ZBook Fury 16 G11 Workstation (Laptop)<br />
GPU: NVIDIA RTX 4000 Ada Generation Laptop GPU (afaik equivalent to an RTX 4080?)<br />
CPU: Intel Core i7 14700HX <br />
RAM: 64GBs <br />

I purposefully set the model to large-v3-turbo per default, as this is the best "bang for the buck" if you have decent hardware <br />
If you have even more potent hardware or you live in a future where that specific issue has been fixed, feel free to change ```--max-context-tokens```. <br />
I set it to ```125``` per default, as otherwise WLK with sortformer tended to loop and crash as well as get very slow due to filling the VRAM to the brim.

### ~~Run the Enhanced Server Directly~~

~~You can also run the enhanced server directly from the command line:~~
```Nope you cannot right now! Since I dont use this myself I am also too lazy. Gotta find the issue with from .speaker_names import .... ```
```bash
# Basic usage with speaker diarization
python server.py --model large-v3-turbo --diarization

# Custom port and host
python server.py--model base --port 8000 --host 192.168.0.42

# With translation
python server.py --model medium --language fr --target-language en
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
3. **Save** your changes, names will persist for the duration of the server session
4. **See it in action** - speaker names will appear automatically in the live transcription. No reload required!

## API Endpoints

The Improved WLK UI server provides REST API endpoints for managing speaker names:

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

### Set a new speaker name

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

## TL;DR
This repo provides standalone UI Improvements to WhisperLiveKit. Namely, you can add custom names to all detected Speakers <br/>
and there is a GUI based on streamlit for end users to easily launch and configure the tool. <br/>
It only provides the relevant files needed to improve the UI/UX. You still need to install and setup WhisperLiveKit. <br/>

For a link to QuentinFuxa/WhisperLiveKit see "Credits".

## Development

To contribute or modify the code, install from source:

```bash
git clone https://github.com/AeneasChristodoulou/Improved-WLK-UI.git
cd Improved-WLK-UI
pip install -e ".[dev]"
```

## Credits

This project builds upon [WhisperLiveKit](https://github.com/QuentinFuxa/WhisperLiveKit) by Quentin Fuxa.

## License

Apache-2.0 License - see LICENSE file for details.
