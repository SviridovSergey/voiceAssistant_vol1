from googlesearch import search  # поиск в Google
from pyowm import OWM  # использование OpenWeatherMap для получения данных о погоде
from dotenv import load_dotenv  # загрузка информации из .env-файла
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import pyttsx3  # синтез речи (Text-To-Speech)
import wikipediaapi  # поиск определений в Wikipedia
import random  # генератор случайных чисел
import webbrowser  # работа с использованием браузера по умолчанию (открывание вкладок с web-страницей)
import traceback  # вывод traceback без остановки работы программы при отлове исключений
import json  # работа с json-файлами и json-строками
import wave  # создание и чтение аудиофайлов формата wav
import os  # работа с файловой системой
import numpy as np



class OwnerPerson:
    """
    Информация о владельце, включающие имя, город проживания, родной язык речи, изучаемый язык (для переводов текста)
    """
    name = ""
    home_city = ""
    native_language = ""

ttsEngine = pyttsx3.init()
voices = ttsEngine.getProperty("voices")
ttsEngine.setProperty("voice",voices[1].id)
#что может джарвис(но не точно ха-ха)
def record_and_recognize_audio(*args:tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""
        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        try:
            print("Слушаю...")
            audio = recognizer.listen(microphone, 5, 5)

        except speech_recognition.WaitTimeoutError:
            print("Сер,посмотрите пожалуйста ваш микрофон включен")
            return
        # использование online-распознавания через Google
        try:
            print("Начинаю распознование...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass
        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            print("Проверьте пожалуйста свое интернет соединение,сер")
        return recognized_data
while True:
    voice_input = record_and_recognize_audio()
    print(voice_input)
    #инициализация инструмента синтеза речи

def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()
def play_greetings(*args: tuple):

    greetings = [
        ("Здраствуйте Сер,чем я могу помочь вам сегодня?")
    ]
    play_voice_assistant_speech(greetings[0])
def play_bue_and_quit(*args: tuple):
    farewells= [
        ("До свидания сер,Удачи вам")
    ]
    play_voice_assistant_speech(farewells[0])
    quit()

def execute_command_with_name(command_name: str, *args: list):
    """
    Выполнение заданной пользователем команды с дополнительными аргументами
    :param command_name: название команды
    :param args: аргументы, которые будут переданы в функцию
    :return:
    """
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            print("Command not found")
            pass

def search_on_google(*args: tuple):
    if not args[0]:
        return
    search_term=" ".join(args[0])

    url="https://www.google.com/search?q="+search_term
    webbrowser.get().open(url)

    search_results= []
    try:
        for _ in search(search_term,
                        tld="com",
                        num=1,
                        start=0,
                        stop=1,
                        pause=1.0,
                        ):
            search_results.append(_)
            webbrowser.get().open(_)
    except:
        play_bue_and_quit("Посмотрим что есть по вашему запросу")
        return
    print(search_results)
    play_voice_assistant_speech("Сер,вот что я нашел по {} в Google").format(search_term)

def search_on_youtube(*args: tuple):
    if not args[0]:
        return
    search_term=" ".join(args[0])
    url="https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open()
    play_voice_assistant_speech("Сер,вот что я нашел по вашему запросу").format(search_term)

def search_on_wikipedia(*args: tuple):
    if not args[0]:
        return
    search_term=" ".join(args[0])
    wiki=wikipediaapi.Wikipedia()
    wiki_page=wiki.page(search_term)
    try:
        if wiki_page.exists():
            play_voice_assistant_speech("Сер,вот что я нашел по вашему запросу на Wikipedia ").format(search_term)
            webbrowser.get().open(wiki_page.fullur1)
            # чтение ассистентом первых двух предложений summary со страницы Wikipedia
            play_voice_assistant_speech(wiki_page.summary.split(".")[:2])
        else:
            play_voice_assistant_speech(
                "Не могу найти {} в Википедии. Но вот что я нашел в Google").format(search_term)
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)
    except:
        play_voice_assistant_speech("Похоже, у нас проблема. Смотрите журналы для получения дополнительной информации")
        traceback.print_exc()
        return

commands= {
    ("привет","hi","hello"):play_greetings,
    ("пока","стоп","exit"):play_bue_and_quit,
    ("найди","поиск","gogle","search"):search_on_google,
    ("video","youtube","watch","видео"):search_on_youtube,
    ("wikipedia","определение","вики","википедия"):search_on_wikipedia,
    ("translate","перевод","перевести","переведи"):translate,
    ("погода","прогноз"):get_weather_forecast
}
#функция сигмоида,нужна для определения значения весов
def sigmoid(x,der=False):
    if der==True:
        return x*(1-x)
    return 1 / (1+np.exp(-x))

#для сигмоида
def taskTest():
    #входные данные
    x =np.array([[1,0,1],
                [1,0,1],
                [0,1,0],
                [0,1,0],])
    #выходные данные
    y=np.array([[0,0,1,1]]).T
    #более определенные случ числа
    np.random.seed(1)
    #инициализируем веса случ образом со средним 0
    syn0=2*np.random.random((3,1))-1

    l1=[]

    for iter in range(10000):
        #прямое распространение
        l0=x
        l1=sigmoid(np.dot(l0,syn0))
        #пепреножаем с наклоном сигмоиды на основе значения l1
        l1_error=y-l1
        l1_delta=l1_error*sigmoid(l1,True)
        #обновляем веса
        syn0+=np.dot(l0.T,l1_delta)
    print("данные после тренеровки:")
    print(l1)

#слова в духе да сер и нет сер(куда-нибудь их присунуть бы...)
def talkkAIyes():
    tts = pyttsx3.init()
    tts.say("секунду сер")
    tts.runAndWait()

def talkkAIno():
    tts = pyttsx3.init()
    tts.say("слушаюсь вас сер")
    tts.runAndWait()

#команды дальше
def get_weather_forecast(*args: tuple):
    """
    Получение и озвучивание прогнза погоды
    :param args: город, по которому должен выполняться запос
    """
    # в случае наличия дополнительного аргумента - запрос погоды происходит по нему,
    # иначе - используется город, заданный в настройках
    if args[0]:
        city_name = args[0][0]
    else:
        city_name = person.home_city

    try:
        # использование API-ключа, помещённого в .env-файл по примеру WEATHER_API_KEY = "01234abcd....."
        weather_api_key = os.getenv("88e8b6c2e9dd5190b8184499dec5d09c")
        open_weather_map = OWM(weather_api_key)

        # запрос данных о текущем состоянии погоды
        weather_manager = open_weather_map.weather_manager()
        observation = weather_manager.weather_at_place(city_name)
        weather = observation.weather

    # поскольку все ошибки предсказать сложно, то будет произведен отлов с последующим выводом без остановки программы
    except:
        play_voice_assistant_speech(("Сер,у нас походу возникли некоторые ошибки "))
        traceback.print_exc()
        return

    # разбивание данных на части для удобства работы с ними
    status = weather.detailed_status
    temperature = weather.temperature('celsius')["temp"]
    wind_speed = weather.wind()["speed"]
    pressure = int(weather.pressure["press"] / 1.333)  # переведено из гПА в мм рт.ст.

    # вывод логов
    print(("Weather in " + city_name +
                  ":\n * Status: " + status +
                  "\n * скорость ветра (m/s): " + str(wind_speed) +
                  "\n * температура (°C): " + str(temperature) +
                  "\n * давление (mm Hg): " + str(pressure)))

    # озвучивание текущего состояния погоды ассистентом (здесь для мультиязычности требуется дополнительная работа)
    play_voice_assistant_speech(("это {0} в {1}").format(status, city_name))
    play_voice_assistant_speech(("Сер,температура в {} °C").format(str(temperature)))
    play_voice_assistant_speech(("Сер,скорость ветра в {} m/s").format(str(wind_speed)))
    play_voice_assistant_speech(("Сер,давление в {} mm Hg").format(str(pressure)))

def search_person(*args: tuple):
    if not args[0]:
        return
    google_search=" ".join(args[0])
    vk_search=" ".join(args[0])

    # открытие ссылки на поисковик в браузере
    url = "https://google.com/search?q=" + google_search + " site: vk.com"
    webbrowser.get().open(url)

    # открытие ссылкок на поисковики социальных сетей в браузере
    vk_url = "https://vk.com/people/" + vk_search
    webbrowser.get().open(vk_url)

    play_voice_assistant_speech(("Here is what I found for "
    "{} on social nets").format(google_search))

#основная функция где выбираются команды
def comands(command_name:str,*args: tuple):
    for item in commands.keys():
        if command_name in item:
            commands[item](*args)
        else:
            print("Сер,я вас не понял")
            play_voice_assistant_speech("Сер,я вас не понял")
            pass

if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    person = OwnerPerson()
    person.name = "sergey"
    person.home_city = "Rostov-on-Don"
    person.native_language = "ru"

    while True:
        # старт записи речи с последующим выводом распознанной речи и удалением записанного в микрофон аудио
        voice_input = record_and_recognize_audio()

        # отделение комманд от дополнительной информации (аргументов)
        voice_input = voice_input.split(" ")
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_name(command, command_options)