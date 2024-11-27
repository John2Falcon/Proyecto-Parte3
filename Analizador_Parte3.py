def comparar_versiones(archivo_viejo, archivo_nuevo):
    """
    Compara dos versiones de un archivo y cuenta las líneas añadidas, borradas y modificadas.

    Args:
        archivo_viejo (str): Ruta al archivo de la versión anterior.
        archivo_nuevo (str): Ruta al archivo de la nueva versión.
    
    Returns:
        dict: Diccionario con los contadores de líneas añadidas, borradas y modificadas.
    """
    with open(archivo_viejo, 'r', encoding='utf-8') as f_viejo, open(archivo_nuevo, 'r', encoding='utf-8') as f_nuevo:
        lineas_viejas = f_viejo.readlines()
        lineas_nuevas = f_nuevo.readlines()

    # Contadores
    lineas_añadidas = 0
    lineas_borradas = 0
    lineas_modificadas = 0

    # Índices para recorrer las líneas de ambos archivos
    i = 0
    j = 0

    while i < len(lineas_viejas) or j < len(lineas_nuevas):
        if i < len(lineas_viejas) and j < len(lineas_nuevas) and lineas_viejas[i].strip() == lineas_nuevas[j].strip():
            # Línea común, no se cuenta como cambio
            i += 1
            j += 1
        elif j < len(lineas_nuevas) and (i >= len(lineas_viejas) or lineas_viejas[i].strip() != lineas_nuevas[j].strip()):
            # Línea añadida
            lineas_añadidas += 1
            j += 1
        elif i < len(lineas_viejas) and (j >= len(lineas_nuevas) or lineas_viejas[i].strip() != lineas_nuevas[j].strip()):
            # Línea borrada
            lineas_borradas += 1
            i += 1

    # Comparar líneas en común para modificaciones
    i = 0
    j = 0
    while i < len(lineas_viejas) and j < len(lineas_nuevas):
        if lineas_viejas[i].strip() != lineas_nuevas[j].strip():
            lineas_modificadas += 1
        i += 1
        j += 1

    return {
        'añadidas': lineas_añadidas,
        'borradas': lineas_borradas,
        'modificadas': lineas_modificadas
    }

def formatear_lineas_largas(lineas):
    """
    Formatea las líneas que superan los 80 caracteres, dividiéndolas en varias líneas.

    Args:
        lineas (list): Lista de líneas del archivo.
    
    Returns:
        list: Lista de líneas formateadas.
    """
    lineas_formateadas = []
    for linea in lineas:
        while len(linea) > 80:
            lineas_formateadas.append(linea[:80])
            linea = linea[80:]
        lineas_formateadas.append(linea)
    return lineas_formateadas

def imprimir_informe(cambios):
    """
    Imprime el informe de cambios.

    Args:
        cambios (dict): Diccionario con los contadores de cambios.
    """
    print("-" * 60)
    print(f"CAMBIOS EN LAS VERSIONES:")
    print(f"Líneas añadidas: {cambios['añadidas']}")
    print(f"Líneas borradas: {cambios['borradas']}")
    print(f"Líneas modificadas: {cambios['modificadas']}")
    print("-" * 60)

if __name__ == "__main__":
    archivo_viejo = './version_antigua.py'  # Ruta del archivo antiguo
    archivo_nuevo = './version_nueva.py'   # Ruta del archivo nuevo

    # Leer y formatear las líneas si son demasiado largas
    with open(archivo_viejo, 'r', encoding='utf-8') as f:
        lineas_viejas = f.readlines()
    with open(archivo_nuevo, 'r', encoding='utf-8') as f:
        lineas_nuevas = f.readlines()

    lineas_viejas_formateadas = formatear_lineas_largas(lineas_viejas)
    lineas_nuevas_formateadas = formatear_lineas_largas(lineas_nuevas)

    cambios = comparar_versiones(archivo_viejo, archivo_nuevo)
    imprimir_informe(cambios)
