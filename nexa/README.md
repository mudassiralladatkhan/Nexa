Nexa Voice Assistant (Python Edition)
=====================================

Overview
--------
Nexa is a full Python reimplementation of the VocalPA assistant. It
reuses the existing web UX while replacing the Android/Kotlin stack
with Python services and clients.

Monorepo Layout
---------------
- `backend/` — FastAPI service that orchestrates command parsing,
  conversational context, wake-word configuration, and third-party
  API integrations (OpenWeather, NewsAPI, Spotify, etc.).
- `frontend/` — Rebranded copy of the existing PWA assets wired to the
  Python backend for data and command execution.
- `mobile/` — Kivy/KivyMD application delivering the Compose-style UX,
  background listening, and Android integrations such as notifications,
  calls, and media control through PyJNIus bridges.
- `shared/` — Pure-Python packages reused by both backend and mobile
  clients (command processor, phrase models, TTS/STT adapters,
  analytics, configuration).

Key Capabilities
----------------

**Voice Pipeline**
- Always-on wake-word detection powered by Porcupine/Snowboy adapters.
- Speech-to-text abstraction supporting Google Cloud Speech, Vosk
  offline models, or Whisper APIs.
- Text-to-speech drivers for pyttsx3 (offline) or cloud providers.
- Resilient error handling and automatic recovery mirroring the Kotlin
  implementation.

**Command & Context**
- Python port of VocalPA command processor with modular intent
  handlers for web search, app/site launching, calls, music control,
  reminders, jokes, facts, and more.
- Conversation memory persisted via SQLite/JsonStore and surfaced to
  both the mobile client and PWA.
- Localization hooks for multi-language command recognition.

**UX Parity**
- Compose-inspired layouts recreated with KivyMD widgets, custom
  canvas animations (voice waves, particles), onboarding flow, and
  permission dialogs.
- The web PWA keeps its CSS/JS animations but adopts new branding and
  API endpoints routed through the FastAPI backend.
- Cross-platform theming and settings synchronization handled by the
  shared configuration module.

Migration Roadmap
-----------------
1. Scaffold Python packages and tooling (poetry/pipenv, linting,
   testing).
2. Port command logic and API wrappers into `shared/`.
3. Build FastAPI backend endpoints + WebSocket channels for realtime
   updates.
4. Adapt the web frontend to call the new Python backend and rebrand to
   Nexa.
5. Develop the Kivy mobile client with background services, speech
   pipeline, and UI parity.
6. Integrate Android-specific hooks (battery optimization, notifications,
   call status) via PyJNIus.
7. Add comprehensive testing, packaging (Buildozer for APK, Docker for
   backend), and deployment scripts.

Environment Requirements
------------------------
- Python 3.11+
- Node.js (for frontend tooling and bundling)
- Android SDK & NDK (for Buildozer/Kivy Android builds)
- Poetry or Pipenv for dependency management (to be configured)

Next Steps
----------
- Initialize Python project scaffolding with dependency managers.
- Port command processor and API integrations into the shared module.
- Stand up the FastAPI backend with placeholder endpoints for
  frontend integration.

