import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scraping_la_vanguardia():
    print("Iniciando prueba de scraping en La Vanguardia...")
    
    # URL de la portada de La Vanguardia
    url = "https://www.lavanguardia.com"
    
    # Es importante añadir un 'User-Agent' para que la web no bloquee la petición del servidor de GitHub
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error al conectar con La Vanguardia: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    titulares = []
    enlaces = []
    
    # Buscamos las etiquetas de las historias/artículos principales
    # La Vanguardia suele usar etiquetas <article> para sus noticias
    articulos = soup.find_all('article')
    
    print(f"Se han encontrado {len(articulos)} elementos de noticias potenciales.")

    for art in articulos:
        # Buscamos el primer enlace <a> que suele contener el titular dentro del artículo
        enlace_tag = art.find('a')
        
        if enlace_tag and enlace_tag.text:
            texto_titular = enlace_tag.text.strip()
            url_noticia = enlace_tag.get('href', '')
            
            # Filtramos titulares vacíos o demasiado cortos (como "Opinión", "Vídeo", etc.)
            if len(texto_titular) > 15:
                # Aseguramos que la URL sea completa
                if url_noticia.startswith('/'):
                    url_noticia = f"https://www.lavanguardia.com{url_noticia}"
                
                titulares.append(texto_titular)
                enlaces.append(url_noticia)
    
    # Si no encontramos nada por cambios de diseño, añadimos un plan B general
    if not titulares:
        # Busca cualquier encabezado h1, h2 o h3 que tenga un enlace dentro
        for encabezado in soup.find_all(['h1', 'h2', 'h3']):
            a_tag = encabezado.find('a')
            if a_tag and a_tag.text.strip():
                titulares.append(a_tag.text.strip())
                enlaces.append(a_tag.get('href', ''))

    # Creamos el reporte de datos
    fecha_extraccion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    df = pd.DataFrame({
        'Titular': titulares,
        'Enlace': enlaces,
        'Fecha_Captura': fecha_extraccion
    })
    
    # Eliminamos duplicados si los hay
    df.drop_duplicates(subset=['Titular'], inplace=True)
    
    # Nombre del archivo que aparecerá en tu repositorio
    archivo_salida = "titulares_lavanguardia.csv"
    
    # Guardamos los datos (Sobrescribe el archivo para tener siempre las noticias de última hora)
    df.to_csv(archivo_salida, index=False, encoding='utf-8')
    print(f"✅ ¡Éxito! Se han guardado {len(df)} titulares en '{archivo_salida}'.")

if __name__ == "__main__":
    scraping_la_vanguardia()
