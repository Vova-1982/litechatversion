import speech_recognition as sr
import pyttsx3
from config_file import koef_relevant_model, stop_words, dict_lang, please_repeat
from model.tf_idf import classify_intent, answer_generation


def voice_to_text_translation(recognizer, audio):
    response = {
        "success": True,
        "transcription": None,
        "language": "en-US"
    }

    for key, lang in dict_lang.items():
        try:
            json_response = recognizer.recognize_google(audio, show_all=True, language=lang)
            dict_trancript = json_response.get('alternative')[0]
            print(lang)
            print("dict_trancript", dict_trancript)
            if dict_trancript.get('confidence') > koef_relevant_model:
                response["transcription"] = dict_trancript["transcript"]
                response["language"] = lang
                break
        except sr.RequestError:
            response["success"] = False
        except Exception:
            pass
    return response


def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    response = voice_to_text_translation(recognizer, audio)
    return response


def check_instanse(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")


def say_answer(ansver, lang):
    tts = pyttsx3.init()
    voices = tts.getProperty('voices')
    tts.setProperty('voice', lang)
    tts.say(ansver)
    tts.runAndWait()

def get_intent(replica, lang):
    return classify_intent(replica)


def get_answer(intent,lang):
    if intent is not None:
        return answer_generation(intent, lang)
    return please_repeat[lang]

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        check_instanse(recognizer, microphone)
        greeting = "Hello, I will try to answer your questions"
        print(greeting)

        while True:
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"] is not None:
                sentens = guess.get("transcription")
                if sentens in stop_words:
                    break
                else:
                    lang = guess.get("language")
                    intent = get_intent(sentens, lang)
                    answer = get_answer(intent, lang)
                    print(answer)
                    say_answer(answer, lang)

            elif not guess["success"]:
                print("problem to online servisse, please connetc late")
                break

            else:
                lang = guess.get("language")
                answer = get_answer(None, lang)
                print(answer)
                say_answer(answer, lang)

    except Exception as ex:
        print(ex)
