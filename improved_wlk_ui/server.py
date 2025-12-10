"""
This server is based on the basic_server.py of "upstream" WhisperLiveKit. However, it is extended to include some further features.
The main difference is, that this is standalone
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from whisperlivekit import (
    AudioProcessor,
    TranscriptionEngine,
    parse_args,
)

from .speaker_names import SpeakerNameManager, SpeakerNameUpdate

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.getLogger().setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

args = parse_args()
transcription_engine = None
speaker_names = SpeakerNameManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for FastAPI app."""
    global transcription_engine
    transcription_engine = TranscriptionEngine(
        **vars(args),
    )
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get():
    """Serve the enhanced UI with speaker name management."""
    web_dir = Path(__file__).parent / "web"
    html_file = web_dir / "live_transcription.html"

    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    return HTMLResponse(html_content)


# Speaker Name API Endpoints
@app.get("/api/speakers")
async def get_speaker_names():
    """Get all speaker name mappings."""
    return {"speakers": speaker_names.get_all_mappings()}


@app.post("/api/speakers")
async def set_speaker_name(data: SpeakerNameUpdate):
    """Set or update a speaker's custom name."""
    speaker_names.set_name(data.speaker_id, data.name)
    return {"success": True, "speaker_id": data.speaker_id, "name": data.name}


@app.delete("/api/speakers/{speaker_id}")
async def delete_speaker_name(speaker_id: int):
    """Remove a speaker's custom name (revert to numeric)."""
    speaker_names.remove_name(speaker_id)
    return {"success": True, "speaker_id": speaker_id}


@app.delete("/api/speakers")
async def clear_all_speaker_names():
    """Clear all custom speaker names."""
    speaker_names.clear()
    return {"success": True}


@app.get("/{file_path:path}")
async def serve_web_assets(file_path: str):
    """Serve web assets (CSS, JS, images, etc.)."""
    web_dir = Path(__file__).parent / "web"
    file = web_dir / file_path

    if file.exists() and file.is_file():
        return FileResponse(file)

    # If not found in our web dir, return 404
    return HTMLResponse(content="Not Found", status_code=404)


async def handle_websocket_results(websocket, results_generator):
    """Consumes results from the audio processor and sends them via WebSocket."""
    try:
        async for response in results_generator:
            # Inject speaker names into the response
            response_dict = response.to_dict()
            for line in response_dict.get("lines", []):
                speaker_id = line.get("speaker")
                if speaker_id and speaker_id > 0:
                    line["speaker_name"] = speaker_names.get_name(speaker_id)
            await websocket.send_json(response_dict)
        logger.info("Results generator finished. Sending 'ready_to_stop' to client.")
        await websocket.send_json({"type": "ready_to_stop"})
    except WebSocketDisconnect:
        logger.info(
            "WebSocket disconnected while handling results (client likely closed connection)."
        )
    except Exception as e:
        logger.exception(f"Error in WebSocket results handler: {e}")


@app.websocket("/asr")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for audio streaming and transcription."""
    global transcription_engine
    audio_processor = AudioProcessor(
        transcription_engine=transcription_engine,
    )
    await websocket.accept()
    logger.info("WebSocket connection opened.")

    try:
        await websocket.send_json(
            {"type": "config", "useAudioWorklet": bool(args.pcm_input)}
        )
    except Exception as e:
        logger.warning(f"Failed to send config to client: {e}")

    results_generator = await audio_processor.create_tasks()
    websocket_task = asyncio.create_task(
        handle_websocket_results(websocket, results_generator)
    )

    try:
        while True:
            message = await websocket.receive_bytes()
            await audio_processor.process_audio(message)
    except KeyError as e:
        if "bytes" in str(e):
            logger.warning("Client has closed the connection.")
        else:
            logger.error(
                f"Unexpected KeyError in websocket_endpoint: {e}", exc_info=True
            )
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected by client during message receiving loop.")
    except Exception as e:
        logger.error(
            f"Unexpected error in websocket_endpoint main loop: {e}",
            exc_info=True,
        )
    finally:
        logger.info("Cleaning up WebSocket endpoint...")
        if not websocket_task.done():
            websocket_task.cancel()
        try:
            await websocket_task
        except asyncio.CancelledError:
            logger.info("WebSocket results handler task was cancelled.")
        except Exception as e:
            logger.warning(f"Exception while awaiting websocket_task completion: {e}")

        await audio_processor.cleanup()
        logger.info("WebSocket endpoint cleaned up successfully.")


def main():
    """Entry point for the CLI command."""
    import uvicorn

    uvicorn_kwargs = {
        "app": "improved_wlk_ui.server:app",
        "host": args.host,
        "port": args.port,
        "reload": False,
        "log_level": "info",
        "lifespan": "on",
    }

    ssl_kwargs = {}
    if args.ssl_certfile or args.ssl_keyfile:
        if not (args.ssl_certfile and args.ssl_keyfile):
            raise ValueError(
                "Both --ssl-certfile and --ssl-keyfile must be specified together."
            )
        ssl_kwargs = {
            "ssl_certfile": args.ssl_certfile,
            "ssl_keyfile": args.ssl_keyfile,
        }

    if ssl_kwargs:
        uvicorn_kwargs = {**uvicorn_kwargs, **ssl_kwargs}
    if args.forwarded_allow_ips:
        uvicorn_kwargs = {
            **uvicorn_kwargs,
            "forwarded_allow_ips": args.forwarded_allow_ips,
        }

    uvicorn.run(**uvicorn_kwargs)


if __name__ == "__main__":
    main()
