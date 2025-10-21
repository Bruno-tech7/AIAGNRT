from typing import Any, Optional

RESPONSES = {
    "ahoj": "Ahoj! Jak se máš?",
    "jak se jmenujes": "Jsem jednoduchý hlasový agent.",
    "nápověda": "Můžeš mi položit otázku, například 'Jak se jmenuješ?'."
}

_TTS_ENGINE: Optional[Any] = None
_TTS_VOICE_ID: Optional[str] = None


def _choose_voice_id(engine: Any) -> Optional[str]:
    try:
        voices = engine.getProperty("voices") or []
    except Exception:
        return None

    # Prefer Czech/Zuzana if available; otherwise keep default
    preferred_id: Optional[str] = None
    for voice in voices:
        name = getattr(voice, "name", "") or ""
        voice_id = getattr(voice, "id", None)
        langs = getattr(voice, "languages", None)
        lang_str = ""
        if isinstance(langs, (list, tuple)) and langs:
            first = langs[0]
            try:
                lang_str = first.decode("utf-8", errors="ignore") if isinstance(first, (bytes, bytearray)) else str(first)
            except Exception:
                lang_str = str(first)
        elif hasattr(voice, "lang"):
            lang_str = str(getattr(voice, "lang", ""))

        lower_name = name.lower()
        lower_lang = lang_str.lower()
        if "zuzana" in lower_name or "czech" in lower_name or "cs" in lower_lang:
            preferred_id = voice_id
            break

    return preferred_id


def _init_tts_engine() -> Any:
    # Lazy import to reduce load time if TTS is unused
    try:
        import pyttsx3  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "K běhu TTS je potřeba balíček 'pyttsx3'. Nainstalujte jej: pip install pyttsx3"
        ) from e

    # Prefer a lightweight driver selection by deferring to defaults
    engine = pyttsx3.init()
    voice_id = _choose_voice_id(engine)
    if voice_id:
        try:
            engine.setProperty("voice", voice_id)
        except Exception:
            pass
    return engine


def _get_tts_engine() -> Optional[Any]:
    global _TTS_ENGINE
    if _TTS_ENGINE is None:
        try:
            _TTS_ENGINE = _init_tts_engine()
        except Exception as e:
            print(f"Text-to-speech nelze inicializovat: {e}")
            _TTS_ENGINE = None
    return _TTS_ENGINE


def speak(text: str) -> None:
    engine = _get_tts_engine()
    if engine is None:
        # Bez TTS pouze vypiš text, aby UX nebylo zcela prázdné
        print(text)
        return
    engine.say(text)
    engine.runAndWait()

def respond(command: str) -> str:
    normalized = command.lower()
    return RESPONSES.get(normalized, "Omlouvám se, nerozumím.")

def main() -> None:
    try:
        import speech_recognition as sr  # Lazy import to speed module import
    except Exception as e:
        print("K běhu je potřeba balíček 'speech_recognition'. Nainstalujte jej: pip install SpeechRecognition")
        print(f"Chyba importu: {e}")
        return

    recognizer = sr.Recognizer()
    # Rychlejší start: kratší kalibrace hluku a omezení délky věty
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.6

    try:
        mic = sr.Microphone()
    except OSError as mic_err:
        print(f"Nelze otevřít mikrofon: {mic_err}")
        return

    print("Zkuste promluvit. (Řekněte 'Ahoj' nebo 'Jak se jmenuješ')")
    with mic as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
        except Exception:
            pass
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
        except sr.WaitTimeoutError:
            print("Vypršel časový limit pro začátek mluvení.")
            return

    try:
        command = recognizer.recognize_google(audio, language="cs-CZ")
        print(f"Rozpoznáno: {command}")
        answer = respond(command)
        print(answer)
        speak(answer)
    except sr.UnknownValueError:
        print("Hlasu nebylo rozuměno.")
    except sr.RequestError as e:
        print(f"Chyba rozpoznávání: {e}")

if __name__ == "__main__":
    main()
