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
TEMPS_PAGAMENT = 2 #temps que tarda en realitzar el pagametn un cotxe
TEMPS_ARRIBADES = 2 # Temps entre arribades de cotxes


class Peatge(object):
    """ Un petge té un nombre concret de barreres per on poden pasar els cotxes"""
    def __init__(self,env, num_peatges, temps_pagament):
        self.env = env
        self.machine = simpy.Resource(env,num_peatges)
        self.temps_pagament = temps_pagament
    
    def pagar(self, numero):
         yield self.env.timeout(TEMPS_PAGAMENT)
         print("cotxe % realitzant el pagament" % (numero))
        

def cotxe(env, numero, peatg):
    print("%s arriba al peatge en temps: %.2f. es disposa a fer cua" % (numero, env.now))
    with peatg.machine.request() as request:   
        yield request
         
    print("%s entra al peatge i realitza el pagament a temps: %.2f."(numero, env.now))
    yield env.process(peatg.pagar(numero))
    
    print("%s marxa del peatge a temps: %.2f." % (numero, env.now))
    
def setUp(env, num_peatges, temps_pagament, temps_arribades):
    """crea un peatge amb un nonmbre concret de peatges, amb un temps de pagament
    i un temps entre arribades definit"""
    
    peatge = Peatge(env, num_peatges, temps_pagament)
    
    # Create 4 initial cotxes
    for i in range(4):
        env.process(cotxe(env, "Cotxe %d" % i, peatge))
    # crea més cotxes mentres s'executa la simulació
    
    while True:
        try:
            yield env.timeout(1)
            "yield env.timeout(random.randint(t_inter - 2, t_inter + 2))"
            i += 1
            env.process(cotxe(env, "Cotxe %d" % i, peatge))
        except:
            print("algo pasa")
  
    
print("Peatge")
env = simpy.Environment()
p = env.process(setUp(env,NUM_PEATGES,TEMPS_PAGAMENT,TEMPS_ARRIBADES))
env.run(until=20)
    
