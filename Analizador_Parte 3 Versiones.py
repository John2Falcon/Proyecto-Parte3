from difflib import unified_diff

class ComparadorDeVersiones:
    def __init__(self, archivo_anterior, archivo_nuevo):
        self.archivo_anterior = archivo_anterior
        self.archivo_nuevo = archivo_nuevo
        self.lineas_anteriores = []
        self.lineas_nuevas = []
        self.lineas_iguales = 0
        self.lineas_añadidas = 0
        self.lineas_borradas = 0

    def leer_archivo(self, ruta):
        """
        Lee un archivo y retorna sus líneas formateadas (80 caracteres máximo).
        """
        lineas = []
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    linea = linea.rstrip()
                    if len(linea) > 80:
                        lineas.extend(self.dividir_linea(linea))
                    else:
                        lineas.append(linea)
        except FileNotFoundError:
            print(f"Error: El archivo {ruta} no existe.")
        return lineas

    def dividir_linea(self, linea):
        """
        Divide una línea en múltiples líneas si excede los 80 caracteres.
        """
        return [linea[i:i+80] for i in range(0, len(linea), 80)]

    def comparar_versiones(self):
        """
        Compara las líneas entre la versión anterior y la nueva.
        """
        self.lineas_anteriores = self.leer_archivo(self.archivo_anterior)
        self.lineas_nuevas = self.leer_archivo(self.archivo_nuevo)

        for diff in unified_diff(self.lineas_anteriores, self.lineas_nuevas, lineterm=''):
            if diff.startswith('+ ') and not diff.startswith('+++'):
                self.lineas_añadidas += 1
                print(f"{diff[2:]}  # LÍNEA NUEVA")
            elif diff.startswith('- ') and not diff.startswith('---'):
                self.lineas_borradas += 1
                print(f"{diff[2:]}  # LÍNEA BORRADA")
            elif not diff.startswith(('+++', '---', '@@')):
                self.lineas_iguales += 1

    def generar_informe(self):
        """
        Imprime un informe del análisis de versiones.
        """
        print("\n--- Informe de Cambios ---")
        print(f"Líneas iguales: {self.lineas_iguales}")
        print(f"Líneas añadidas: {self.lineas_añadidas}")
        print(f"Líneas borradas: {self.lineas_borradas}")
        print("-------------------------")

if __name__ == "__main__":
    archivo_anterior = './version_anterior.py'
    archivo_nuevo = './version_nueva.py'
    comparador = ComparadorDeVersiones(archivo_anterior, archivo_nuevo)
    comparador.comparar_versiones()
    comparador.generar_informe()
