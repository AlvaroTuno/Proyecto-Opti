# Ideas de que se tiene que hacer
# Crear un archivo para que lo pueda leer el LpSolve. (Tiene que salir un archivo .lp)
# Pedirle al usuario que tipo de dificultad (pequeño, mediano o grande)
# Generar para ambos tipos de costos (a y c) a la vez

#Librerias 
import random
#from lpsolve import *

#Creamos los datos iniciales

#Fijo
Diametros={ 
    "D1": {"diametro": 50, "flujoMax": 353, "costos": {"a":16, "c":90}},
    "D3": {"diametro": 100, "flujoMax": 1414, "costos": {"a":24, "c":145}},
    "D5": {"diametro": 150, "flujoMax": 3181, "costos": {"a":32, "c":210}}
           }

#Variables
Tamano={
    "Pequeno":{"plantas": (1,2), "tanques": (5,10), "nodosTrans": (5,10), "nodosFinal": (10,20)},
    "Mediano":{"plantas": (3,4), "tanques": (10,20), "nodosTrans": (10,20), "nodosFinal": (20,50)},
    "Grande":{"plantas": (5,7), "tanques": (20,50), "nodosTrans": (25,50), "nodosFinal": (50,100)} }

#Restricciones

#Declaracion tipo de variable


#achivoInstancias
def archivoInstancias(instancia):
    match instancia:
        case 1:
            pass #placeholder. eliminar dps de poner codigo.
        case 2:
            pass #placeholder. eliminar dps de poner codigo.
        case 3:
            pass #placeholder. eliminar dps de poner codigo.
    
def generadordemanda():
    demanda = random.randint(40,100)
    return demanda
def generadorcostos():
    costo = random.randint(2,8)
    return costo


#generador de instancias
def generadorInstancias(instancia, cantidad):
    match instancia:
        case 1:
            eleccion=Tamano["Pequeno"]
        case 2:
            eleccion=Tamano["Mediano"]
        case 3:
            eleccion=Tamano["Grande"]

    #el azar
    nPlantas=random.randint(eleccion["plantas"][0],eleccion["plantas"][1]+1)
    nTanques=random.randint(eleccion["tanques"][0],eleccion["tanques"][1]+1)
    nNodosTrans=random.randint(eleccion["nodosTrans"][0],eleccion["nodosTrans"][1]+1)
    nNodosFinal=random.randint(eleccion["nodosFinal"][0],eleccion["nodosFinal"][1]+1)

    #rellenar los parametros

    Nodos={}
    Plantas={}
    Tanques={}
    NodosTrans={}
    NodosFinal={}
    for n in range(nPlantas):
        Plantas["p" + str(n)]=""
    Nodos["plantas"]=Plantas
    
    for n in range(nTanques):
        Tanques["t" + str(n)]=""
    Nodos["tanques"]=Tanques
    
    for n in range(nNodosTrans):
        NodosTrans["ct" + str(n)]={"demanda": generadordemanda() }
    Nodos["nodosTrans"]=NodosTrans
    
    for n in range(nNodosFinal):
        NodosFinal["cf" + str(n)]={"demanda": generadordemanda() }
    Nodos["nodosFinal"]=NodosFinal
    
    Arcos=[]
    for n in Plantas.keys():
        for i in Tanques.keys():
            Arcos.append({"origen": n, "destino": i, "costo": generadorcostos()})
    
    for n in Tanques.keys():
        for i in NodosTrans.keys():
            Arcos.append({"origen": n, "destino": i, "costo": generadorcostos()})

    for n in NodosTrans.keys():
        for i in NodosFinal.keys():
            Arcos.append({"origen": n, "destino": i, "costo": generadorcostos()})


    print(Nodos)
    print(Arcos)
    #archivoInstancias(instancia)
    

def generadorarchivoa(instancia,Nodos):
    archivo = f"instancia_aleatoria_a.lp"
    file = open(archivo, 'w')
    file.write("/* archivo generado automáticamente*/") 
    Funcion_obj=""
    #for i in 
    archivo.write("min: ;")#funcion objetivo
    file.close()

    
def generadorArchivoC(instancia, Nodos):
    FO = "min: pija * xija + cija * fija ;"
    restricciones = """ 
    """
    rds = """
    xija es binaria
    bin xij
    fija es >= 0
    int fij 
    """ 

    archivo = f"instancia_aleatoria_C.lp"

   #with  openarchivoo, 'w' as file:)    #    fileo.write("/* archivogeneradoo automáticamente */"
   #     file.write(f"{FO}\n{restricciones}\n{rds}"))



#Pedirle informacion al usuario
#llamar a la funcion generadorInstancias -> archivoInstancias

print("Ingrese el numero para seleccionar el tamaño del mapa que quiera crear")
instancia=int(input("1. Pequeño \n2. Mediano\n3. Grande\n"))
cantidadM=int(input("¿Cuantos mapas quiere generar?\n"))
generadorInstancias(instancia, cantidadM)

