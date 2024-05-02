from utilities import borrarPantalla, gotoxy
import time
#from cedula_ecuatoriana import CedulaEcuatorina
class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc   
class Valida:
    def solo_numeros(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil)            
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor

    def solo_letras(self,mensajeError,col,fil): 
        while True:
            gotoxy(col,fil)
            valor = str(input())
            if valor.isalpha():
                break
            else:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor

    def solo_decimales(self,mensajeError,col,fil):
        while True:
            try:
                valor = input()
                valor = float(valor)
                if valor % 1 != 0:
                    break
                else:
                    gotoxy(col,fil);print("Ingresa un porcentaje")
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor
    
    def cedula(self, mensajeError, col, fil):
        while True:
            gotoxy(col,fil)
            cedula = str(input())
            codigo_cedula = tuple(str(i).zfill(2) for i in range(1, 25))
            if len(cedula) == 10 and cedula.startswith(codigo_cedula) and cedula.isdigit():
                # Validación del dígito verificador
                coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
                suma = 0
                for i in range(len(coeficientes)):
                    digito = int(cedula[i]) * coeficientes[i]
                    suma += digito if digito < 10 else digito - 9
                verificador_calculado = (10 - (suma % 10)) % 10
                verificador = int(cedula[-1])
                if verificador_calculado != verificador:
                    return False
                break
            else:
                gotoxy(col, fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col, fil);print(" " * 20)
        return cedula
        
    def validar_entero_and_decimal(self,mensaje_error, col, fil):
        while True:
            gotoxy(col,fil)
            entrada = input()
            if entrada.replace(".", "", 1).isdigit(): 
                break
            else:
                gotoxy(col, fil);print(mensaje_error)
                time.sleep(1)
                gotoxy(col, fil);print(" " * 20)
        return float(entrada)
    

class otra:
    pass    















