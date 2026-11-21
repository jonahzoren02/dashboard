import re
import unicodedata
import pandas as pd
import numpy as np


def crear_grupo_producto(texto):
    if pd.isna(texto):
        return ""

    # Convertir a mayúsculas y quitar tildes (ej. BETAÍNA -> BETAINA)
    texto = str(texto).upper()
    texto = "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

    # Eliminar todo lo que esté entre paréntesis: (2.5-5 KG), (10 G), (CAJA X 12...), (MUESTRA)
    texto = re.sub(r"\([^)]*\)", " ", texto)

    # Eliminar textos basura o notas internas específicas de tu inventario
    texto = re.sub(r"\bCODIGO NO JALA\b", " ", texto)
    texto = re.sub(r"\bEN CAJA\b", " ", texto)

    # Eliminar combinaciones de Pack / Caja con cantidades (ej. PACK 24 FRASCOS X 10 ML)
    texto = re.sub(
        r"\b(PACK|CAJA CON|CAJA|POTE|SACO|BOLSA)\s*\d*\s*(FRASCOS?|LATAS?|JERINGAS?|SOBRES?|TABLETAS?|PASTILLAS?|SACHETS?|TUBOS?|PIPETAS?)?\b",
        " ",
        texto,
    )

    # Eliminar formatos de medida precedidos por "X" (ej. X 100 ML, X 3.5 L, X 25 KG, X 1 TABLETA)
    texto = re.sub(
        r"\bX\s*\d+(\.\d+)?\s*(ML|L|LT|LTS|KG|G|GR|MG|OZ|CC|TABLETAS?|PASTILLAS?|SOBRES?|SACHETS?|JERINGAS?|FRASCOS?|LATAS?|UNIDADES?|UND)?\b",
        " ",
        texto,
    )

    # Eliminar concentraciones en porcentaje o peso (ej. 10%, 22.2%, 500 MG, 0.4 G, 1M)
    texto = re.sub(r"\b\d+(\.\d+)?\s*%", " ", texto)
    texto = re.sub(r"\b\d+(\.\d+)?\s*(MG|G|GR|ML|KG|L|M)\b", " ", texto)

    # Eliminar palabras sueltas de presentación o siglas técnicas
    palabras_excluir = [
        "ADULTO",
        "JERINGA",
        "JERINGAS",
        "SACO",
        "CAJA",
        "FRASCO",
        "FRASCOS",
        "BOTELLA",
        "BOLSA",
        "SOBRE",
        "SOBRES",
        "POTE",
        "TABLETA",
        "TABLETAS",
        "PASTILLAS",
        "PIPETA",
        "SACHETS",
        "TUBO",
        "SPRAY",
        "PACK",
        "LATAS",
        "L.A.",
        "LA",
        "USP",
        "FG",
        "DAB8",
        "CPV96",
        "ORAL",
        "INYECTABLE",
        "INYENTABLE",
        "POLVO SOLUBLE",
        "POLVO",
        "PREMIX",
        "GRANULADO",
        "PASTA",
        "SOLUCION",
        "SUSPENSION",
    ]
    patron_palabras = r"\b(" + "|".join(map(re.escape, palabras_excluir)) + r")\b"
    texto = re.sub(patron_palabras, " ", texto)

    # Estandarizar guiones y signos sueltos (ej. ALIMPET-DOG -> ALIMPET DOG)
    texto = re.sub(r"(?<=[A-Z])-(?=[A-Z])", " ", texto)
    texto = re.sub(r"\s+[\+\-\.,]\s*$", "", texto)  # Quitar símbolos al final

    # Limpiar espacios múltiples y recortar extremos
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto

def crear_grupo_linea(vendedor):
    relaciones = {
        "Felipe Morillos": "Aves & Cerdos",
        "Gustavo Feijóo": "Aves & Cerdos",
        "Maria Alemán": "Aves & Cerdos",
        "Melissa Garriazo": "Aves & Cerdos",
        "Milagros Huaringa": "Aves & Cerdos",
        "Nicolh Boza": "Aves & Cerdos",
        "Ubaldo Torreblanca": "Aves & Cerdos",
        "Willy Chihua": "Aves & Cerdos",
        "Antenor Culqui": "Ganadería",
        "Luis Puluche": "Ganadería",
        "Max Reategui": "Ganadería",
        "Yalilhe Espinoza": "Ganadería",
        "Eglys Bermudez": "Mascotas",
        "Karla Solano": "Mascotas",
        "Miguel Cabrera": "Mascotas",
        "Omar Tenaud": "Mascotas",
        "Jacky Gamarra": "Oficina",
        "Kely Espinoza": "Oficina",
        "Nimia Quispe": "Oficina",
        "Rogelio Gamarra": "Oficina",
        "Wilmer Gamarra": "Oficina",
        "NO REGISTRADO": "SIN LINEA"
    }

    return relaciones[vendedor]

def columna_antes(loc):
    if isinstance(loc, (int, np.integer)):
        pos = int(loc) - 1
    elif isinstance(loc, slice):
        pos = int(loc.stop or 0)
    else:
        pos = int(np.where(loc)[0][-1]) - 1
    return pos

def columna_despues(loc):
    if isinstance(loc, (int, np.integer)):
        pos = int(loc) + 1
    elif isinstance(loc, slice):
        pos = int(loc.stop or 0)
    else:
        pos = int(np.where(loc)[0][-1]) + 1
    return pos

def crear_excel():
    archivo_salida = "completo.xlsx"
    data = enviar_data()
    data.to_excel(archivo_salida, index=False)
    print((data["CONFLICTO"] == "SI").sum())

def enviar_data():

    # --- CONFIGURACIÓN DE ARCHIVOS ---
    # Nombres de los archivos
    archivo_entrada = "reporte melisa.xlsx"
    archivo_rv_2025 = "reporte ventas 2025.xlsx"
    archivo_rv_2026 = "reporte ventas 2026.xlsx"

    # Lista columnas seleccionadas
    columnas_entrada = [
        "MES",
        "AÑO",
        "SERIE.",
        "NÚMERO.",
        "PARTNER",
        "PRODUCTO",
        "UNIDAD",
        "SALIDA CANTIDAD",
        "VENDEDOR"
    ]
    columnas_rv = [
        "Nombre del contacto a mostrar en la factura",
        "Número",
        "TOTAL",
        "Vendedor"
    ]

    # Lista con los tipos de datos de cada columna
    tipos_entrada = {
        'MES': str,
        'AÑO': str,
        'SERIE.': str,
        'NÚMERO.': str,
        'PARTNER': str,
        'PRODUCTO': str,
        'UNIDAD': str,
        'SALIDA CANTIDAD': int,
        'VENDEDOR': str
    }
    tipos_rv = {
        'Nombre del contacto a mostrar en la factura': str,
        'Número': str,
        'TOTAL': float,
        'Vendedor': str
    }

    #Lista de cambios de nombres
    nuevo_nombre_entrada = {
        "SERIE.": "SERIE",
        "NÚMERO.": "NUMERO",
        "PRODUCTO": "PRESENTACION",
        "SALIDA CANTIDAD": "CANTIDAD"
    }
    nuevo_nombre_rv = {
        "Nombre del contacto a mostrar en la factura": "RV_PARTNER",
        "Número": "RV_NUMERO",
        "TOTAL": "RV_TOTAL",
        "Vendedor": "RV_VENDEDOR"
    }

    # Cargar solo los datos necesarios(los encabezados reales están en la fila 2 del Excel)
    df_entrada = pd.read_excel(archivo_entrada, header=1, usecols=columnas_entrada, dtype=tipos_entrada)
    df_rv_2025 = pd.read_excel(archivo_rv_2025, usecols=columnas_rv, dtype=tipos_rv)
    df_rv_2026 = pd.read_excel(archivo_rv_2026, usecols=columnas_rv, dtype=tipos_rv)

    # Renombrar las columnas (es necesario reasignar las variables)
    df_entrada = df_entrada.rename(columns=nuevo_nombre_entrada)
    df_rv_2025 = df_rv_2025.rename(columns=nuevo_nombre_rv)
    df_rv_2026 = df_rv_2026.rename(columns=nuevo_nombre_rv)

    # Normalizar los nombres de las columnas (MAYUSCULAS)
    # df_entrada.columns = df_entrada.columns.str.strip().str.upper()
    # df_rv_2025.columns = df_rv_2025.columns.str.strip().str.upper()
    # df_rv_2026.columns = df_rv_2026.columns.str.strip().str.upper()

    # Crear el nuevo grupo de PRODUCTOS(FAMILIA) y LINEA
    columna_producto = df_entrada["PRESENTACION"].apply(crear_grupo_producto)
    columna_linea = df_entrada["VENDEDOR"].apply(crear_grupo_linea)

    # Crear el nuevo grupo de COMPROBANTE
    col_serie = df_entrada["SERIE"].str.strip()
    col_numero = df_entrada["NUMERO"].str.strip()
    condicion_comprobante = (col_serie == '-') & (col_numero == '-')
    columna_comprobante = np.where(condicion_comprobante, '-', col_serie + '-' + col_numero )

    # Insertar la columna nueva de producto al costado de PRESENTACION y VENDEDOR
    loc_presentacion = df_entrada.columns.get_loc("PRESENTACION")
    loc_vendedor = df_entrada.columns.get_loc("VENDEDOR")
    loc_numero = df_entrada.columns.get_loc("NUMERO")
    df_entrada.insert(columna_despues(loc_presentacion), "PRODUCTO", columna_producto)
    df_entrada.insert(columna_despues(loc_vendedor), "LINEA", columna_linea)
    df_entrada.insert(columna_despues(loc_numero), "COMPROBANTE", columna_comprobante)

    # Concatenar los reportes de ventas (2025 y 2026) en una sola tabla vertical
    df_rv = pd.concat([df_rv_2025, df_rv_2026], ignore_index=True)
    df_rv = df_rv.drop_duplicates(subset=["RV_NUMERO"])

    # Realizar un único merge con el archivo principal (agrega solo 4 columnas limpias)
    df_resultado = pd.merge(
        df_entrada,
        df_rv,
        left_on="COMPROBANTE",
        right_on="RV_NUMERO",
        how="left"
    )

    # Agregar columna de CONFLICTO
    df_resultado["CONFLICTO"] = np.where(df_resultado["VENDEDOR"] == df_resultado["RV_VENDEDOR"], "NO", "SI")

    # Actualizar RV_VENDEDOR --> VENDEDOR ("NO REGISTRADO")
    condicion_no_registrado = (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "NO REGISTRADO") & ~(df_resultado["RV_VENDEDOR"].isna())
    df_resultado.loc[condicion_no_registrado, "VENDEDOR"] = df_resultado["RV_VENDEDOR"]
    # Actualizar VENDEDOR --> RV_VENDEDOR ("")
    condicion_en_blanco = (df_resultado["CONFLICTO"] == "SI") & (df_resultado["RV_VENDEDOR"].isna()) & ~(df_resultado["VENDEDOR"].isna())
    df_resultado.loc[condicion_en_blanco, "RV_VENDEDOR"] = df_resultado["VENDEDOR"]

    # VENDEDOR --- RV_VENDEDOR
    # Actualizar linea Aves & Cerdos
    # 1 --> Maria Alemán < Nicolh Boza
    condicion_ac_1 = (df_resultado["LINEA"] == "Aves & Cerdos") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Maria Alemán") & (df_resultado["RV_VENDEDOR"] == "Nicolh Boza")
    df_resultado.loc[condicion_ac_1, "VENDEDOR"] = df_resultado["RV_VENDEDOR"]
    # 2 --> Felipe Morillos < Ubaldo Torreblanca
    condicion_ac_2 = (df_resultado["LINEA"] == "Aves & Cerdos") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Felipe Morillos") & (df_resultado["RV_VENDEDOR"] == "Ubaldo Torreblanca")
    df_resultado.loc[condicion_ac_2, "VENDEDOR"] = df_resultado["RV_VENDEDOR"]
    # 3 --> Milagros Huaringa < Melissa Garriazo
    condicion_ac_3 = (df_resultado["LINEA"] == "Aves & Cerdos") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Milagros Huaringa") & (df_resultado["RV_VENDEDOR"] == "Melissa Garriazo")
    df_resultado.loc[condicion_ac_3, "VENDEDOR"] = df_resultado["RV_VENDEDOR"]
    # 4 --> Ubaldo Torreblanca > Miguel Cabrera
    condicion_ac_4 = (df_resultado["LINEA"] == "Aves & Cerdos") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Ubaldo Torreblanca") & (df_resultado["RV_VENDEDOR"] == "Miguel Cabrera")
    df_resultado.loc[condicion_ac_4, "RV_VENDEDOR"] = df_resultado["VENDEDOR"]
    # 5 --> Melissa Garriazo > all
    condicion_ac_5 = (df_resultado["LINEA"] == "Aves & Cerdos") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Melissa Garriazo") & ~(df_resultado["RV_VENDEDOR"] == "Melissa Garriazo")
    df_resultado.loc[condicion_ac_5, "RV_VENDEDOR"] = df_resultado["VENDEDOR"]
    # 6 --> Milagros Huaringa < Andrea Huauya
    condicion_ac_6 = (df_resultado["LINEA"] == "Aves & Cerdos") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Milagros Huaringa") & (df_resultado["RV_VENDEDOR"] == "Andrea Huauya")
    df_resultado.loc[condicion_ac_6, "VENDEDOR"] = df_resultado["RV_VENDEDOR"]

    # Actualizar linea Ganadería
    # 1 --> Antenor Culqui > all
    condicion_ganaderia_1 = (df_resultado["LINEA"] == "Ganadería") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Antenor Culqui") & ~(df_resultado["RV_VENDEDOR"] == "Antenor Culqui")
    df_resultado.loc[condicion_ganaderia_1, "RV_VENDEDOR"] = df_resultado["VENDEDOR"]

    # Actualizar linea Mascotas
    # 1 --> Eglys Bermudez < Karla Solano
    condicion_mascota_1 = (df_resultado["LINEA"] == "Mascotas") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Eglys Bermudez") & (df_resultado["RV_VENDEDOR"] == "Karla Solano")
    df_resultado.loc[condicion_mascota_1, "VENDEDOR"] = df_resultado["RV_VENDEDOR"]
    # 2 --> Eglys Bermudez > Nimia Quispe
    condicion_mascota_2 = (df_resultado["LINEA"] == "Mascotas") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Eglys Bermudez") & (df_resultado["RV_VENDEDOR"] == "Nimia Quispe")
    df_resultado.loc[condicion_mascota_2, "RV_VENDEDOR"] = df_resultado["VENDEDOR"]
    # 3 --> Karla Solano > Jacky Gamarra
    condicion_mascota_3 = (df_resultado["LINEA"] == "Mascotas") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Karla Solano") & (df_resultado["RV_VENDEDOR"] == "Jacky Gamarra")
    df_resultado.loc[condicion_mascota_3, "RV_VENDEDOR"] = df_resultado["VENDEDOR"]
    # 4 --> Karla Solano < Kristhian Rodriguez
    condicion_mascota_4 = (df_resultado["LINEA"] == "Mascotas") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Karla Solano") & (df_resultado["RV_VENDEDOR"] == "Kristhian Rodriguez")
    df_resultado.loc[condicion_mascota_4, "VENDEDOR"] = df_resultado["RV_VENDEDOR"]
    # 5 --> Miguel Cabrera > Jacky Gamarra
    condicion_mascota_5 = (df_resultado["LINEA"] == "Mascotas") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Miguel Cabrera") & (df_resultado["RV_VENDEDOR"] == "Jacky Gamarra")
    df_resultado.loc[condicion_mascota_5, "RV_VENDEDOR"] = df_resultado["VENDEDOR"]

    # Actualizar linea Oficina
    # Jacky Gamarra < Wilmer Gamarra
    condicion_oficina_1 = (df_resultado["LINEA"] == "Oficina") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Jacky Gamarra") & (df_resultado["RV_VENDEDOR"] == "Wilmer Gamarra")
    df_resultado.loc[condicion_oficina_1, "VENDEDOR"] = df_resultado["RV_VENDEDOR"]
    # Rogelio Gamarra > Jacky Gamarra
    condicion_oficina_2 = (df_resultado["LINEA"] == "Oficina") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Rogelio Gamarra") & (df_resultado["RV_VENDEDOR"] == "Jacky Gamarra")
    df_resultado.loc[condicion_oficina_2, "RV_VENDEDOR"] = df_resultado["VENDEDOR"]
    # Wilmer Gamarra > all
    condicion_oficina_3 = (df_resultado["LINEA"] == "Oficina") & (df_resultado["CONFLICTO"] == "SI") & (df_resultado["VENDEDOR"] == "Wilmer Gamarra") & ~(df_resultado["RV_VENDEDOR"] == "Wilmer Gamarra")
    df_resultado.loc[condicion_oficina_3, "RV_VENDEDOR"] = df_resultado["VENDEDOR"]

    # Actualizar columna CONFLICTO
    df_resultado.loc[df_resultado["VENDEDOR"] == df_resultado["RV_VENDEDOR"], "CONFLICTO"] = "NO"

    return df_resultado