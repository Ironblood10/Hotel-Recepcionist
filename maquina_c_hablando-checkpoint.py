import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import pickle
import random
import speech_recognition as sr
from gtts import gTTS
import pyttsx3

#Cargar el clasificador desde el archivo pickle
with open('modelo_clasificador_SVC.pkl', 'rb') as archivo_modelo:
    clasificador = pickle.load(archivo_modelo)

#Cargar el conjunto de datos desde el archivo CSV
df = pd.read_csv('hoteis.csv')

# Crear una instancia de CountVectorizer y ajustar/transformar el conjunto completo
vectorizer = CountVectorizer()
X_features = vectorizer.fit_transform(df['comentario'])

#Variable para controlar si ya se respondió al saludo
respuesta_saludo = False

#Máquina de estados para la interacción por consola
estado_actual = "inicio"

#Función para preprocesar el texto de la reseña
def preprocesar_texto(texto):
    return texto

# Función para clasificar una reseña
def clasificar_resena(resena):
    texto_procesado = vectorizer.transform([preprocesar_texto(resena)])
    prediccion = clasificador.predict(texto_procesado)
    return "Positiva" if prediccion[0] == 1 else "Negativa"

#Función para convertir texto a voz
"""def texto_a_voz(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save("output.mp3")
    playsound.playsound("output.mp3")
"""
def texto_a_voz(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

#Función para reconocimiento de voz 1
def voz_a_texto_saludo():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        try:
            audio = recognizer.listen(source, timeout= 5)
        except sr.WaitTimeoutError:
            print("Tiempo de espera agotado. ¿Puedes repetir tu respuesta?")

    try:
        print("Reconociendo...")
        texto = recognizer.recognize_google(audio, language="es")
        return texto
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error en la solicitud de reconocimiento de voz; {e}")
        return ""

#Función para reconocimiento de voz 2
def voz_a_texto():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        try:
            audio = recognizer.listen(source, timeout= 3)
        except sr.WaitTimeoutError:
            print("Tiempo de espera agotado. ¿Puedes repetir tu respuesta?")

    try:
        print("Reconociendo...")
        texto = recognizer.recognize_google(audio, language="es")
        return texto
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error en la solicitud de reconocimiento de voz; {e}")
        return ""
    except sr.WaitTimeoutError:
            print("Tiempo de espera agotado. ¿Puedes repetir tu respuesta?")
            return None
    
#Función para reconocimiento de voz 3
def voz_a_texto_opinion():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        try:
            audio = recognizer.listen(source, timeout= 35) #Diferentes tiempos opiniones más largas
        except sr.WaitTimeoutError:
            print("Tiempo de espera agotado. ¿Puedes repetir tu respuesta?")

    try:
        print("Reconociendo...")
        texto = recognizer.recognize_google(audio, language="es")
        return texto
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error en la solicitud de reconocimiento de voz; {e}")
        return ""
    except sr.WaitTimeoutError:
            print("Tiempo de espera agotado. ¿Puedes repetir tu respuesta?")
            return None

#Gestión de nodos:
while estado_actual != "salir":
    if estado_actual == "inicio":
        #Genera un saludo aleatorio
        saludo = random.randint(1, 3)
        if saludo == 1:
            texto_a_voz("¡Hola!")
        elif saludo == 2:
            texto_a_voz("¡Buenas!")
        else:
            texto_a_voz("¡Encantado!")
        estado_actual = "saludo"

    if estado_actual == "saludo":
        #Espera la respuesta del usuario al saludo
        respuesta_usuario= voz_a_texto_saludo()
        #Hace la pregunta
        pregunta_agente= texto_a_voz("¿Es su último día aquí?")
        respuesta_usuario = voz_a_texto() #Hay que decir frases más largas, no vale "si o sí". Ej: La verdad es que sí.
        if "si" in respuesta_usuario.lower() or "sí" in respuesta_usuario.lower():
            #Pregunta de opinión aleatoria
            pregunta = random.randint(1, 3)
            if pregunta == 1:
                texto_a_voz("Vale, ¿le importaría darme su opinión respecto a su estancia?")
            elif pregunta == 2:
                texto_a_voz("Bien, ¿podría decirme qué tal lo ha pasado?")
            else:
                texto_a_voz("Genial, ¿cómo describiría su experiencia en nuestro hotel?")

            estado_actual = "respuesta"
            continue
        elif "no" in respuesta_usuario.lower(): #Con no funciona bien
            #Disculpa y despedida
            disculpa = random.randint(1, 3)
            if disculpa == 1:
                texto_a_voz("Vale. Siento molestarle.")
            elif disculpa == 2:
                texto_a_voz("Disculpe la intromisión. Siga disfrutando de su estancia.")
            else:
                texto_a_voz("Perdone. Seguiré caminando.")

            estado_actual = "salir"
            continue
        else:
            texto_a_voz("No entendí. ¿Podría repetir?")
            continue

    if estado_actual == "respuesta":
        #Espera la respuesta del usuario a la pregunta
        reseña = voz_a_texto_opinion()

        #Ajusta el vectorizador con la nueva reseña
        texto_procesado = vectorizer.transform([preprocesar_texto(reseña)])
        prediccion = clasificador.predict(texto_procesado)

        if prediccion[0] == 1:
            despedida_positiva = random.randint(1, 4)
            if despedida_positiva == 1:
                texto_a_voz("Gracias por su opinión. Nos alegramos de que haya disfrutado de su estancia.")
            elif despedida_positiva == 2:
                texto_a_voz("Un placer. Seguiremos esforzándonos para prestar los mejores servicios.")
            elif despedida_positiva == 3:
                texto_a_voz("Nos alegra oír eso. Muchas gracias y que tenga un buen día.")
            else:
                texto_a_voz("Ha sido un placer tenerle como huésped. Esperamos verle pronto.")
        else:
            despedida_negativa = random.randint(1, 4)
            if despedida_negativa == 1:
                texto_a_voz("Lamentamos oír eso. Nos esforzaremos más. Muchas gracias por su valoración.")
            elif despedida_negativa == 2:
                texto_a_voz("Lo sentimos. Trataremos de mejorar en los aspectos que ha comentado.")
            elif despedida_negativa == 3:
                texto_a_voz("Sentimos que su estancia no haya sido de su agrado. Intentaremos mejorar.")
            else:
                texto_a_voz("Siempre es bueno recibir este tipo de críticas. Las tendremos en cuenta para mejorar nuestra calidad de servicios prestada. Gracias.")
        estado_actual = "salir"
