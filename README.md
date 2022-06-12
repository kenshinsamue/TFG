
# Trabajo de Fin de Grado : Análisis y Pentesting de la Tecnología Bluetooth

Este proyecto utiliza la tecnologia Deep Learning para probar si el generador de cadena cifrante E0 es vulnerable. La implementacion utiliza pytorch como framework de DL 

La estructura del proyecto viene dividida de la siguiente forma:

## App

Es el directorio donde se guarda la aplicacion desarrollada en `Android Java`, de forma nativa.

## Bin

Es el directorio donde se guardan librerias usadas de forma local, entre ellas se pueden encontrar `pyubertooth`, `scapy`, `structured_data_regressor` y `usb`

## BT

Es el directorio que almacena los diferentes programas que automatizan la comunicacion con el HCI y el BUS del sistema, tambien esta guardado el simulador de claves del generador E0

## Documentacion

En este directorio se guarda documentacion que fue consultada de forma regular durante el desarrollo del proyecto

## Pruebas y resultados 

En este directorio se guardan las diferentes pruebas con modelos de deep learning, asi como pruebas para ver el rendimiento de los modelos dependiendo de la codificacion de los datos (binario o hexadecimal)

## Sniffing

Contiene el conjunto de programas que permiten realizar el sniffing y el entrenamiento de la red neuronal 

## Test 

Directorio con pruebas 

--------------------------------------

El programa principal es `main.py` y se apoya en `metodos.py` para acceder a las diferentes funcionalidades distribuidas a lo largo del proyecto. 


Para instalar los paquetes necesarios de python ejecutar 

`pip3 install -r requirements.txt`
