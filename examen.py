import psutil
import time
import paho.mqtt.client as mqtt
import json 


BROKER = '127.0.0.1'  
PORT = 1883  
TOPIC_CPU = 'examen/cpu'
TOPIC_RAM = 'examen/ram'


client = mqtt.Client()
client.connect(BROKER, PORT, 60) 
client.loop_start()  

def obtener_datos_sistema():

    uso_cpu = psutil.cpu_percent(interval=1)

    
    uso_memoria = psutil.virtual_memory().percent

    return uso_cpu, uso_memoria

def registrar_datos():
    while True:
        
        cpu, memoria = obtener_datos_sistema()

        
        mensaje_cpu = {
            'cpu_usage': cpu
        }
        mensaje_ram = {
            'ram_usage': memoria
        }

        
        client.publish(TOPIC_CPU, json.dumps(mensaje_cpu))  
        client.publish(TOPIC_RAM, json.dumps(mensaje_ram))  

        
        print(f"Uso de CPU: {cpu}%")
        print(f"Uso de Memoria RAM: {memoria}%")

        time.sleep(5)  

if __name__ == "__main__":
    registrar_datos()  
