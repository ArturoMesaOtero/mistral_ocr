# 🔍 Mistral OCR Explorer

Un proyecto completo en Python para explorar y probar todas las capacidades de **Mistral Document AI** con OCR avanzado.

## 🌟 Características

- ✅ **Procesamiento de múltiples formatos**: PDF, DOCX, PPTX, imágenes (PNG, JPEG, AVIF)
- ✅ **Múltiples métodos de procesamiento**: Local, upload, URLs
- ✅ **Análisis avanzado de texto**: Extracción de datos estructurados, nubes de palabras
- ✅ **Procesamiento en lote**: Procesa carpetas completas automáticamente
- ✅ **Benchmarking**: Mide rendimiento y velocidad de procesamiento
- ✅ **Comparación de métodos**: Compara diferentes enfoques de OCR
- ✅ **Reportes detallados**: Genera reportes completos en Markdown
- ✅ **Interfaz interactiva**: Menús fáciles de usar para todas las funciones

## 🚀 Instalación

### 1. Configurar el entorno

```bash
# Clonar o crear el proyecto
git clone <tu-repo> # o crear carpeta manualmente
cd mistral-ocr-explorer

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
# Instalar dependencias básicas
pip install mistralai python-dotenv PyPDF2 python-docx2txt Pillow

# Para funciones avanzadas (opcional)
pip install matplotlib seaborn wordcloud pandas numpy requests tqdm

# O instalar todo desde requirements
pip install -r requirements.txt
```

### 3. Configurar API Key

1. Obtén tu API key de Mistral en: https://console.mistral.ai/
2. Crea un archivo `.env` en la raíz del proyecto:

```env
MISTRAL_API_KEY=tu_api_key_aqui
```

## 📁 Estructura del Proyecto

```
mistral_ocr_project/
│
├── .env                    # Tu API key
├── main.py                 # Demo básico
├── advanced_demo.py        # Demo avanzado
├── requirements.txt        # Dependencias
│
├── src/
│   ├── ocr_processor.py    # Clase principal OCR
│   └── utils.py            # Utilidades avanzadas
│
├── documents/              # Tus archivos a procesar
│   ├── pdf/               # Archivos PDF
│   ├── word/              # Archivos DOCX
│   ├── images/            # Imágenes PNG/JPEG
│   └── samples/           # Archivos de muestra
│
└── results/               # Resultados JSON y reportes
    ├── *.json             # Resultados OCR
    ├── *.png              # Nubes de palabras
    └── *.md               # Reportes
```

## 🎯 Uso Rápido

### Demo Básico

```bash
python main.py
```

Incluye:
- Procesamiento de PDF desde URL
- Procesamiento de imagen desde URL  
- Procesamiento de archivos locales
- Subida y procesamiento de archivos
- Menú interactivo

### Demo Avanzado

```bash
python advanced_demo.py
```

Incluye todas las funciones avanzadas:
- Análisis de texto estructurado
- Procesamiento en lote
- Benchmarking de rendimiento
- Comparación de métodos
- Generación de reportes

## 📖 Ejemplos de Código

### Procesamiento Básico

```python
from src.ocr_processor import MistralOCRProcessor

# Inicializar
processor = MistralOCRProcessor()

# Procesar PDF desde URL
response = processor.process_document_from_url(
    "https://arxiv.org/pdf/2201.04234", 
    "document_url"
)

# Extraer texto
text = processor.extract_text_content(response)
print(f"Texto extraído: {len(text)} caracteres")

# Guardar resultados
processor.save_results(response, "mi_documento.json")
```

### Procesamiento de Archivo Local

```python
# Procesar archivo local
response = processor.process_local_file("documents/pdf/mi_archivo.pdf")

if response:
    text = processor.extract_text_content(response)
    analysis = processor.analyze_document_structure(response)
    print(f"Palabras: {analysis['total_words']}")
```

### Procesamiento en Lote

```python
from src.utils import batch_process_folder

# Procesar toda una carpeta
results = batch_process_folder("documents/pdf", processor)
print(f"Procesados: {results['processed_files']} archivos")
```

## 🔧 Funcionalidades Detalladas

### 1. Métodos de Procesamiento

- **Local (Base64)**: Codifica archivos localmente y los envía
- **Upload**: Sube archivos a Mistral y los procesa
- **URL**: Procesa documentos directamente desde URLs

### 2. Análisis de Texto

- Extracción de emails, teléfonos, URLs, fechas
- Detección de headers y estructura
- Conteo de palabras, caracteres, líneas
- Generación de nubes de palabras

### 3. Formatos Soportados

| Formato | Extensión | Método |
|---------|-----------|--------|
| PDF | .pdf | document_url |
| Word | .docx | document_url |
| PowerPoint | .pptx | document_url |
| Imagen PNG | .png | image_url |
| Imagen JPEG | .jpg, .jpeg | image_url |
| Imagen AVIF | .avif | image_url |

### 4. Limitaciones del API

- **Tamaño máximo**: 50 MB por archivo
- **Páginas máximas**: 1,000 páginas por documento
- **Formatos**: Solo documentos e imágenes (no audio/video)

## 📊 Casos de Uso

### 1. Digitalización de Documentos
```python
# Procesar facturas escaneadas
receipt_response = processor.process_local_file("invoices/receipt_001.png")
text = processor.extract_text_content(receipt_response)
structured_data = extract_structured_data(text)
print(f"Emails encontrados: {structured_data['emails']}")
```

### 2. Análisis de Papers Científicos
```python
# Procesar paper desde arXiv
paper_url = "https://arxiv.org/pdf/2201.04234"
response = processor.process_document_from_url(paper_url, "document_url")
analysis = processor.analyze_document_structure(response)
create_word_cloud(processor.extract_text_content(response))
```

### 3. Procesamiento Masivo
```python
# Procesar carpeta completa de documentos
batch_results = batch_process_folder("documents/contracts", processor)
generate_batch_report(batch_results)
```

## 🛠️ Desarrollo y Personalización

### Añadir Nuevos Análisis

Puedes extender `utils.py` con nuevas funciones:

```python
def extract_financial_data(text: str) -> Dict[str, List[str]]:
    """Extrae datos financieros específicos"""
    patterns = {
        "amounts": r'\$\d+\.?\d*',
        "percentages": r'\d+\.?\d*%',
        "currencies": r'(USD|EUR|GBP)\s*\d+'
    }
    
    results = {}
    for key, pattern in patterns.items():
        results[key] = re.findall(pattern, text)
    
    return results
```

### Personalizar Reportes

Modifica las funciones de reporte en `utils.py` para incluir tus métricas específicas.

## 🚨 Solución de Problemas

### Error: "No se encontró MISTRAL_API_KEY"
- Verifica que el archivo `.env` existe y contiene `MISTRAL_API_KEY=tu_key`
- Asegúrate de que el archivo `.env` está en la raíz del proyecto

### Error: "Formato de archivo no soportado"
- Verifica que el archivo tiene una extensión soportada (.pdf, .docx, .png, etc.)
- Comprueba que el archivo no está corrupto

### Error de memoria o timeout
- Para archivos grandes (>10MB), usa el método de upload
- Divide documentos muy largos en secciones más pequeñas

### Dependencias faltantes
```bash
# Instalar dependencias opcionales para funciones avanzadas
pip install matplotlib seaborn wordcloud pandas numpy
```

## 📈 Métricas y Rendimiento

El sistema incluye herramientas de benchmark que miden:

- **Tiempo de procesamiento** por archivo
- **Caracteres por segundo** extraídos
- **Palabras por segundo** procesadas
- **Tasa de éxito** por tipo de archivo
- **Comparación entre métodos** de procesamiento

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🔗 Enlaces Útiles

- [Documentación de Mistral OCR](https://docs.mistral.ai/)
- [Console de Mistral](https://console.mistral.ai/)
- [Ejemplos de Mistral](https://github.com/mistralai/cookbook)

## 📞 Soporte

Si encuentras problemas o tienes preguntas:

1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Consulta la documentación oficial de Mistral
3. Abre un issue en el repositorio del proyecto

---

**¡Happy coding! 🚀**