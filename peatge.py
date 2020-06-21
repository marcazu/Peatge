# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 18:35:12 2020

@author: Marc.A.A
"""

import simpy
import random

""" ----------------------VARIABLES GLOBALS---------------------- """
 


""" ----------------------CODI---------------------- """



class Peatge(object):
    """ Un petge té un nombre concret de barreres per on poden pasar els cotxes"""
    maquinaPagament = 0
    def __init__(self,env, num_peatges, temps_pagament, f):
        self.env = env
        self.maquinaPagament = simpy.Resource(env, num_peatges)
        f.write("numero de peages activats %s \n" % (num_peatges))
        self.temps_pagament = temps_pagament
        self.f = f
    
    def pagar(self, numero, targeta,f):
         "Si es paga en targeta es realitza el pagemtn al instant"
         tempsPrevi = env.now
         factorHuma = random.randrange(10, 30)
         if(targeta == 0):
             f.write("El %s es prepara per fer pagament en efectiu \n" % (numero))
             yield self.env.timeout(TEMPS_PAGAMENT + factorHuma)         
         else:
             f.write("El %s es prepara per fer pagament en targeta \n" % (numero))
             yield self.env.timeout(TEMPS_PAGAMENT)
             tempsPagament = env.now-tempsPrevi 
             maquinaFalla = random.randrange(0, 4)
             if(maquinaFalla == 0):
                 "la maquina falla ha de venir un operari a arreglar la maquina"
                 f.write("El %s ha tingut un error al realitzar el pagament \n" % (numero))
                 f.write("Un operari està realitzant el pagament de cotxe %s \n" % (numero))
                 tempsPreviOperari = env.now
                 yield self.env.timeout(factorHuma)
                 f.write("l'operari ha realitzat el pagament del %s en %s segons \n" 
                       % (numero, env.now-tempsPreviOperari))
                 
         tempsPagament = env.now-tempsPrevi 
         f.write("El %s ha realitzat el pagament correctament en %s segons \n"
               % (numero, tempsPagament))
    
        

def cotxe(env, numero, peatg,f):
    targeta =  random.randrange(0, 2)
    f.write("El %s arriba a la cua del peatge a temps: %s. \n" % (numero, env.now))
    tempsInicial = env.now
    with peatg.maquinaPagament.request() as request:
        yield request         
        f.write("El %s ha fet %s segons de cua. \n" % (numero, env.now-tempsInicial))
        yield env.process(peatg.pagar(numero,targeta,f))
    f.write("El %s marxa del peatge a temps: %s, ha tardat %s en pasar el peatge \n"
          % (numero, env.now, env.now-tempsInicial))
    
def setUp(env, num_peatges, temps_pagament, temps_arribades,f):
    """crea un peatge amb un nonmbre concret de peatges, amb un temps de pagament
    i un temps entre arribades definit"""
    
    peatge = Peatge(env, num_peatges, temps_pagament,f)
    
    # Create 4 initial cotxes
    i = 0
    """
    for i in range(4):
        env.process(cotxe(env, "Cotxe %d" % i, peatge))
    # crea més cotxes mentres s'executa la simulació"""
    
    while True:
        try:
            "tarda entre 10 i 30 segons a crea un cotxe de forma aleatoria"
            
            yield env.timeout(temps_arribades)
            "yield env.timeout(random.randint(t_inter - 2, t_inter + 2))"
            i += 1
            env.process(cotxe(env, "Cotxe %d" % i, peatge,f))
        except:
            print("No fer ni cas a aquesta excepcio!!!")
  
imput = open("imput.txt","r")
NUM_PEATGES = int(imput.readline())
TEMPS_PAGAMENT = int(imput.readline())
TEMPS_SIMULACIO = int(imput.readline())
TEMPS_ARRIBADES = int(imput.readline())
imput.close()
f = open("output.txt", "w")
f.write("-----INICI DE LA SIMULACIO-----\n")
env = simpy.Environment()
p = env.process(setUp(env,NUM_PEATGES, TEMPS_PAGAMENT, TEMPS_ARRIBADES,f))
env.run(TEMPS_SIMULACIO)
f.write("-----FI DE LA SIMULACIO-----\n")
f.close()


    
