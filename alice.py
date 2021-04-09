import pyttsx3 as pyx


def say(request):
    engine = pyx.init()
    engine.say(request)
    engine.runAndWait()
