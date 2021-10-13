import time
import rrdtool
from getSNMP import consultaSNMP
rrdpath = '/home/gonzalo/PycharmProjects/Practica2/Principal/RRD/'
carga_CPU = 0
cargaRAM = 0
carga_CPU = 0

while 1:
    # carga_CPU = int(consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.25.3.3.1.2.196608'))
    carga_CPU = int(consultaSNMP('comunidadASR', '192.168.100.5', '1.3.6.1.2.1.25.3.3.1.2.9'))
    carga_RAM = int(consultaSNMP('comunidadASR', '192.168.100.5', '1.3.6.1.2.1.25.2.3.1.6.4'))
    carga_Disco = int(consultaSNMP('comunidadASR', '192.168.100.5', '1.3.6.1.2.1.25.2.3.1.6.1'))
    valor = "N:" + str(carga_CPU) + ":" + str(carga_RAM) + ":" + str(carga_Disco)
    nombreds = "-t CPUload:RAMload:DISKload"
    print (valor)
    rrdtool.update(rrdpath+'trend.rrd', valor)
    # rrdtool.update(rrdpath + '192.168.100.72.rrd', valor)
    rrdtool.dump(rrdpath+'trend.rrd','trend.xml')
    # rrdtool.dump(rrdpath + '192.168.100.72.rrd', 'trend2.xml')
    time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)
