# Fall Detection System
Real-time fall detection using webcam, MediaPipe, and OpenCV. Sends WhatsApp alert with image on fall detection.

> **Disclaimer:** Detection results may not be accurate. Do not rely on this system as a sole safety measure.

## Install
pip install opencv-python mediapipe pywhatkit pyautogui

## Notes
- WhatsApp Web must be logged in on your browser
- Model file is auto-downloaded on first run

## Libraries Used
- [MediaPipe](https://github.com/google-ai-edge/mediapipe) — Apache 2.0
- [OpenCV](https://github.com/opencv/opencv) — Apache 2.0
- [pywhatkit](https://github.com/Ankit404butfound/PyWhatKit) — MIT
- [PyAutoGUI](https://github.com/asweigart/pyautogui) — BSD 3-Clause

## Legal
This project uses the MediaPipe Pose Landmarker Lite model sourced from Google Cloud Storage under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). No modifications were made to the model.

This project is intended for educational and personal use only. The author assumes no liability for any misuse or inaccurate detection results.
