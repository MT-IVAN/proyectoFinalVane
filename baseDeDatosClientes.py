from tabulate import tabulate

#Headers que voy a usar para imprimi mis datos ordenados
dbUsersHeaders = ["Tipo de identificación", "Número de identificación", "Nombre"]
dbCuentasHeaders = ["Tipo de identifiación(Client)", "Número de identificación(Client)", "Tipo de cuenta", "Número de cuenta", "Monto"]
headerError = ["ERROR"]
#DataBase. con Info de los clientes
dbUsers = [
    ["CC", "123", "Ivan Eraso"],
    ["NIT", "509", "Vane Diaz"],
    ["CC", "234", "Vane sth"],
    ]

#DataBase. con Info de las cuentas 
dbCuentas = [
    ["CC", "123", "AHORROS","543", 1],
    ["CC", "234", "AHORROS", "970", 2],
    ["CC", "234", "CORRIENTE", "970", 3],
    ["CC", "123", "CORRIENTE", "970", 4],
    ["NIT", "509", "AHORROS", "659", 5],
    ["NIT", "509", "CORRIENTE", "970", 6],
    ]    


#Valido que el valor ingresado no este vacio, si no, vuelvo a pedir el dato
#param mensaje: es el mensaje que voy a mostrar al usuario cuando pida el dato
def obtenerNuevoDatoString(mensaje):
    nuevoDato = ""
    #Con len cuento la cantidad de caracteres del nuevoDato
    while  len(nuevoDato) < 1 :
        nuevoDato = input(mensaje).strip()
    return nuevoDato

def obtenerNuevoDatoNumber(mensaje):
    nuevoDato = -1
    while  nuevoDato < 0 :
        #intenta resolver el codigo dentro de el, si se genera un error en el procesamient del codigo el except sera ejecutado
        #Uso try and except para controlar errores en el codigo.
        try: #si input = "23" -> 23
            nuevoDato = int(input(mensaje).strip())
        except:
            print("El valor ingresado debe ser numerico")
            nuevoDato
    return nuevoDato

def obtenerNuevoDatoTipoId(mensaje):
    tipos = ["CC","CE","NIT"] #arreglo con tipos de identificacion valido
    nuevoDato = ""
    while  not nuevoDato in tipos: #nuevoDato = CC
        print("Los valores validos de tipo de indentificacion son: CC,CE,NIT")
        nuevoDato = input(mensaje).strip() #CC
    return nuevoDato

def obtenerNuevoDatoTipoCuenta(mensaje):
    tipos = ["CORRIENTE","AHORROS"]
    nuevoDato = ""
    while  not nuevoDato in tipos:
        print("Los valores validos de tipo de indentificacion son: CORRIENTE,AHORROS")
        nuevoDato = input(mensaje).strip()
    return nuevoDato

#Muestra todos los usuarios
def mostrarTodosLosClientes():
    #Tabulate recibe PARAMS: data, headers(opciones), tablefmt
    print(tabulate(dbUsers, headers=dbUsersHeaders, tablefmt="fancy_grid"))

#Obtener cliente por numero de identificacion y tipo de documento
def obtenerClientePorCedula(tipo, num):
    for cliente in dbUsers:
        if cliente[0] == tipo and cliente[1] == num:
            return cliente
    return "El cliente no existe"
   
#Obtener cliente por numero de cuenta
def obtenerClientePorNumCuenta(tipoCuenta, numCuenta):
    for cuenta in dbCuentas:
        if cuenta[2]==tipoCuenta and cuenta[3] == numCuenta:
            #si entra a este if, entonces encontramos el numero de cuenta
            #ahora tengo que rescatar el usuario que posee esa cuenta
            clienteBuscado = obtenerClientePorCedula(cuenta[0], cuenta[1])
            return clienteBuscado        
    return "La cuenta ingresada no se encuentra registrada"

#Obtiene todas las cuentas de un cliente
def obtenerCuentasDelCliente(tipo,num):
    clienteBuscado = obtenerClientePorCedula(tipo, num)
    ## si el dato que retorna obtenerClientePorCedula() es string, significa que no existe
    if type(clienteBuscado) is str:
        return "El cliente que se ingreso no existe en nuestra base de datos"
    else:
        #entonces Existe porque el valor retorna no es un string, si no, una lista! list
        #data almacenara las cuentas del cliente en caso de que existan! si no existe se mostrara
        #un mensaje diciendo que el cliente no tiene cuentas!
        data = []
        for cuenta in dbCuentas:
            if(cuenta[0]==tipo and cuenta[1]==num):
                data.append(cuenta)
        if len(data)==0:
            return "El cliente no tiene cuentas asociadas"
        else:
            return data

#Agregar un cliente
def agregarCliente(tipo, num, nombre):
    cliente = obtenerClientePorCedula(tipo, num)
    #si el tipo de la variable cliente NO es string(str), entonces el cliente existe y no es
    #agregado a nuestra base de datos
    if type(cliente) is not str:
        return "El cliente no se pudo agregar, ya existe en nuestra base de datos!"
    else:
        nuevoCliente =[] 
        nuevoCliente.append(tipo)
        nuevoCliente.append(num)
        nuevoCliente.append(nombre)
        #Agrego mi nuevo cliente a mi base de datos de clientes (matriz || list || arrreglo)
        dbUsers.append(nuevoCliente)
        #Retorno el cliente nuevo
        return nuevoCliente

def agregarCuentaACliente(tipoCedula, numCedula, tipoCuenta, numCuenta, monto):
    if obtenerClientePorCedula(tipoCedula,numCedula) == "El cliente no existe":
        return "El cliente al que se le desea agregar una cuenta no se encuentra registrado en nuestra base de datos"
    #preparamos el nuevo registro con toda la información necesaria
    nuevaCuenta = []
    nuevaCuenta.append(tipoCedula)
    nuevaCuenta.append(numCedula)
    nuevaCuenta.append(tipoCuenta)
    nuevaCuenta.append(numCuenta)
    nuevaCuenta.append(monto)
    #agregamos el nuevo registro (nuevaCuenta) a nuestra base de datos llamada dbCuentas
    dbCuentas.append(nuevaCuenta)
    return nuevaCuenta

#Eliminar un cliente por tipo y numero de cedula y las cuentas que tenga asociadas
def eliminarCliente(tipo, num):
    try:
        #Elimino al cliente
        clienteAEliminar = obtenerClientePorCedula(tipo,num)
        #Si la variable clienteAElminar es un String, entonces el pop de la siguente linea
        #generar un error haciendo que el except se ejecute
        #Si el cliente fue encontrado, será eliminado con la funcion pop
        dbUsers.pop(dbUsers.index(clienteAEliminar))
        #Elimino las cuentas asociadas al cliente
        #el index lo resto en -1 porque si encuentro la cuenta y la elimino, las posiciones donde esta 
        #la información serán diferentes
        index = 0
        #uso el while porque el recalcula la longitud de dbCuentas en cada iteración
        #Si uso un for el va a estallar porque la longitud de dbCuentas será siempre la misma
        # a pesar de que cambie debio a que estoy eliminando elementos de dbCuentas
        #y genera un IndexError
        while index < len(dbCuentas):
            if(dbCuentas[index][0] ==tipo and dbCuentas[index][1] ==num ):
                dbCuentas.pop(index)
                index -= 1
            index +=1 
        return clienteAEliminar
    except:
        print("El cliente que se desea eliminar no esta registrado en la base de datos")

def buscarClientePorRangoEnSalario(minSalario, maxSalario):
    clientes = {} #Diccionario clave : valor clientes.append("HappyCode!")
    for cuenta in dbCuentas:
        if cuenta[4] >= minSalario and cuenta[4]<=maxSalario:
            cliente = obtenerClientePorCedula(cuenta[0], cuenta[1])
            #si el tipo de dato de cliente es String significa que el cliente fue encontrado
            if type(cliente) != "str":
                cedula = cliente[0]+cliente[1]
                clientes[cedula] = cliente[2]
    if len(clientes)==0:
        return "No existen clientes en el rango salarial dado"
    else:
        return clientes

#modificar nombre cliente
def modificarNombreCliente(tipo, num, nombre):
    modificado = False
    for cliente in dbUsers:
        if cliente[0]==tipo and cliente[1]==num:
            cliente[2]=nombre
            modificado = True
            break
    if modificado:
        return obtenerClientePorCedula(tipo, num)
    else:    
        return "El cliente no existe en nuestra base de datos"
    
#modificar monto de la cuenta del cliente
def modificarMontoDeLaCuenta(tipoCuenta, numCuenta, monto):
    modificado = False
    auxCuenta = []
    for cuenta in dbCuentas:
        if cuenta[2]==tipoCuenta and cuenta[3]==numCuenta:
            cuenta[4]=monto
            modificado = True
            auxCuenta = cuenta
            break
    if modificado:
        return auxCuenta
    else:    
        return "La cuenta no existe en nuestra base de datos"

#imprime en pantalla la data en una tabla o el error indicando que el registro no se encontro 
#recibe la data que va a mostrar y el tipo que puede ser cliente o cuenta
def mostrarDataOError(data, tipo, mensaje="notAMessage"):
    head = []
    dataForTable = []
    if type(data) is str:
        arr = []
        arr2 = []
        arr.append(data)
        arr2.append(arr)
        print(tabulate(arr2, headers=headerError, tablefmt="fancy_grid"))      
    else:
        #se hace la siguiente validacion porque la data puede llegar en una dos dimensiones
        if type(data[0]) is list:
            dataForTable = data
        else:
            dataForTable.append(data)

        if tipo == "cuenta":
            head = dbCuentasHeaders
        elif tipo == "cliente":
            head = dbUsersHeaders
        if mensaje != "notAMessage":
            print(mensaje)
        print(tabulate(dataForTable, headers=head, tablefmt="fancy_grid"))      

while True:
    print("---------------------------------------")
    print("Menú principal:")
    print("\t1 Mostrar todos los clientes")
    print("\t2 Buscar cliente por Cedula")
    print("\t3 Buscar cliente por N. de cuenta")
    print("\t4 Mostrar cuentas asociadas a un cliente")
    print("\t5 Agregar cliente")
    print("\t6 Agregar cuenta a un cliente")
    print("\t7 Eliminar cliente")
    print("\t8 Buscar cliente entre rango salarial")
    print("\t9 Modificar el nombre de un cliente")
    print("\t10 Modificar el monto de una cuenta")
    print("\t0 Finalizar programa")
    print("---------------------------------------")
	
    opcion = int(input("Que acción desea ejecutar: "))


    if opcion == 0:
        break
    elif opcion == 1:
        mostrarTodosLosClientes()
    elif opcion ==2:
        tipo = obtenerNuevoDatoTipoId("Ingrese el tipo de cédula del cliente: ")
        num = obtenerNuevoDatoString("Ingrese el número de cédula del cliente: ")
        clienteBuscado = obtenerClientePorCedula(tipo, num)
        mostrarDataOError(clienteBuscado, "cliente")
    elif opcion ==3:
        tipo = obtenerNuevoDatoTipoCuenta("Ingrese el tipo de cuenta del cliente: ")
        num = obtenerNuevoDatoString("Ingrese el número de cuenta del cliente: ")
        cuentaBuscada= obtenerClientePorNumCuenta(tipo,num)
        mostrarDataOError(cuentaBuscada, "cliente")
    elif opcion ==4:
        tipo = obtenerNuevoDatoTipoId("Ingrese el tipo de cédula del cliente: ")
        num = obtenerNuevoDatoString("Ingrese el número de cédula del cliente: ")
        cuentas = obtenerCuentasDelCliente(tipo,num)
        mostrarDataOError( cuentas,"cuenta")
    elif opcion ==5:
        tipo = obtenerNuevoDatoTipoId("Ingrese el tipo de cédula del cliente que desea agregar: ")
        num = obtenerNuevoDatoString("Ingrese el número de cédula del cliente que desea agregar: ")
        nombre = obtenerNuevoDatoString("Ingrese el nombre del cliente que desea agregar: ")
        nuevoCliente = agregarCliente(tipo,num,nombre)
        mostrarDataOError(nuevoCliente, "cliente")
        print("Cliente agregado satisfactoriamente")
    elif opcion ==6:
        tipo = obtenerNuevoDatoTipoId("Ingrese el tipo de cédula del nuevo cliente: ")
        num = obtenerNuevoDatoString("Ingrese el número de cédula del nuevo cliente: ")
        tipoCuenta = obtenerNuevoDatoTipoCuenta("Ingrese el tipo de cuenta del nuevo cliente: ")
        numCuenta = obtenerNuevoDatoString("Ingrese el número de cuenta del nuevo cliente: ")
        monto = obtenerNuevoDatoNumber("Ingrese el monto con el que cargará la nueva cuenta: ")
        nuevaCuenta = agregarCuentaACliente(tipo, num, tipoCuenta,numCuenta,monto)
        mostrarDataOError(nuevaCuenta, "cuenta")
        print("Cuenta agregada satisfactoriamente")
    elif opcion == 7:
        tipo = obtenerNuevoDatoTipoId("Ingrese el tipo de cédula del nuevo cliente: ")
        num = obtenerNuevoDatoString("Ingrese el número de cédula del nuevo cliente: ")
        clienteEliminado = eliminarCliente(tipo, num)
        mostrarDataOError(clienteEliminado,"cliente" )
        print("El cliente y todas sus cuentas fueron eliminadas correctamente")
    elif opcion == 8:
        montoMin = obtenerNuevoDatoNumber("Ingrese el valor mínimo: ")
        montoMax = obtenerNuevoDatoNumber("Ingrese el valor máximo: ")
        clientes = buscarClientePorRangoEnSalario(montoMin, montoMax)
        data = []
        data.append(clientes.keys())
        data.append(clientes.values())
        print(tabulate(data, tablefmt="fancy_grid")) 
    elif opcion == 9:
        tipo = obtenerNuevoDatoTipoId("Ingrese el tipo de cédula del cliente que desea modificar: ")
        num = obtenerNuevoDatoString("Ingrese el número de cédula del cliente que desea modificar: ")
        nombre = obtenerNuevoDatoString("Ingrese el nombre del cliente que desea modificar: ")
        clienteModificado = modificarNombreCliente(tipo, num, nombre)
        mostrarDataOError(clienteModificado, "cliente")
    elif opcion == 10:
        tipoCuenta = obtenerNuevoDatoTipoCuenta("Ingrese el tipo de cuenta del cliente: ")
        numCuenta = obtenerNuevoDatoString("Ingrese el número de cuenta del cliente: ")
        monto = obtenerNuevoDatoNumber("Ingrese el nuevo monto de la cuenta: ")
        cuentaModificada = modificarMontoDeLaCuenta(tipoCuenta,numCuenta,monto)
        mostrarDataOError(cuentaModificada, "cuenta")

    else:
        print("Opcion no válida")