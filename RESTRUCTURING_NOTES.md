# Repository Restructuring Summary

Early December 2025 the repo was restructured to be independent from "upstream" WhisperLiveKit. <br/> 
This was necessary and the obvious step to take. 

## What Changed? (Before and after)

### Before
- The entire codebase was in the `whisperlivekit/` directory
- All modifications in this repo were done directly in those original WLK files
- Later on, just the streamlit interface was it's own file (only feature that didn't rely on the WLK Stack)

### Issues
- This led to some rather obvious issues:
  - Hard time incorporating "upstream" updates (including new features and fixes)
  - cluttered codebase
  - dependent on there being no or few changes in the upstream UI/server files
  
### After
- Standalone `improved_wlk_ui` repo, that extends the features of upstream WLK:
  - The server now features an interface for customizing names of detected speakers (when using diarization)
  - The name-changing feature is exposed as an API-Endpoint
  - There is a Streamlit UI for configuring and launching the WLK Session. End-user-friendlier than the CLI of WLK
- Own (necessary) adjustments to the UI now have an clean foundation
- WhisperLiveKit is installed as PyPI dependency and configured separately. 
- This separates custom code and upstream cleanly

## New Package Structure

```
improved_wlk_ui/
├── __init__.py              # Package exports
├── speaker_names.py         # SpeakerNameManager & SpeakerNameUpdate (... for customizing SpeakerNames)
├── server.py               # Extended FastAPI server (based on basic_server.py from upstream)
├── streamlit_app.py        # Streamlit GUI launcher
└── web/                   # Complete web assets
    ├── live_transcription.html     # based on the respective file from upstream WLK
    ├── live_transcription.css      # based on the respective file from upstream WLK
    ├── live_transcription.js       # based on the respective file from upstream WLK
    ├── pcm_worklet.js              # based on the respective file from upstream WLK
    ├── recorder_worker.js          # based on the respective file from upstream WLK    
    └── src/               # SVG icons      # based on the respective file(s) from upstream WLK
```

## Key Features

### 1. Speaker Name Management
- `SpeakerNameManager` class for mapping speaker IDs to names
- `SpeakerNameUpdate` Pydantic model for API requests
- Standalone module, reusable

### 2. Extended Server
- Extends WhisperLiveKit server with speaker name API
- REST endpoints: GET/POST/DELETE `/api/speakers`
- Injects `speaker_name` into WebSocket responses
- Serves custom HTML/CSS/JS

### 3. Enhanced Web UI
- Speaker editor button (👤 Speakers)
- Speaker name management panel (accessible through aforementioned button)
- Real-time speaker name display in transcripts (replacing 1,2,3 etc.)
- All custom UI in inline styles/scripts

### 4. Streamlit Interface
- GUI for configuring and launching server
- Adapted to use `improved_wlk_ui.server` instead of base WLK
- Includes a command builder as well as all current (December 2025) Options from WLK
- Relevant values all have their appropriate default for my current use case, to be separated into a config file
- Essentially builds a command with modifiers etc., then runs that in a terminal
## Installation

```bash
# From PyPI (once published)
pip install improved-wlk-ui # not implemented yet!

# From source
git clone https://github.com/AeneasChristodoulou/Improved-WLK-UI.git
cd Improved-WLK-UI
pip install -e .
```

## Usage

```bash
# Streamlit interface (recommended)
streamlit run -m improved_wlk_ui.streamlit_app

# Direct server launch
improved-wlk-server --model large-v3-turbo --diarization # one bug is yet to be swatted for direct server, use streamlit!
```

## Dependencies

- `whisperlivekit>=0.2.15` - Base transcription engine
- `streamlit>=1.28.0` - GUI framework
- `pydantic>=2.0.0` - Data validation
- `faster-whisper>=1.2.1` - recommended for most users as it speeds performance up, might wanna remove that as dependency

## Getting started

### For Users
1. Clone the repo
2. Install it with `pip install -e`
3. Use new commands: ~~`improved-wlk-server`~~ or `streamlit run improved_wlk_ui/streamlit_app.py`
4. All features from "upstream" WLK are preserved, but now you can adjust the names of any and all speakers!
5. Update "upstream" wlk via pip

### For Developers
1. Clone the repo
2. Install in editable mode: `pip install -e .`
3. Custom code now in `improved_wlk_ui/` directory
4. WhisperLiveKit updates pulled automatically via pip


## Next Steps

1. Test with actual WhisperLiveKit installation
2. Verify transcription + speaker diarization works
3. Test speaker name editor in browser
4. Publish to PyPI (if desired)
