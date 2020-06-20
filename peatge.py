# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 18:35:12 2020

@author: Marc
"""

import simpy
import random

NUM_PEATGES = 2 # numero de peatges actius
NUM_RODES = [2,4,8]
PREU_RODES = [6,7,10]
TEMPS_PAGAMENT = 15 #temps que la maquina tarda en realitzar un pagament en segons
TEMPS_ARRIBADES = 0.5 # Temps entre arribades de cotxes


class Peatge(object):
    """ Un petge té un nombre concret de barreres per on poden pasar els cotxes"""
    maquinaPagament = 0
    def __init__(self,env, num_peatges, temps_pagament):
        self.env = env
        self.maquinaPagament = simpy.Resource(env, num_peatges)
        print ("numerp de peages")
        print (num_peatges)
        self.temps_pagament = temps_pagament
    
    def pagar(self, numero):
         print("El %s acaba la cua i comença a realitzar el pagametn a temps: %s." % (numero, env.now))
         #temps que pot tardar una persona a realitzar el pagament
         factorHuma = random.randrange(10, 30) 
         tempsPrevi = env.now
         yield self.env.timeout(TEMPS_PAGAMENT + factorHuma)
         tempsPagament = env.now-tempsPrevi
         print("El %s ha realitzat el pagament en %s segons" % (numero,tempsPagament))
        

def cotxe(env, numero, peatg):
    tempsIni = env.now
    print("El %s arriba a la cua del peatge a temps: %s." % (numero, env.now))
    with peatg.maquinaPagament.request() as request:
        result = yield request
         

    yield env.process(peatg.pagar(numero))
    tempsTotal = env.now-tempsIni
    print("%s marxa del peatge a temps: %s, ha tardat %s segons en completar tot el proces" % (numero, env.now, tempsTotal))
    
def setUp(env, num_peatges, temps_pagament, temps_arribades):
    """crea un peatge amb un nonmbre concret de peatges, amb un temps de pagament
    i un temps entre arribades definit"""
    
    peatge = Peatge(env, num_peatges, temps_pagament)
    
    # Create 4 initial cotxes
    i = 0
    """
    for i in range(4):
        env.process(cotxe(env, "Cotxe %d" % i, peatge))
    # crea més cotxes mentres s'executa la simulació"""
    
    while True:
        try:
            "tarda entre 10 i 30 segons a crea un cotxe de forma aleatoria"
            tempsEntreCotxes = random.randrange(5, 15)
            yield env.timeout(tempsEntreCotxes)
            "yield env.timeout(random.randint(t_inter - 2, t_inter + 2))"
            i += 1
            env.process(cotxe(env, "Cotxe %d" % i, peatge))
        except:
            print("linia 51 setUp falla!!!")
  
    
print("Peatge")
env = simpy.Environment()
p = env.process(setUp(env,NUM_PEATGES, TEMPS_PAGAMENT, TEMPS_ARRIBADES))
env.run(100)


    
