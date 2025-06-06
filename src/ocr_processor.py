"""
OCR Processor usando Mistral Document AI
Creado para explorar las capacidades de OCR con diferentes tipos de documentos
"""

import os
import base64
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from mistralai import Mistral
from dotenv import load_dotenv


class MistralOCRProcessor:
    """
    Clase para procesar documentos usando Mistral OCR
    Soporta PDF, Word, imágenes y más formatos
    """

    def __init__(self):
        """Inicializa el procesador con la API key de Mistral"""
        load_dotenv()  # Carga variables del archivo .env

        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("❌ No se encontró MISTRAL_API_KEY en el archivo .env")

        self.client = Mistral(api_key=self.api_key)
        self.model = "mistral-ocr-latest"

        # Crear carpetas si no existen
        self._create_directories()

        print("✅ MistralOCRProcessor inicializado correctamente")

    def _create_directories(self):
        """Crea las carpetas necesarias para el proyecto"""
        directories = ['documents/pdf', 'documents/word', 'documents/images', 'results']
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

    def encode_file_to_base64(self, file_path: str) -> Optional[str]:
        """
        Codifica un archivo a base64

        Args:
            file_path (str): Ruta del archivo a codificar

        Returns:
            str: Archivo codificado en base64 o None si hay error
        """
        try:
            with open(file_path, "rb") as file:
                encoded = base64.b64encode(file.read()).decode('utf-8')
                print(f"✅ Archivo {file_path} codificado correctamente")
                return encoded
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo {file_path}")
            return None
        except Exception as e:
            print(f"❌ Error al codificar {file_path}: {e}")
            return None

    def process_document_from_url(self, document_url: str, doc_type: str = "document_url") -> Optional[Dict[Any, Any]]:
        """
        Procesa un documento desde una URL

        Args:
            document_url (str): URL del documento
            doc_type (str): Tipo de documento ('document_url' o 'image_url')

        Returns:
            dict: Respuesta del OCR o None si hay error
        """
        try:
            print(f"🔄 Procesando documento desde URL: {document_url}")

            document_config = {
                "type": doc_type,
                doc_type: document_url
            }

            response = self.client.ocr.process(
                model=self.model,
                document=document_config,
                include_image_base64=True
            )

            print("✅ Documento procesado exitosamente desde URL")
            return response

        except Exception as e:
            print(f"❌ Error al procesar documento desde URL: {e}")
            return None

    def process_local_file(self, file_path: str) -> Optional[Dict[Any, Any]]:
        """
        Procesa un archivo local

        Args:
            file_path (str): Ruta del archivo local

        Returns:
            dict: Respuesta del OCR o None si hay error
        """
        try:
            print(f"🔄 Procesando archivo local: {file_path}")

            # Determinar el tipo de archivo y formato MIME
            file_extension = Path(file_path).suffix.lower()

            mime_types = {
                '.pdf': 'application/pdf',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.avif': 'image/avif'
            }

            if file_extension not in mime_types:
                print(f"❌ Formato de archivo no soportado: {file_extension}")
                return None

            # Codificar archivo
            base64_content = self.encode_file_to_base64(file_path)
            if not base64_content:
                return None

            # Determinar el tipo de documento
            doc_type = "image_url" if file_extension in ['.jpg', '.jpeg', '.png', '.avif'] else "document_url"

            # Crear URL con base64
            data_url = f"data:{mime_types[file_extension]};base64,{base64_content}"

            document_config = {
                "type": doc_type,
                doc_type: data_url
            }

            response = self.client.ocr.process(
                model=self.model,
                document=document_config,
                include_image_base64=True
            )

            print("✅ Archivo local procesado exitosamente")
            return response

        except Exception as e:
            print(f"❌ Error al procesar archivo local: {e}")
            return None

    def upload_and_process_file(self, file_path: str) -> Optional[Dict[Any, Any]]:
        """
        Sube un archivo a Mistral y lo procesa

        Args:
            file_path (str): Ruta del archivo a subir

        Returns:
            dict: Respuesta del OCR o None si hay error
        """
        try:
            print(f"🔄 Subiendo y procesando archivo: {file_path}")

            # Subir archivo
            with open(file_path, "rb") as file:
                uploaded_file = self.client.files.upload(
                    file={
                        "file_name": Path(file_path).name,
                        "content": file,
                    },
                    purpose="ocr"
                )

            print(f"✅ Archivo subido con ID: {uploaded_file.id}")

            # Obtener URL firmada
            signed_url = self.client.files.get_signed_url(file_id=uploaded_file.id)

            # Procesar archivo
            response = self.client.ocr.process(
                model=self.model,
                document={
                    "type": "document_url",
                    "document_url": signed_url.url,
                },
                include_image_base64=True
            )

            print("✅ Archivo subido y procesado exitosamente")
            return response

        except Exception as e:
            print(f"❌ Error al subir y procesar archivo: {e}")
            return None

    def save_results(self, response: Dict[Any, Any], filename: str = None) -> str:
        """
        Guarda los resultados del OCR en un archivo JSON

        Args:
            response (dict): Respuesta del OCR
            filename (str): Nombre del archivo (opcional)

        Returns:
            str: Ruta del archivo guardado
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ocr_result_{timestamp}.json"

        results_path = Path("results") / filename

        try:
            # Convertir la respuesta a diccionario si es necesario
            if hasattr(response, '__dict__'):
                response_dict = response.__dict__
            else:
                response_dict = response

            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(response_dict, f, indent=2, ensure_ascii=False, default=str)

            print(f"💾 Resultados guardados en: {results_path}")
            return str(results_path)

        except Exception as e:
            print(f"❌ Error al guardar resultados: {e}")
            return ""

    def extract_text_content(self, response: Dict[Any, Any]) -> str:
        """
        Extrae solo el contenido de texto de la respuesta

        Args:
            response (dict): Respuesta del OCR

        Returns:
            str: Texto extraído
        """
        try:
            # Según la API de Mistral, la estructura es:
            # response.pages[].markdown

            extracted_text = ""

            # Si es un objeto de Mistral
            if hasattr(response, 'pages'):
                pages = response.pages
                if pages and isinstance(pages, list):
                    for page in pages:
                        if hasattr(page, 'markdown') and page.markdown:
                            extracted_text += page.markdown + "\n\n"
                        elif isinstance(page, dict) and 'markdown' in page:
                            extracted_text += page['markdown'] + "\n\n"

                if extracted_text.strip():
                    return extracted_text.strip()

            # Si es un diccionario
            elif isinstance(response, dict):
                if 'pages' in response and isinstance(response['pages'], list):
                    for page in response['pages']:
                        if isinstance(page, dict) and 'markdown' in page and page['markdown']:
                            extracted_text += page['markdown'] + "\n\n"

                if extracted_text.strip():
                    return extracted_text.strip()

            # Buscar en otras ubicaciones posibles como fallback
            if hasattr(response, '__dict__'):
                response_dict = response.__dict__
            else:
                response_dict = response if isinstance(response, dict) else {}

            # Buscar en diferentes ubicaciones posibles
            for key in ['text', 'content', 'markdown', 'extracted_text', 'ocr_text']:
                if key in response_dict and response_dict[key]:
                    content = response_dict[key]
                    if isinstance(content, str):
                        return content
                    elif isinstance(content, dict) and 'text' in content:
                        return content['text']

            # Buscar recursivamente
            def find_text_recursive(obj, depth=0):
                if depth > 3:  # Evitar recursión infinita
                    return None

                if isinstance(obj, str) and len(obj) > 10:  # Texto significativo
                    return obj
                elif isinstance(obj, dict):
                    for key, value in obj.items():
                        if key in ['text', 'content', 'markdown'] and isinstance(value, str) and len(value) > 10:
                            return value
                        result = find_text_recursive(value, depth + 1)
                        if result:
                            return result
                elif isinstance(obj, list):
                    for item in obj:
                        result = find_text_recursive(item, depth + 1)
                        if result:
                            return result
                return None

            recursive_result = find_text_recursive(response)
            if recursive_result:
                return recursive_result

            return "No se encontró texto en la respuesta del OCR"

        except Exception as e:
            print(f"❌ Error al extraer texto: {e}")
            return f"Error al extraer texto: {e}"

    def analyze_document_structure(self, response: Dict[Any, Any]) -> Dict[str, Any]:
        """
        Analiza la estructura del documento procesado

        Args:
            response (dict): Respuesta del OCR

        Returns:
            dict: Análisis de la estructura
        """
        analysis = {
            "total_characters": 0,
            "total_words": 0,
            "total_lines": 0,
            "has_images": False,
            "document_type": "unknown",
            "processing_time": "unknown"
        }

        try:
            text_content = self.extract_text_content(response)

            if text_content and text_content != "No se encontró texto en la respuesta del OCR":
                analysis["total_characters"] = len(text_content)
                analysis["total_words"] = len(text_content.split())
                analysis["total_lines"] = len(text_content.split('\n'))

            # Buscar información adicional en la respuesta
            if hasattr(response, '__dict__'):
                response_dict = response.__dict__
            else:
                response_dict = response

            # Detectar si hay imágenes
            if 'images' in str(response_dict).lower() or 'image' in str(response_dict).lower():
                analysis["has_images"] = True

            return analysis

        except Exception as e:
            print(f"❌ Error al analizar estructura: {e}")
            return analysis

    def debug_response_structure(self, response: Dict[Any, Any]) -> None:
        """
        Función de diagnóstico para entender la estructura de la respuesta
        """
        try:
            print("\n" + "=" * 50)
            print("🔍 DIAGNÓSTICO DE RESPUESTA MISTRAL OCR")
            print("=" * 50)

            print(f"Tipo de respuesta: {type(response)}")

            if hasattr(response, '__dict__'):
                print(f"Atributos del objeto: {list(response.__dict__.keys())}")

                # Mostrar cada atributo
                for attr_name in response.__dict__.keys():
                    attr_value = getattr(response, attr_name)
                    print(f"\n📝 {attr_name}:")
                    print(f"  Tipo: {type(attr_value)}")

                    if isinstance(attr_value, str):
                        preview = attr_value[:200] + "..." if len(attr_value) > 200 else attr_value
                        print(f"  Contenido: {preview}")
                    elif hasattr(attr_value, '__dict__'):
                        print(f"  Sub-atributos: {list(attr_value.__dict__.keys())}")
                    else:
                        print(f"  Valor: {str(attr_value)[:100]}...")

            elif isinstance(response, dict):
                print(f"Claves del diccionario: {list(response.keys())}")

                for key, value in response.items():
                    print(f"\n📝 {key}:")
                    print(f"  Tipo: {type(value)}")

                    if isinstance(value, str):
                        preview = value[:200] + "..." if len(value) > 200 else value
                        print(f"  Contenido: {preview}")
                    elif isinstance(value, dict):
                        print(f"  Sub-claves: {list(value.keys())}")
                    else:
                        print(f"  Valor: {str(value)[:100]}...")

            print("=" * 50)

        except Exception as e:
            print(f"❌ Error en diagnóstico: {e}")


