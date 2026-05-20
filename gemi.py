import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def ejecutar_scraping():
    print("Iniciando el proceso de scraping manual...")
    
    # 1. Definir la URL a la que le haremos scraping
    # Usaremos una web de prueba de libros muy común para scraping
    url = "http://books.toscrape.com/"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Lanza un error si la web no responde correctamente
    except Exception as e:
        print(f"Error al conectar con la web: {e}")
        return

    # 2. Parsear el contenido HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Listas para guardar la información
    titulos = []
    precios = []
    
    # 3. Buscar los elementos en la página (en este caso, libros)
    libros = soup.find_all('article', class_='product_pod')
    
    for libro in libros:
        # Extraer el título del libro
        titulo = libro.h3.a['title']
        # Extraer el precio
        precio = libro.find('p', class_='price_color').text
        
        titulos.append(titulo)
        precios.append(precio)
    
    # 4. Crear un DataFrame con los datos estructurados
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame({
        'Título': titulos,
        'Precio': precios,
        'Fecha de Extracción': fecha_actual
    })
    
    # Nombre del archivo donde se guardarán los datos
    archivo_salida = "resultados_scraping.csv"
    
    # 5. Guardar los datos en un archivo CSV
    # Si el archivo ya existe, añade los nuevos datos abajo sin borrar los anteriores (mode='a')
    # Si no existe, lo crea desde cero con las cabeceras
    if not os.path.isfile(archivo_salida):
        df.to_csv(archivo_salida, index=False, encoding='utf-8')
        print(f"Archivo '{archivo_salida}' creado con éxito.")
    else:
        df.to_csv(archivo_salida, mode='a', header=False, index=False, encoding='utf-8')
        print(f"Datos nuevos añadidos correctamente a '{archivo_salida}'.")

if __name__ == "__main__":
    ejecutar_scraping()
