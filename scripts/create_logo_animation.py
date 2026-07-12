from __future__ import annotations

import re
import shutil
import socket
import subprocess
import tempfile
import time
import base64
import json
from pathlib import Path

import requests
import websocket


ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / "index.html"
OUT_DIR = ROOT / "img"
TMP_DIR = ROOT / ".tmp_logo_animation"
FRAMES_DIR = TMP_DIR / "frames"
EXPORT_HTML = TMP_DIR / "logo_intro_export.html"
MP4_PATH = OUT_DIR / "project-neura-logo-build.mp4"
GIF_PATH = OUT_DIR / "project-neura-logo-build.gif"

SIZE = 1080
EXPORT_CROP = 560
FPS = 30
DURATION = 3.3
FRAME_COUNT = int(FPS * DURATION)


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


class CdpClient:
    def __init__(self, url: str) -> None:
        self.ws = websocket.create_connection(url, timeout=30)
        self.next_id = 1

    def call(self, method: str, params: dict | None = None) -> dict:
        message_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == message_id:
                if "error" in message:
                    raise RuntimeError(f"CDP {method} failed: {message['error']}")
                return message.get("result", {})

    def close(self) -> None:
        self.ws.close()


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def chrome_path() -> str:
    candidates = [
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise RuntimeError("Could not find Chrome/Chromium for CSS animation rendering.")


def read_web_intro() -> tuple[str, str]:
    html = INDEX_HTML.read_text(encoding="utf-8")
    style_match = re.search(r"<style>(.*?)</style>", html, re.S)
    if not style_match:
        raise RuntimeError("Could not find the <style> block in index.html.")

    overlay_match = re.search(
        r'(<div class="intro-overlay" id="introOverlay" aria-hidden="true">.*?</div>\s*</div>)\s*<header',
        html,
        re.S,
    )
    if not overlay_match:
        raise RuntimeError("Could not find the intro overlay markup in index.html.")

    return style_match.group(1), overlay_match.group(1)


def write_export_html() -> None:
    style, overlay = read_web_intro()
    EXPORT_HTML.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <base href="{ROOT.as_uri()}/" />
    <style>
{style}
        body {{
            width: {SIZE}px;
            height: {SIZE}px;
        }}

        .intro-overlay {{
            width: {SIZE}px;
            height: {SIZE}px;
        }}
    </style>
</head>
<body class="intro-lock">
    {overlay}
</body>
</html>
""",
        encoding="utf-8",
    )


def wait_for_cdp(port: int) -> str:
    deadline = time.time() + 20
    version_url = f"http://127.0.0.1:{port}/json/version"
    while time.time() < deadline:
        try:
            response = requests.get(version_url, timeout=0.5)
            if response.ok:
                return str(response.json()["webSocketDebuggerUrl"])
        except requests.RequestException:
            time.sleep(0.1)
    raise RuntimeError("Timed out waiting for Chrome DevTools endpoint.")


def capture_frames_with_chrome(chrome: str) -> None:
    port = free_port()
    with tempfile.TemporaryDirectory(prefix="neura-chrome-profile-") as profile:
        process = subprocess.Popen(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--disable-background-networking",
                "--disable-default-apps",
                "--disable-extensions",
                "--disable-sync",
                "--hide-scrollbars",
                "--no-first-run",
                "--no-default-browser-check",
                "--run-all-compositor-stages-before-draw",
                "--remote-allow-origins=*",
                f"--remote-debugging-port={port}",
                f"--user-data-dir={profile}",
                f"--window-size={SIZE},{SIZE}",
                "about:blank",
            ],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        client: CdpClient | None = None
        try:
            browser_ws = wait_for_cdp(port)
            client = CdpClient(browser_ws)
            target = client.call("Target.createTarget", {"url": EXPORT_HTML.as_uri()})
            targets = requests.get(f"http://127.0.0.1:{port}/json/list", timeout=5).json()
            page_ws = next(item["webSocketDebuggerUrl"] for item in targets if item["id"] == target["targetId"])
            client.close()
            client = CdpClient(page_ws)

            client.call("Page.enable")
            client.call("Runtime.enable")
            client.call(
                "Emulation.setDeviceMetricsOverride",
                {
                    "width": SIZE,
                    "height": SIZE,
                    "deviceScaleFactor": 1,
                    "mobile": False,
                    "screenWidth": SIZE,
                    "screenHeight": SIZE,
                },
            )

            # Ensure document, CSS, and images are ready before seeking animation time.
            client.call(
                "Runtime.evaluate",
                {
                    "expression": "document.fonts ? document.fonts.ready.then(() => document.readyState) : document.readyState",
                    "awaitPromise": True,
                },
            )

            for frame_index in range(FRAME_COUNT):
                seconds = frame_index / FPS
                expression = f"""
                    new Promise((resolve) => {{
                        const t = {seconds * 1000:.4f};
                        document.body.classList.add("intro-lock");
                        for (const animation of document.getAnimations({{ subtree: true }})) {{
                            animation.pause();
                            animation.currentTime = t;
                        }}
                        requestAnimationFrame(() => requestAnimationFrame(resolve));
                    }})
                """
                client.call("Runtime.evaluate", {"expression": expression, "awaitPromise": True})
                screenshot = client.call("Page.captureScreenshot", {"format": "png", "fromSurface": True})
                frame_path = FRAMES_DIR / f"frame_{frame_index:04d}.png"
                frame_path.write_bytes(base64.b64decode(screenshot["data"]))
                if frame_index % 15 == 0:
                    print(f"Captured frame {frame_index + 1}/{FRAME_COUNT}")
        finally:
            if client is not None:
                client.close()
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


def capture_frames() -> None:
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    write_export_html()

    chrome = chrome_path()
    capture_frames_with_chrome(chrome)


def encode() -> None:
    crop_filter = f"crop={EXPORT_CROP}:{EXPORT_CROP}:(iw-{EXPORT_CROP})/2:(ih-{EXPORT_CROP})/2"
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(FRAMES_DIR / "frame_%04d.png"),
            "-vf",
            f"{crop_filter},scale={SIZE}:{SIZE}:flags=lanczos",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(MP4_PATH),
        ]
    )

    palette = TMP_DIR / "palette.png"
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(FRAMES_DIR / "frame_%04d.png"),
            "-vf",
            f"fps=20,{crop_filter},scale=720:720:flags=lanczos,palettegen",
            "-frames:v",
            "1",
            "-update",
            "1",
            str(palette),
        ]
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(FRAMES_DIR / "frame_%04d.png"),
            "-i",
            str(palette),
            "-lavfi",
            f"fps=20,{crop_filter},scale=720:720:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3",
            "-loop",
            "0",
            str(GIF_PATH),
        ]
    )


def main() -> None:
    capture_frames()
    encode()
    print(f"Wrote {MP4_PATH.relative_to(ROOT)}")
    print(f"Wrote {GIF_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
