import speech_recognition as sr
import pyttsx3

# Simple mapping of Czech voice commands to responses
RESPONSES = {
    "ahoj": "Ahoj! Jak se máš?",
    "jak se jmenujes": "Jsem jednoduchý hlasový agent.",
    "nápověda": "Můžeš mi položit otázku, například 'Jak se jmenuješ?'."
}


def speak(text: str) -> None:
    """Use text-to-speech to say `text` in Czech."""
    engine = pyttsx3.init()
    engine.setProperty("voice", "cs")
    engine.say(text)
    engine.runAndWait()


def respond(command: str) -> str:
    """Return a Czech response based on the text command."""
    normalized = command.lower()
    return RESPONSES.get(normalized, "Omlouvám se, nerozumím.")


def main() -> None:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Zkuste promluvit. (Řekněte 'Ahoj' nebo 'Jak se jmenuješ')")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

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
