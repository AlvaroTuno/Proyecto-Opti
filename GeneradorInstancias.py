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
    return Nodos, Arcos
    #archivoInstancias(instancia)
    
def generadorarchivoa(instancia, Nodos, Arcos):
    archivo = f"instancia_aleatoria_a.lp"
    with open(archivo, 'w') as file:
        file.write("/* Archivo generado automáticamente */\n")

        file.write("min: ")# 1. Función objetivo
        for arco in Arcos:
            for d in ["D1", "D3", "D5"]:
                costo = Diametros[d]["costos"]["a"] + arco["costo"]
                var = f"x_{arco['origen']}_{arco['destino']}_{d}"
                file.write(f"{costo}*{var} + ")
        file.write("0;\n\n") 

        for arco in Arcos:# 2. Restricciones de capacidad de flujo
            fvar = f"f_{arco['origen']}_{arco['destino']}"
            expresion = f"{fvar}"
            for d in ["D1", "D3", "D5"]:
                capacidad = Diametros[d]["flujoMax"]
                var_bin = f"x_{arco['origen']}_{arco['destino']}_{d}"
                expresion += f" - {capacidad}*{var_bin}"
            file.write(expresion + " <= 0;\n")

        for nodo_tipo, grupo in Nodos.items():# 3. Conservación de flujo
            for nodo, data in grupo.items():
                if nodo_tipo == "plantas":
                    for arco in Arcos:
                        if arco['origen'] == nodo:
                            file.write(f"f_{nodo}_{arco['destino']} + ")
                    file.write("0 >= 0;\n")
                elif nodo_tipo == "tanques" or nodo_tipo == "nodosTrans":
                    for arco in Arcos:
                        if arco['destino'] == nodo:
                            file.write(f"f_{arco['origen']}_{nodo} + ")
                    for arco in Arcos:
                        if arco['origen'] == nodo:
                            file.write(f"- f_{nodo}_{arco['destino']} ")
                    file.write("= 0;\n")
                elif nodo_tipo == "nodosFinal":
                    demanda = data["demanda"]
                    for arco in Arcos:
                        if arco['destino'] == nodo:
                            file.write(f"f_{arco['origen']}_{nodo} + ")
                    file.write(f"0 = {demanda};\n")

        file.write("\nbin ")# 4. Declaración de variables binarias
        i = 0
        for arco in Arcos:
            for d in ["D1", "D3", "D5"]:
                var = f"x_{arco['origen']}_{arco['destino']}_{d}"
                if i == 0:
                    file.write(f"{var}")
                else:
                    file.write(f",{var}")
                i+=1
        file.write(";\n")

        i=0
        file.write("int ")# 5. Declaración de variables de flujo
        for arco in Arcos:
            fvar = f"f_{arco['origen']}_{arco['destino']}"
            if i == 0:
                    file.write(f"{fvar}")
            else:
                    file.write(f",{fvar}")
            i+=1
        file.write(";\n")

def generadorarchivoc(instancia, Nodos, Arcos):
    archivo = f"instancia_aleatoria_c.lp"
    with open(archivo, 'w') as file:
        file.write("/* Archivo generado automáticamente */\n")

        file.write("min: ")# 1. Función objetivo
        for arco in Arcos:
            for d in ["D1", "D3", "D5"]:
                costo = Diametros[d]["costos"]["c"] + arco["costo"]
                var = f"x_{arco['origen']}_{arco['destino']}_{d}"
                file.write(f"{costo}*{var} + ")
        file.write("0;\n\n") 

        for arco in Arcos:# 2. Restricciones de capacidad de flujo
            fvar = f"f_{arco['origen']}_{arco['destino']}"
            expresion = f"{fvar}"
            for d in ["D1", "D3", "D5"]:
                capacidad = Diametros[d]["flujoMax"]
                var_bin = f"x_{arco['origen']}_{arco['destino']}_{d}"
                expresion += f" - {capacidad}*{var_bin}"
            file.write(expresion + " <= 0;\n")

        for nodo_tipo, grupo in Nodos.items():# 3. Conservación de flujo
            for nodo, data in grupo.items():
                if nodo_tipo == "plantas":
                    for arco in Arcos:
                        if arco['origen'] == nodo:
                            file.write(f"f_{nodo}_{arco['destino']} + ")
                    file.write("0 >= 0;\n")
                elif nodo_tipo == "tanques" or nodo_tipo == "nodosTrans":
                    for arco in Arcos:
                        if arco['destino'] == nodo:
                            file.write(f"f_{arco['origen']}_{nodo} + ")
                    for arco in Arcos:
                        if arco['origen'] == nodo:
                            file.write(f"- f_{nodo}_{arco['destino']} ")
                    file.write("= 0;\n")
                elif nodo_tipo == "nodosFinal":
                    demanda = data["demanda"]
                    for arco in Arcos:
                        if arco['destino'] == nodo:
                            file.write(f"f_{arco['origen']}_{nodo} + ")
                    file.write(f"0 = {demanda};\n")

        file.write("\nbin ")# 4. Declaración de variables binarias
        i = 0
        for arco in Arcos:
            for d in ["D1", "D3", "D5"]:
                var = f"x_{arco['origen']}_{arco['destino']}_{d}"
                if i == 0:
                    file.write(f"{var}")
                else:
                    file.write(f",{var}")
                i+=1
        file.write(";\n")

        i=0#esto es pa que se escriba bn en el archivo noma XD
        file.write("int ")# 5. Declaración de variables de flujo
        for arco in Arcos:
            fvar = f"f_{arco['origen']}_{arco['destino']}"
            if i == 0:
                    file.write(f"{fvar}")
            else:
                    file.write(f",{fvar}")
            i+=1
        file.write(";\n")
#Pedirle informacion al usuario
#llamar a la funcion generadorInstancias -> archivoInstancias

print("Ingrese el numero para seleccionar el tamaño del mapa que quiera crear")
instancia=int(input("1. Pequeño \n2. Mediano\n3. Grande\n"))
cantidadM=int(input("¿Cuantos mapas quiere generar?\n"))
a =(generadorInstancias(instancia, cantidadM))
generadorarchivoa(instancia,a[0],a[1])
generadorarchivoc(instancia,a[0],a[1])
