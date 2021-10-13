import sys
import rrdtool
from  Notify import send_alert_attached
import time

def graficaCPU(baserrd,capacidad, umbral,tipo):  #La función pide el nombre que se le va poner, el limite para la grafica y el valor del umbral y el tipo de dato a graficar
    rrdpath = '/home/gonzalo/PycharmProjects/Practica2/Principal/RRD/'
    imgpath = '/home/gonzalo/PycharmProjects/Practica2/Principal/IMG/'

    ultima_lectura = int(rrdtool.last(rrdpath + "trend.rrd"))  # Obtenemos el tiempo de la ultima lectura de la base de datos
    #
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 400
    ret = rrdtool.graphv(imgpath + tipo+".png",
                    "--start", str(tiempo_inicial),
                    "--end", str(tiempo_final),
                    "--vertical-label=Carga",
                    '--lower-limit', '0',
                    '--upper-limit', capacidad,
                    "--title=Uso del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales",
                    "DEF:cargaCPU=" + rrdpath + baserrd + ".rrd:" + tipo +"load:AVERAGE",

                    "VDEF:cargaMAXC=cargaCPU,MAXIMUM",
                    "VDEF:cargaMINC=cargaCPU,MINIMUM",
                    "VDEF:cargaSTDEVC=cargaCPU,STDEV",
                    "VDEF:cargaLASTC=cargaCPU,LAST",

                    "CDEF:umbral5C=cargaCPU,90,LT,0,cargaCPU,IF",
                    "AREA:cargaCPU#00FF00:Carga del CPU",
                    "AREA:umbral5C#FF9F00:Carga CPU mayor que 90",
                    "HRULE:90#FF0000:Umbral 1 - 5%",

                    "PRINT:cargaLASTC:%6.2lf",
                    "GPRINT:cargaMINC:%6.2lf %SMIN",
                    "GPRINT:cargaSTDEVC:%6.2lf %SSTDEV",
                    "GPRINT:cargaLASTC:%6.2lf %SLAST"

                    )




rrdpath = '/home/gonzalo/PycharmProjects/Practica2/Principal/RRD/'
imgpath = '/home/gonzalo/PycharmProjects/Practica2/Principal/IMG/'

ultima_lectura = int(rrdtool.last(rrdpath+"trend.rrd")) #Obtenemos el tiempo de la ultima lectura de la base de datos
print(ultima_lectura)
tiempo_final = ultima_lectura
tiempo_inicial = tiempo_final - 200

ret = rrdtool.graphv( imgpath+"deteccion.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Carga",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                    "--title=Uso del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales",

                    # "DEF:cargaCPU=" + rrdpath + nombre +".rrd"+":CPUload:AVERAGE",
                    # "DEF:cargaCPU=" + rrdpath + "trend.rrd:CPUload:AVERAGE",
                     "DEF:cargaCPU=" + rrdpath + "192.168.100.72.rrd:CPUload:AVERAGE",
                     "VDEF:cargaMAXC=cargaCPU,MAXIMUM",
                     "VDEF:cargaMINC=cargaCPU,MINIMUM",
                     "VDEF:cargaSTDEVC=cargaCPU,STDEV",
                     "VDEF:cargaLASTC=cargaCPU,LAST",


                     "CDEF:umbral5C=cargaCPU,10,LT,0,cargaCPU,IF",
                     "AREA:cargaCPU#00FF00:Carga del CPU",
                     "AREA:umbral5C#FF9F00:Carga CPU mayor que 5",
                     "HRULE:15#FF0000:Umbral 1 - 5%",


                     "PRINT:cargaLASTC:%6.2lf",
                     "GPRINT:cargaMINC:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEVC:%6.2lf %SSTDEV",
                     "GPRINT:cargaLASTC:%6.2lf %SLAST",


                      )


# ultimo_valor=float(ret['print[0]'])
# if ultimo_valor>4:
    # send_alert_attached("Sobrepasa Umbral línea base")
    # print("Sobrepasa Umbral línea base")