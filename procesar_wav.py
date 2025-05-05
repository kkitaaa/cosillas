import wave
import numpy as np

# Ruta del archivo de entrada
input = "song.wav"
output = "out.wav"

# Abrir el archivo WAV original en modo lectura
with wave.open(input, 'rb') as wav_in:
    n_channels, sampwidth, framerate, n_frames = wav_in.getparams()[:4]
    
    # Leer todos los frames
    frames = wav_in.readframes(n_frames)

# Convertir los datos binarios en un arreglo NumPy de enteros de 16 bits
audio_data = np.frombuffer(frames, dtype=np.int16)

# Como el audio es estéreo, los datos están intercalados: [L, R, L, R, ...]
# Separamos los canales
canal_izq = audio_data[0::2]
canal_der = audio_data[1::2]

# Invertimos el canal derecho
canal_der_rev = canal_der[::-1]

# Reducimos la frecuencia de muestreo a la mitad (de 44100 a 22050 Hz)
# Esto se hace tomando una muestra de cada dos
canal_der_procesado = canal_der_rev[::2]

# Guardamos el resultado como un nuevo archivo WAV en formato mono
with wave.open(output, 'wb') as wav_out:
    wav_out.setnchannels(1)        # Mono
    wav_out.setsampwidth(2)        # 16 bits por muestra (2 bytes)
    wav_out.setframerate(22050)    # Nueva tasa de muestreo
    wav_out.writeframes(canal_der_procesado.tobytes())

print("Archivo procesado y guardado como", output)
