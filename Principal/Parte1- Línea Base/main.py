import rrdtool
import time
import _thread
import Notify
from getSNMP import consultaSNMP
import trendGraphDetection as graph

def creacionrrd(nombre):    #Usamos la dirección IP como nombre del dispositivo
    rutafinal = "/home/gonzalo/PycharmProjects/Practica2/Principal/RRD/"+nombre+".rrd" #creamos la base con el nombre de su direccion ip
    ret = rrdtool.create(rutafinal,
                     "--start",'N',
                     "--step",'10',
                     "DS:CPUload:GAUGE:600:U:U",
                     "DS:RAMload:GAUGE:600:U:U",
                     "DS:DISKload:GAUGE:600:U:U",
                     "RRA:AVERAGE:0.5:1:24")
    if ret:
        print (rrdtool.error())


def actualizacionw(direccion,comunidad):  #Actualización para sistema windows
    rrdpath = '/home/gonzalo/PycharmProjects/Practica2/Principal/RRD/' #limites obtenidos de la datasheet de intel para el procesador i5 10400f
    limiteCPU = 100
    umbralCPU = 90
    limiteRAM = int(consultaSNMP(comunidad, direccion, "1.3.6.1.2.1.25.2.3.1.5.4"))
    umbralRAM = limiteRAM - limiteRAM / 10
    limitedisco = int(consultaSNMP(comunidad, direccion, "1.3.6.1.2.1.25.2.3.1.5.1"))
    umbraldisco = limitedisco - limitedisco / 10
    print("Los valores de umbral del cpu, ram y  disco son:\n" + str(umbralCPU) + "\n" + str(umbralRAM) + "\n" + str(umbraldisco))
    alertacpu = False
    alertaram = False
    alertadisk = False
    while 1:
        # carga_CPU = int(consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.25.3.3.1.2.196608'))
        carga_CPU = int(consultaSNMP('comunidadASR', '192.168.100.5', '1.3.6.1.2.1.25.3.3.1.2.9'))
        carga_RAM = int(consultaSNMP('comunidadASR', '192.168.100.5', '1.3.6.1.2.1.25.2.3.1.6.4'))
        carga_Disco = int(consultaSNMP('comunidadASR', '192.168.100.5', '1.3.6.1.2.1.25.2.3.1.6.1'))
        valor = "N:" + str(carga_CPU) + ":" + str(carga_RAM) + ":" + str(carga_Disco)
        nombreds = "-t CPUload:RAMload:DISKload"
        print(valor)
        rrdtool.update(rrdpath + 'trend.rrd', valor)
        rrdtool.dump(rrdpath + 'trend.rrd', 'trend.xml')
        if (carga_CPU >= umbralCPU) and (
                alertacpu == False):  # si toca el umbral y no se ha emitido una aleta previamente
            print("Alerta umbral excedido\nPreparando el mensaje")
            graph.graficaCPU(str(direccion), str(limiteCPU), str(umbralCPU), "CPU")
            Notify.send_alert_attached("Notificación sobrepaso de umbral limite CPU", "CPU")
            alertacpu = True  # Cambiamos la bandera a verdadero para no volver a enviar el mensaje.
            print("Mensaje enviado")

        if (carga_RAM >= umbralRAM) and (alertaram == False):
            print("Alerta umbral excedido\nPreparando el mensaje")
            graph.graficaCPU(str(direccion), str(limiteCPU), str(umbralCPU), "RAM")
            Notify.send_alert_attached("Notificación sobrepaso de umbral limite RAM", "RAM")
            alertaram = True  # Cambiamos la bandera a verdadero para no volver a enviar el mensaje.
            print("Mensaje enviado")

        if (carga_Disco >= umbraldisco) and (alertadisk == False):
            print("Alerta umbral excedido\nPreparando el mensaje")
            graph.graficaCPU(str(direccion), str(limiteCPU), str(umbralCPU), "DISK")
            Notify.send_alert_attached("Notificación sobrepaso de umbral limite del disco duro", "DISK")
            alertadisk = True  # Cambiamos la bandera a verdadero para no volver a enviar el mensaje.
            print("Mensaje enviado")
        time.sleep(1)

    if ret:
        print(rrdtool.error())
        time.sleep(300)

def actualizacionl(direccion,comunidad):#funcion actualización linux
    rrdpath = '/home/gonzalo/PycharmProjects/Practica2/Principal/RRD/' + direccion + ".rrd" #definimos la ruta de base de datos
    #definimos los umbrales como el 90 por ciento de capacidad de los diferentes perifericos
    limiteCPU = 100
    umbralCPU = 90
    limiteRAM = int(consultaSNMP(comunidad,direccion,"1.3.6.1.2.1.25.2.3.1.5.1"))
    umbralRAM = limiteRAM - limiteRAM/10
    limitedisco = int(consultaSNMP(comunidad,direccion,"1.3.6.1.2.1.25.2.3.1.5.36"))
    umbraldisco = limitedisco - limitedisco/10
    print("Los valores de umbral del cpu, ram y  disco son:\n"+str(umbralCPU)+"\n"+str(umbralRAM)+"\n"+str(umbraldisco))
    alertacpu = False
    alertaram = False
    alertadisk = False

    while 1:
        # carga_CPU = int(consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.25.3.3.1.2.196608'))
        carga_CPU = int(consultaSNMP(comunidad, direccion, '1.3.6.1.2.1.25.3.3.1.2.196608'))
        carga_RAM = int(consultaSNMP(comunidad, direccion, '1.3.6.1.2.1.25.2.3.1.6.1'))
        carga_Disco = int(consultaSNMP(comunidad, direccion, '1.3.6.1.2.1.25.2.3.1.6.36'))
        valor = "N:" + str(carga_CPU) + ":" + str(carga_RAM) + ":" + str(carga_Disco)
        print(valor)
        rrdtool.update(rrdpath, valor)
        rrdtool.dump(rrdpath, direccion + ".xml")
        if (carga_CPU >= umbralCPU)and(alertacpu == False): # si toca el umbral y no se ha emitido una aleta previamente
            print("Alerta umbral excedido\nPreparando el mensaje")
            graph.graficaCPU(str(direccion),str(limiteCPU),str(umbralCPU),"CPU")
            Notify.send_alert_attached("Notificación sobrepaso de umbral limite CPU","CPU")
            alertacpu = True #Cambiamos la bandera a verdadero para no volver a enviar el mensaje.
            print("Mensaje enviado")

        if (carga_RAM >= umbralRAM)and(alertaram == False):
            print("Alerta umbral excedido\nPreparando el mensaje")
            graph.graficaCPU(str(direccion), str(limiteCPU), str(umbralCPU), "RAM")
            Notify.send_alert_attached("Notificación sobrepaso de umbral limite RAM", "RAM")
            alertaram = True  # Cambiamos la bandera a verdadero para no volver a enviar el mensaje.
            print("Mensaje enviado")

        if (carga_Disco >= umbraldisco)and(alertadisk == False):
            print("Alerta umbral excedido\nPreparando el mensaje")
            graph.graficaCPU(str(direccion), str(limiteCPU), str(umbralCPU), "DISK")
            Notify.send_alert_attached("Notificación sobrepaso de umbral limite del disco duro", "DISK")
            alertadisk = True  # Cambiamos la bandera a verdadero para no volver a enviar el mensaje.
            print("Mensaje enviado")
        time.sleep(1)

    if ret:
        print(rrdtool.error())
        time.sleep(300)

if __name__ == "__main__":      #Desplegamos un menu para interactuar con el usuario
    inicio = False
    while 1:
        print("Monitor de recursos SNMP")
        print("Seleccione una opción: ")
        print("1) Agregar un dispositivo")
        # print("/n 2) Eliminar un dispositvo")
        a = int(input())
        print(a)

        if (a == 1 and inicio == False):  # Preguntamos la información del nuevo dispositivo
            print("Introduce la dirección IP del dispositivo:")
            direccionIP = input()
            print("Introduce el nombre de la comunidad:")
            comunidad = input()
            informacionsistema = consultaSNMP(comunidad, direccionIP, "1.3.6.1.2.1.1.1.0")
            print(informacionsistema)
            if (informacionsistema.find("Windows") != -1):  # Identificamos el sistema del dispositivo
                creacionrrd(direccionIP)  # Creamos la base de datos
                -_thread.start_new_thread(actualizacionw, (direccionIP, comunidad))
            else:
                print("\ncreando demonio para linux")
                creacionrrd(direccionIP) #Creamos la base de datos
                -_thread.start_new_thread(actualizacionl, (direccionIP, comunidad))



