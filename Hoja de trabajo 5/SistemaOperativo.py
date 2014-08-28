# -*- coding: cp1252 -*-
#Universidad del Valle de Guatemala
#Jefferson Silva carné:12605
#Pablo Samayoa carné:12635
#sección: 20
#sistemOperativo.py
#programa principal simula la funcion de un cpu, donde el cpu corre cada proceso con una cantidad de ramrequerida
#y una cantidad de isntrucciones requerida del proceso.

import random
from math import sqrt
import simpy
import math


RANDOM_SEED = 300
NEW_CUSTOMERS = 100 # total numero de procesos
INTERVAL_CUSTOMERS = 1 #Generate new customers roughly every x seconds
CANTIDAD_RAM_CPU = 100 #cantidad ram cpu
CANTIDAD_INSTRUCCIONES_PROCESO = random.randint(1,10) #contiene cantidad de instrucciones de un proceso
ESPERAR_HABER_RAM = 300

CANTIDAD_RAM_PROCESO = random.randint(1,10) #contiene cantidad de ram a utilizar de un proceso

#crea procesos como necesitemos
def proceso(env, number, interval,counter,cpu_ram_total,waiting):
    """Source generates customers randomly"""
    
    for i in range(number):
        tiempo = env.now
        c = start(env, 'Proceso%02d' % i, counter, CANTIDAD_RAM_PROCESO,cpu_ram_total,tiempo,waiting) #crea proceso
        env.process(c)
        t = random.expovariate(1.0 / interval) #crear un numero randon distribucion exponencial 
        yield env.timeout(t) #espera un tiempo
        
#llega a start, donde decide si hay cantidad de ram suficiente para ser ejecutado
def start(env, name, interval,ram_proceso,cpu_ram_total,tiempo,waiting):    
        ram_proceso = random.randint(1,10) #conteiene la ram a utilizar de un proceso
        instruccion_proceso = random.randint(1,10) #instrucciones a ejectuar de nu proceso
        with cpu_ram_total.get(ram_proceso) as req: #pide utilizar cierta cantidad de ram al cpu
            yield req #espera 
            start=env.now
            print ('%s necesita cantidad de ram: %s  cantidad de instrucciones: %s camtidad de RAM actual : %.1f' % (name,ram_proceso,instruccion_proceso,cpu_ram_total.level))
        r = running(env,name,interval,ram_proceso,cpu_ram_total,instruccion_proceso,tiempo,waiting) #crea un proceso llamado runnig
        env.process(r)



           
#contiene la parte del cpu , donde ejecuta los procesos con sus instrucciones, donde inteneta acelerar             
def running(env, name, interval,ram_proceso,cpu_ram_total,instruccion_proceso,tiempo,waiting):
    global tiempofinal 
    global tiempo2
    global totalwait
    global suma
    suma = 0
    
    #se ejecuta mientras hayan instrucciones
    while instruccion_proceso > 0:
        siguiente = random.choice(['espera','siguiente']) #paso apra escoger el random si se ejecuta el proceso o no
        arrive = env.now #tomar tiempo
        with cpu.request() as reqcpu: #entra a cpu a ejecutar procesos
            yield reqcpu
            yield env.timeout(1)
            if instruccion_proceso > 3: #si hay mas de 3 instrucciones que le reste 3
                instruccion_proceso = instruccion_proceso - 3
                

                yield env.timeout(1)

                if siguiente == 'espera': #si despues de ejecutar sale esperar , le toca esperar al proceso hasta que salga siguiente
                    with waiting.request() as reqwait:
                        yield reqwait
                        yield env.timeout(10)
                        
                
            else:
                instruccion_proceso = 0
                

    #si no hay ram, liberar mas ram , cantidad de procesos utilizados 
    with cpu_ram_total.put(ram_proceso) as reqmem:
        yield reqmem
    wait = env.now - arrive
    totalwait = totalwait + wait #calcular tiempo total

    
    
    

    

# Setup and start the simulation
print('sIniciando simulacion')
random.seed(RANDOM_SEED)
env = simpy.Environment()
#cpu_ram = simpy.Container(env,CANTIDAD_RAM_PROCESO, init = CANTIDAD_RAM_PROCESO)
cpu_ram_total = simpy.Container(env,init = 100,capacity=100)
waiting = simpy.Resource(env, capacity=1)

# Start processes and run
counter = simpy.Resource(env, capacity=1) # recurso Resource
cpu = simpy.Resource(env, capacity=3) #crea cou con un procesador
totalwait = 0
env.process(proceso(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter,cpu_ram_total,waiting))
env.run()
print ('tiempo total de:  %s con un promedio de : %s' % (totalwait, totalwait/NEW_CUSTOMERS))



