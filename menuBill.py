from components import Menu, Valida
from utilities import borrarPantalla, gotoxy, reset_color, red_color, green_color, yellow_color, blue_color, purple_color, cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient, VipClient
from product  import Product
from sales import Sale
from iCrud import ICrud
import datetime
import time, os
from functools import reduce
from functools import wraps


path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
#Menu de Clientes
class CrudClients(ICrud):

    def create(self):
        validar = Valida()
        json_file = JsonFile(path+'/archivos/clients.json')
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registrar cliente")
        gotoxy(1,4);print(green_color+"Ingrese su dni: "+reset_color)

        while True:
            dni = validar.cedula("Cédula inválida",1,5)
            data = json_file.find("dni",dni)
            if not data:
                break
            else:
                gotoxy(1, 5);print("El dni ingresado, no está registrado en el registro civil nacional.")
                time.sleep(10)
                gotoxy(1, 5);print(" " * 35)
        
        gotoxy(18, 4);print("Ingrese su nombre: ")
        nombre = validar.solo_letras("Nombre inválido",18,5)

        gotoxy(38, 4);print("Ingrese su apellido: ")
        apellido = validar.solo_letras("Apellido inválido",45,5)

        gotoxy(60, 4);print("Que tipo de cliente es?")
        gotoxy(60, 5);print("Cliente Regular (1) o Cliente VIP (2), Elija su opción: ")
        while True:
            opc = validar.solo_numeros("Numero inválido", 60,6)
            if int(opc) == 1:
                gotoxy(120, 4);print("Tiene su tarjeta activada?")
                gotoxy(120, 5);print("SI (s) o No(n), Elija su opción: ")
                while True:
                    opc2 = validar.solo_letras("Opción inválida",120,6)
                    if opc2.lower() == "s":
                        client = RegularClient(nombre, apellido, dni, True)
                        break
                    elif opc2.lower() == "n":
                        client = RegularClient(nombre, apellido, dni, False)
                        break
                    else:
                        gotoxy(90, 6);print("Opcion inválida")
                        time.sleep(1)
                        gotoxy(90,6);print(" "*20)
                break
            elif int(opc) == 2:
                client = VipClient(nombre, apellido, dni)
                break
            else:
                gotoxy(60, 6);print("Numero inválido")
                time.sleep(10)
                gotoxy(60,6);print(" "*15)

        json_file = JsonFile(path+'/archivos/clients.json')
        data = json_file.read()
        jsonClient = client.getJson()
        data.append(jsonClient)
        json_file.save(data)
        gotoxy(38, 8);print(green_color+"Cliente registrado con éxito!"+reset_color)
        time.sleep(10)  

    def update(self):

        #Modifica un atributo
        def cambiarAtributo(client, atributo, nuevo):
            if client["dni"] == dni:
                client[atributo] = nuevo
            return client

        validar = Valida()
        json_file = JsonFile(path+'/archivos/clients.json')
        borrarPantalla()
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Actualizar cliente")
        gotoxy(1,4);print(green_color+"Ingresa dni del cliente a modificar: "+reset_color)
        while True:
            dni = validar.cedula("Cédula inválida",1,5)
            data = json_file.find("dni",dni)
            if data:
                data = data[0]
                gotoxy(1,6);print("El usuario a modificar es: ")
                gotoxy(1,7);print(f"NOMBRE: {data["nombre"]} - APELLIDO: {data["apellido"]} - VALOR: {data["valor"]}")
                gotoxy(1, 8); print(f"Que campo deseas cambiar: Nombre(1) - Apellido(2) - Valor(3)")
                while True:

                    opc = validar.solo_numeros("Opción incorrecta",1,9)

                    if int(opc) == 1:
                        gotoxy(1,11);print("Ingresa el nuevo nombre: ")
                        nombre = validar.solo_letras("Nombre inválido",1,12)
                        clients = json_file.read()
                        clientsModificada =  list(map(lambda client: cambiarAtributo(client, "nombre", nombre), clients))
                        json_file.save(clientsModificada)
                        gotoxy(1,14);print("Cliente modificado con éxito!")
                        break

                    elif int(opc) == 2:
                        gotoxy(1,11);print("Ingresa el nuevo apellido: ")
                        apellido = validar.solo_letras("Apellido invalido",1,12)
                        clients = json_file.read()
                        clientsModificada = list(map(lambda client: cambiarAtributo(client, "apellido", apellido), clients))
                        json_file.save(clientsModificada)
                        gotoxy(1,14);print("Cliente modificado con éxito")
                        break

                    elif int(opc) == 3:
                        #pendiente
                        clients = json_file.read()
                        if data["valor"] == 0 or data["valor"]%1 != 0:
                            gotoxy(1,11);print("El usuario en un cliente regular, ingrese su nuevo porciento de descuento: ")
                            descuento = validar.solo_decimales("No es un porcentaje", 1, 12)
                            clientsModificada = list(map(lambda client: cambiarAtributo(client, "valor", descuento), clients))
                            json_file.save(clientsModificada)
                            gotoxy(1, 14);print("Valor actualizado con éxito!")

                        elif data["valor"] > 0 and data["valor"]%1 == 0:
                            gotoxy(1,11);print("El usuario es un cliente VIP, ingrese su nuevo valor de limite: ")
                            limite = validar.solo_numeros("Ingresa un numero entero", 1, 12)
                            clientsModificada = list(map(lambda client: cambiarAtributo(client, "valor", int(limite)), clients))
                            json_file.save(clientsModificada)
                            gotoxy(1, 14);print("Valor actualizado con éxito!")

                        else:
                            pass
                    
                        break
                    else:
                        gotoxy(1,9);print("Opción incorrecta")
                        time.sleep(1)
                        gotoxy(1, 9);print(" " * 35)
                break

            else:   
                gotoxy(1, 5);print("El usuario a modificar no existe")
                time.sleep(1)
                gotoxy(1, 5);print(" " * 35)

        time.sleep(10)

    def delete(self):
        validar = Valida()
        json_file = JsonFile(path+'/archivos/clients.json')
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Eliminar cliente")
        gotoxy(1,4);print(green_color+"Ingresa dni del cliente a eliminar: "+reset_color)

        while True:
            dni = validar.cedula("Cédula inválida",1,5)
            data = json_file.find("dni",dni)
            if data:
                clients = json_file.read()
                dataFiltrer = [client for client in clients if client["dni"] != dni]
                break
            else:
                gotoxy(1, 5);print("El usuario no existe")
                time.sleep(1)
                gotoxy(1, 5);print(" " * 35)

        json_file.save(dataFiltrer)
        gotoxy(20, 8);print(green_color+"Cliente eliminado con éxito!"+reset_color)
        time.sleep(10)

    def consult(self):
        validar = Valida()
        json_file = JsonFile(path+'/archivos/clients.json')
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Consulta de clientes"+reset_color)
        gotoxy(1, 4);print("Ver todos los clientes(1) -  Ver cliente por dni(2), elija su opción: ")

        while True:
            opc = validar.solo_numeros("Opción incorrecta",1,5)
            if int(opc) == 1:
                datas = json_file.read()
                i = 7
                # Inicializa la lista de valores de clientes
                valores_clientes = []
                for client in datas:
                    gotoxy(1,i);print(f"ID: {client['dni']} - NOMBRE: {client['nombre']} - APELLIDO: {client['apellido']} - VALOR: {client['valor']}")
                    # Agrega el valor del cliente a la lista
                    valores_clientes.append(client['valor'])
                    i += 1
                # Calcula la suma, máximo y mínimo de los valores de los clientes
                suma_clientes = sum(valores_clientes)
                max_cliente = max(valores_clientes)
                min_cliente = min(valores_clientes)
                # Imprime la información de suma, máximo y mínimo
                gotoxy(1,i+1);print(f"Suma de los valores de los clientes: {suma_clientes}")
                gotoxy(1,i+2);print(f"Valor máximo de los clientes: {max_cliente}")
                gotoxy(1,i+3);print(f"Valor mínimo de los clientes: {min_cliente}")
                print("---Presione s para regresar---")
                user_input = input()
                if user_input.lower() == 's':
                    return
            
            elif int(opc) == 2:
                while True:
                    gotoxy(1,6);print(green_color+"Ingrese el dni del cliente: "+reset_color)
                    dni = validar.cedula("Cédula inválida",1,7)
                    data = json_file.find("dni",dni)
                    if data:
                        client = data[0]
                        gotoxy(1,9);print(f"ID: {client['dni']} - NOMBRE: {client['nombre']} - APELLIDO: {client['apellido']} - VALOR: {client['valor']}")
                        
                        break
                    else:
                        gotoxy(1, 7);print("El usuario no existe")
                        time.sleep(1)
                        gotoxy(1, 7);print(" " * 35)
                    while True:
                        user_input = input("Press 's' para regresar")
                        if user_input.lower() == 's':
                            return
                        break
            else:
                gotoxy(1, 5);print("Opción incorrecta")
                time.sleep(0)
                gotoxy(1, 5);print(" " * 35)


def with_json_file(path):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            json_file = JsonFile(path)
            return func(self, json_file, *args, **kwargs)
        return wrapper
    return decorator

class CrudProducts(ICrud):
    @with_json_file(path+'/archivos/products.json')
    def create(self, json_file):
        validar = Valida()
        borrarPantalla()
        datas = json_file.read()
        numId = datas[-1]["id"]+1
        print('\033c', end='')
        gotoxy(1,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registrar producto"+reset_color)
        gotoxy(1,4);print("Ingresa el nombre del producto:")
        description = validar.solo_letras("Nombre inválido", 1, 5)
        gotoxy(35, 4);print("Ingresa el precio del producto: ")
        precio = validar.validar_entero_and_decimal("Precio inválido", 35, 5)
        gotoxy(70, 4);print("Ingresa el stock del producto: ")
        stock = validar.solo_numeros("Stock inválido", 70, 5)
        stock = int(stock)
        datas = json_file.read()
        product = Product(numId, description, precio, stock)
        productJson = product.getJson()
        datas.append(productJson)
        json_file.save(datas)
        gotoxy(20, 7);print("Producto registrado con éxito!")
        time.sleep(5)

    def update(self):

        def cambiarAtributoProduct(product, atributo, nuevo):
            if product["id"] == int(id):
                product[atributo] = nuevo
            return product
            
        validar = Valida()
        json_file = JsonFile(path+'/archivos/products.json')
        print('\033c', end='')
        gotoxy(1,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Actualizar producto"+reset_color)
        gotoxy(1, 4);print(green_color+"Ingresa el id del producto a modificar: "+reset_color)

        while True:
            id = validar.solo_numeros("Id inválido", 1, 5)
            data = json_file.find("id", int(id))
            if data:
                data = data[0]
                gotoxy(1,7);print("El producto a modificar es: ")
                gotoxy(1,8);print(f"ID: {data["id"]} - DESCRIPCION: {data["descripcion"]} - PRECIO: {data["precio"]} - STOCK: {data["stock"]}")
                gotoxy(1,9);print(f"Que campo deseas cambiar: Descripcion(1) - Precio(2) - Stock(3), elija su opción")
                while True:
                    opc = validar.solo_numeros("Opción incorrecta", 1, 10)
                    if int(opc) == 1:
                        gotoxy(1,12);print("Ingresa el nuevo nombre del producto: ")
                        nombre_product = validar.solo_letras("Nombre inválido", 1, 13)
                        products = json_file.read()
                        productsModificado = list(map(lambda product: cambiarAtributoProduct(product, "descripcion", nombre_product), products))
                        json_file.save(productsModificado)
                        gotoxy(1, 15);print("Producto modificado con éxito!")
                        break

                    elif int(opc) == 2:
                        gotoxy(1,12);print("Ingresa el nuevo precio del producto: ")
                        precio_product = validar.validar_entero_and_decimal("Precio inválido", 1, 13)
                        products = json_file.read()
                        productsModificado = list(map(lambda product: cambiarAtributoProduct(product, "precio", precio_product), products))
                        json_file.save(productsModificado)
                        gotoxy(1, 15);print("Producto modificado con éxito!")
                        break
        
                    elif int(opc) == 3:
                        gotoxy(1,12);print("Ingresa el nuevo stock del producto: ")
                        stock_product = validar.solo_numeros("Stock inválido", 1, 13)
                        products = json_file.read()
                        productsModificado = list(map(lambda product: cambiarAtributoProduct(product, "stock", int(stock_product)), products))
                        json_file.save(productsModificado)
                        gotoxy(1, 15);print("Producto modificado con éxito!")
                        break

                    else:
                        gotoxy(1, 10);print("Opción incorrecta")
                        time.sleep(1)
                        gotoxy(1, 10);print(" "*35)

                break
            else:
                gotoxy(1, 5);print("El producto a modificar no existe")
                time.sleep(1)
                gotoxy(1, 5);print(" " * 35)

        time.sleep(4)
        
    def delete(self):
        validar = Valida()
        json_file = JsonFile(path+'/archivos/products.json')
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Eliminar productos"+reset_color)
        gotoxy(1,4);print(green_color+"Ingresa id del producto: "+reset_color)

        while True:
            id = validar.solo_numeros("Id inválido", 1, 5)
            id = int(id)
            data = json_file.find("id", id)
            if data:
                products = json_file.read()
                dataFilter = [product for product in products if product["id"] != id]
                gotoxy(1,7);print("El producto fué eliminado con éxito!")
                break
            else:
                gotoxy(1, 5);print("El producto no existe")
                time.sleep(1)
                gotoxy(1, 5);print(" " * 35)

        json_file.save(dataFilter)
        time.sleep(4)

    def consult(self):
        validar = Valida()
        json_file = JsonFile(path+'/archivos/products.json')
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Consulta de productos"+reset_color)
        gotoxy(1, 4);print("Ver todos los productos(1) -  Ver producto por id(2), elija su opción")

        while True:
            opc = validar.solo_numeros("Opción incorrecta", 1, 5)

            if int(opc) == 1:
                datas = json_file.read()
                i = 7
                valores_producto = []
                for product in datas:
                    gotoxy(1,i);print(f"ID: {product['id']} - NOMBRE: {product['descripcion']} - PRECIO: {product['precio']} - STOCK: {product['stock']}")
                    valores_producto.append(product['stock'])
                    i += 1
                #Calcula suma, max, min
                suma_product = sum(valores_producto)
                max_product = max(valores_producto)
                min_product = min(valores_producto)
                #Imprimir info
                gotoxy(1, i+1);print(f"Suma de todos los stocks de los productos: {suma_product}")
                gotoxy(1, i+2);print(f"Max de todos los stocks de los productos: {max_product}")
                gotoxy(1, i+3);print(f"Min de todos los stocks de los productos: {min_product}")
                break
            elif int(opc) == 2:
                while True:
                    gotoxy(1,6);print(green_color+"Ingrese el id del producto: "+reset_color)
                    id = validar.solo_numeros("Id inválido", 1, 7)
                    data = json_file.find("id", int(id))
                    if data:
                        producto = data[0]
                        gotoxy(1,8);print(f"ID: {producto["id"]} - NOMBRE: {producto["descripcion"]} - PRECIO: {producto["precio"]} - STOCK: {producto["stock"]}")
                        break
                    else:
                        gotoxy(1,7);print("El producto no existe!")
                        time.sleep(1)
                        gotoxy(1,7);print(" "*35)
                break
            else:
                gotoxy(1, 5);print("Opción incorrecta")
                time.sleep(1)
                gotoxy(1, 5);print(" " * 35)

        time.sleep(10)


class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"],client["dni"], card=True)  
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
                
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print(" Venta Grabada satisfactoriamente "+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print(" Venta Cancelada "+reset_color)    
        time.sleep(2)    
    

    def update(self):

        def cambiarAtributoClient(client, atributo, nuevo):
            if client["factura"] == num_factura:
                client[atributo] = nuevo
            return client

        validar = Valida()
        json_file = JsonFile(path+'/archivos/invoices.json')
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90)
        gotoxy(30,2);print(yellow_color+"Actualización de Venta"+reset_color)
        gotoxy(2,4);print(green_color+"Ingrese el número de factura a modificar: "+reset_color)
        while True:
            num_factura = int(validar.solo_numeros("Factura inválida",2,5))
            data = json_file.find("factura",num_factura)
            if data:
                data = data[0]
                gotoxy(30,7);print("La factura es: ")
                gotoxy(2,8);print("Cabezera de factura: ")
                gotoxy(2,9);print(f"FACTURA: {data["factura"]} - DNI DE CLIENTE: {data["dni_de_cliente"]} - CLIENTE: {data["cliente"]} - SUBTOTAL: {data["subtotal"]} - DESCUENTO: {data["descuento"]} - IVA: {data["iva"]} - TOTAL: {data["total"]}")
                gotoxy(30,10);print("Productos comprados en la factura: ")
                productos_comprados = data["detalle"]; i=11
                for product in productos_comprados:
                    gotoxy(2,i);print(f"ID: {product["id"]} - PRODUCTO: {product["poducto"]} - PRECIO: {product["precio"]} - CANTIDAD: {product["cantidad"]}")
                    i += 1
                
                gotoxy(2,i+1);print("Que deseas cambiar de la factura? Cambiar cliente(1) o modificar los productos(2): ")
                while True:
                    opc = validar.solo_numeros("Opción incorrecta",2,i+2)
                    if int(opc) == 1:

                        json_file_client = JsonFile(path+'/archivos/clients.json') 
                        gotoxy(2,i+3);print(green_color+"Ingresa dni del cliente a reemplazar: "+reset_color)
                        while True:
                            client_dni = validar.cedula("Cédula inválida",2,i+4)
                            client_nuevo = json_file_client.find("dni",client_dni)
                            if client_nuevo:
                                client_nuevo = client_nuevo[0]
                                client_nuevo_nombre = f"{client_nuevo["nombre"]} {client_nuevo["apellido"]}"
                                clients = json_file.read()
                                clients_modificado = list(map(lambda client: cambiarAtributoClient(client, "cliente", client_nuevo_nombre), clients))
                                json_file.save(clients_modificado)
                                break
                            else:
                                gotoxy(2,i+4);print("No existe el cliente")
                                time.sleep(1)
                                gotoxy(2,i+4);print(" "*35)
                        break

                    elif int(opc) == 2:
                        gotoxy(2,i+3);print("Que deseas hacer? Añadir un producto(1) - Eliminar un producto?(2) : ")
                        while True:
                            opc2 = int(validar.solo_numeros("Opción inválida",2,i+4))
                            if opc2 == 1:
                                json_file_product = JsonFile(path+'/archivos/products.json')
                                index = 0
                                datas = json_file.read()
                                for obj in datas:
                                    if obj["factura"] == num_factura:
                                        index = datas.index(obj)

                                data = json_file.find("factura",num_factura)
                                data = data[0]
                                gotoxy(2,i+5);print("Ingresa el id del producto a agregar: ")
                                while True:
                                    id_product = int(validar.solo_numeros("Id inválido",2,i+6))
                                    data_product = json_file_product.find("id",id_product)
                                    if data_product:
                                        data_product = data_product[0]
                                        break
                                    else:
                                        gotoxy(2,i+6);print("El producto no existe")
                                        time.sleep(1)
                                        gotoxy(2,i+6);print(" "*35)
                                json_file_client = JsonFile(path+'/archivos/clients.json')
                                data_client = json_file_client.find("dni",data["dni_de_cliente"])
                                data_client = data_client[0]
                                client = RegularClient(data_client["nombre"],data_client["apellido"],data_client["dni"], True)
                                sale = Sale(client)
                                product_nuevo = Product(data_product["id"],data_product["descripcion"],data_product["precio"],data_product["stock"])
                                for p in data["detalle"]:
                                    product = Product(p["id"],p["poducto"],p["precio"],p["stock"])
                                    sale.add_detail(product,p["cantidad"])
                                gotoxy(2,i+7);print("Ingresa la cantidad para el producto: ")
                                num_cantidad = validar.solo_numeros("Cantidad inválida",2,i+8)
                                sale.add_detail(product_nuevo,int(num_cantidad))
                                sale_modificada = sale.getJson()
                                sale_modificada["factura"] = data["factura"]
                                invoices = json_file.read()
                                invoices[index] = sale_modificada
                                json_file.save(invoices)
                                break
                            elif opc2 == 2:
                                indice = 0
                                datas = json_file.read()
                                for obj in datas:
                                    if obj["factura"] == num_factura:
                                        indice = datas.index(obj)

                                gotoxy(2,i+5);print("Ingresa el id del producto a eliminar: ")
                                data_detalle = data["detalle"]
                                producto_eliminar = {}
                                while True:
                                    id_product = validar.solo_numeros("Id inválido",2,i+6)
                                    producto_encontrado = False
                                    for producto in data_detalle:
                                        if producto["id"] == int(id_product):
                                            producto_encontrado = True
                                            producto_eliminar = producto
                                            break
                                    if producto_encontrado:
                                        break
                                    else:
                                        gotoxy(2,i+6);print("El producto no existe")
                                        time.sleep(1)
                                        gotoxy(2,i+6);print(" "*30)
                                
                                data_detalle_modificado = [item for item in data_detalle if item["id"] != producto_eliminar["id"]]
                                json_file_client = JsonFile(path+'/archivos/clients.json')
                                data_client = json_file_client.find("dni",data["dni_de_cliente"])
                                data_client = data_client[0]
                                client = RegularClient(data_client["nombre"],data_client["apellido"],data_client["dni"], True)
                                sale = Sale(client)
                                for p in data_detalle_modificado:
                                    product = Product(p["id"],p["poducto"],p["precio"],p["stock"])
                                    sale.add_detail(product,p["cantidad"])
                                sale_modificada = sale.getJson()
                                sale_modificada["factura"] = data["factura"]
                                invoices = json_file.read()
                                invoices[indice] = sale_modificada
                                json_file.save(invoices)
                                break
                            else:
                                gotoxy(2,i+4);print("Opción inválida")
                                time.sleep(1)
                                gotoxy(2,i+4);print(" "*35)
                        break

                    else:
                        gotoxy(2,i+2);print("Opción incorrecta")
                        time.sleep(1)
                        gotoxy(2,i+2);print(" " * 35)
                break
            else:
                gotoxy(2,5);print("La factura no existe")
                time.sleep(1)
                gotoxy(1, 5);print(" " * 35)
        time.sleep(5)


    def delete(self):      
        validar = Valida()
        json_file = JsonFile(path+'/archivos/invoices.json')
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90)
        gotoxy(30,2);print(green_color+"Eliminar una Venta"+reset_color)
        gotoxy(2,3);print("Ingrese el número de la factura a eliminar: ")
        while True:
            num_factura = int(validar.solo_numeros("Número inválido",2,4))
            data = json_file.find("factura",num_factura)
            if data:
                data = data[0]
                invoices = json_file.read()
                invoices_modificado = [item for item in invoices if item["factura"] != num_factura]
                json_file.save(invoices_modificado)
                break
            else:
                gotoxy(2,4);print("La factura no existe")
                time.sleep(1)
                gotoxy(2,4);print(" "*30)
        gotoxy(30,6);print("Factura eliminada correctamente!")
        time.sleep(4)

    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x=input("presione una tecla para continuar...")    

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturación",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":  
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()
            client = CrudClients()    
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                client.create()
            elif opc1 == "2":
                client.update()
            elif opc1 == "3":
                client.delete()
            elif opc1 == "4":
                client.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            products = CrudProducts()
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                products.create()
            elif opc2 == "2":
                products.update()
            elif opc2 == "3":
                products.delete()
            elif opc2 == "4":
                products.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()   
            
                time.sleep(2)
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

