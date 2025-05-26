#Librerias 
import random

#Declaramos los datos del problema
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


def generadordemanda():
    demanda = random.randint(40,100)
    return demanda
def generadorcostos():
    costo = random.randint(2,8)
    return costo

def generadorNodos(instancia):
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
    
    #definimos parametros
    Nodos={}
    Plantas={}
    Tanques={}
    NodosTrans={}
    NodosFinal={}

    #Generamos los nodos
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
    
    #Generamos los arcos
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


    #Retorna los nodos y arcos generados
    #print(Nodos)
    #print("\n bleeeeeeeeh \n") Revisar lo que se genero
    #print(Arcos)
    return Nodos, Arcos


def generadorarchivoa(tamanio, Nodos, Arcos, indice):
    archivo = f"instancia_aleatoria_a_"+tamanio+str(indice)+".lp"
    with open(archivo, 'w') as file:
        file.write("/* Archivo generado automáticamente */\n")
        file.write("\n/* Funcion Objetivo*/\n")
        file.write("min: ")# 1. Función objetivo
        #Primera sumatoria
        for arco in Arcos:
            for d in ["D1", "D3", "D5"]:
                costo = Diametros[d]["costos"]["a"] + arco["costo"]
                var = f"x_{arco['origen']}_{arco['destino']}_{d}"
                file.write(f"{costo}*{var} + ")
        
        #De momento esto se ve asi: 
        #Z=18*x_p0_t0_D1 + ..... +
        #Segunda Sumatoria
        # Segunda sumatoria (costo de transporte)
        for arco in Arcos:
            costo_transporte = arco["costo"]
            fvar = f"f_{arco['origen']}_{arco['destino']}"
            file.write(f"{costo_transporte}*{fvar} + ")
        file.write("0;\n\n") #Se termina de generar la funcion objetivo
        
        #Restricciones
        file.write("\n/* Restricciones*/\n")

        file.write("/*Capacidad de flujo*/\n")
        for arco in Arcos:# 2. Restricciones de capacidad de flujo
            fvar = f"f_{arco['origen']}_{arco['destino']}"
            expresion = f"{fvar}"
            for d in ["D1", "D3", "D5"]:
                capacidad = Diametros[d]["flujoMax"]
                var_bin = f"x_{arco['origen']}_{arco['destino']}_{d}"
                expresion += f" - {capacidad}*{var_bin}"
            file.write(expresion + " <= 0;\n")

        file.write("\n/*Conservación de flujo*/\n")
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

        file.write("\n/* Restricción de selección única de diámetro por arco */\n")
        for arco in Arcos:
            expresion = ""
            for d in ["D1", "D3", "D5"]:
                var_bin = f"x_{arco['origen']}_{arco['destino']}_{d}"
                expresion += f"{var_bin} + "
            file.write(expresion[:-3] + " <= 1;\n")

        file.write("\n/*Declaracion de variables*/\n")
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

def generadorarchivoc(tamanio, Nodos, Arcos, indice):

    archivo = f"instancia_aleatoria_c_"+tamanio+str(indice)+".lp"
    with open(archivo, 'w') as file:
        file.write("/* Archivo generado automáticamente */\n")
        file.write("\n/* Funcion Objetivo*/\n")
        file.write("min: ")# 1. Función objetivo
        for arco in Arcos:
            for d in ["D1", "D3", "D5"]:
                costo = Diametros[d]["costos"]["c"] + arco["costo"]
                var = f"x_{arco['origen']}_{arco['destino']}_{d}"
                file.write(f"{costo}*{var} + ")
        
        
        #De momento esto se ve asi: 
        #Z=18*x_p0_t0_D1 + ..... +
        #Segunda Sumatoria
        # Segunda sumatoria (costo de transporte)
        for arco in Arcos:
            costo_transporte = arco["costo"]
            fvar = f"f_{arco['origen']}_{arco['destino']}"
            file.write(f"{costo_transporte}*{fvar} + ")
        file.write("0;\n\n") #Se termina de generar la funcion objetivo
        
        #Restricciones
        file.write("\n/* Restricciones*/\n")

        file.write("/*Capacidad de flujo*/\n")    
        for arco in Arcos:# 2. Restricciones de capacidad de flujo
            fvar = f"f_{arco['origen']}_{arco['destino']}"
            expresion = f"{fvar}"
            for d in ["D1", "D3", "D5"]:
                capacidad = Diametros[d]["flujoMax"]
                var_bin = f"x_{arco['origen']}_{arco['destino']}_{d}"
                expresion += f" - {capacidad}*{var_bin}"
            file.write(expresion + " <= 0;\n")

        file.write("\n/*Conservación de flujo*/\n")
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

        file.write("\n/* Restricción de selección única de diámetro por arco */\n")
        for arco in Arcos:
            expresion = ""
            for d in ["D1", "D3", "D5"]:
                var_bin = f"x_{arco['origen']}_{arco['destino']}_{d}"
                expresion += f"{var_bin} + "
            file.write(expresion[:-3] + " <= 1;\n")


        file.write("\n/*Declaracion de variables*/\n")
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

        i = 0 #esto es pa que se escriba bn en el archivo noma XD
        file.write("int ")# 5. Declaración de variables de flujo
        for arco in Arcos:
            fvar = f"f_{arco['origen']}_{arco['destino']}"
            if i == 0:
                    file.write(f"{fvar}")
            else:
                    file.write(f",{fvar}")
            i+=1
        file.write(";\n")

#-------------------------Datos Usuario-------------------------#
flag=1
while flag:
    print("Ingrese el numero para seleccionar el tamaño del mapa que quiera crear")
    tamanioInt=int(input("1. Pequeño \n2. Mediano\n3. Grande\n"))
    cantidadM=int(input("¿Cuantos mapas quiere generar?\n"))
    
    match tamanioInt:
        case 1:
            tamanioStr="Pequeno"
        case 2:
            tamanioStr="Mediano"
        case 3:
            tamanioStr="Grande"

    a =(generadorNodos(tamanioInt))
    for i in range(cantidadM):
        generadorarchivoa(tamanioStr,a[0],a[1],i+1)
        generadorarchivoc(tamanioStr,a[0],a[1],i+1)
    
    Resp=int(input("¿Quiere Seguir creando instancias?\n1. Si\n2. No\n"))
    if flag!= Resp:
        flag=0
