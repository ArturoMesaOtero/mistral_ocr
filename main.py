"""
Demostración completa de Mistral OCR
Ejemplos prácticos para explorar todas las funcionalidades
"""

import os
import sys
from pathlib import Path

# Añadir el directorio src al path
sys.path.append(str(Path(__file__).parent / "src"))

from src.ocr_processor import MistralOCRProcessor


def print_separator(title: str):
    """Imprime un separador visual con título"""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)


def demo_url_processing(processor: MistralOCRProcessor):
    """Demuestra el procesamiento de documentos desde URL"""
    print_separator("PROCESAMIENTO DESDE URL")

    # Ejemplo con PDF desde arXiv
    pdf_url = "https://arxiv.org/pdf/2201.04234"
    print(f"📄 Procesando PDF desde: {pdf_url}")

    response = processor.process_document_from_url(pdf_url, "document_url")

    if response:
        # Guardar resultados
        result_file = processor.save_results(response, "arxiv_paper_ocr.json")

        # Extraer y mostrar texto
        text_content = processor.extract_text_content(response)
        print(f"\n📝 Primeros 500 caracteres del texto extraído:")
        print("-" * 50)
        print(text_content[:500] + "..." if len(text_content) > 500 else text_content)

        # Análisis de estructura
        analysis = processor.analyze_document_structure(response)
        print(f"\n📊 Análisis del documento:")
        for key, value in analysis.items():
            print(f"  • {key}: {value}")
    else:
        print("❌ No se pudo procesar el documento desde URL")


def demo_image_processing(processor: MistralOCRProcessor):
    """Demuestra el procesamiento de imágenes desde URL"""
    print_separator("PROCESAMIENTO DE IMAGEN")

    # Ejemplo con imagen de recibo
    image_url = "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
    print(f"🖼️ Procesando imagen desde: {image_url}")

    response = processor.process_document_from_url(image_url, "image_url")

    if response:
        # Guardar resultados
        result_file = processor.save_results(response, "receipt_ocr.json")

        # Extraer y mostrar texto
        text_content = processor.extract_text_content(response)
        print(f"\n📝 Texto extraído de la imagen:")
        print("-" * 50)
        print(text_content)

        # Análisis de estructura
        analysis = processor.analyze_document_structure(response)
        print(f"\n📊 Análisis de la imagen:")
        for key, value in analysis.items():
            print(f"  • {key}: {value}")
    else:
        print("❌ No se pudo procesar la imagen desde URL")


def demo_local_file_processing(processor: MistralOCRProcessor):
    """Demuestra el procesamiento de archivos locales"""
    print_separator("PROCESAMIENTO DE ARCHIVOS LOCALES")

    # Buscar archivos en las carpetas
    pdf_files = list(Path("documents/pdf").glob("*.pdf"))
    word_files = list(Path("documents/word").glob("*.docx"))
    image_files = list(Path("documents/images").glob("*.*"))

    all_files = pdf_files + word_files + image_files

    if not all_files:
        print("📁 No se encontraron archivos en las carpetas documents/")
        print("   Coloca algunos archivos PDF, DOCX o imágenes en:")
        print("   • documents/pdf/")
        print("   • documents/word/")
        print("   • documents/images/")
        return

    print(f"📁 Archivos encontrados: {len(all_files)}")
    for file_path in all_files:
        print(f"  • {file_path}")

    # Procesar el primer archivo encontrado
    if all_files:
        file_to_process = all_files[0]
        print(f"\n🔄 Procesando: {file_to_process}")

        response = processor.process_local_file(str(file_to_process))

        if response:
            # *** AÑADIR DIAGNÓSTICO TEMPORAL ***
            processor.debug_response_structure(response)

            # Crear nombre de archivo para resultados
            result_filename = f"{file_to_process.stem}_ocr.json"
            result_file = processor.save_results(response, result_filename)

            # Extraer y mostrar texto
            text_content = processor.extract_text_content(response)
            print(f"\n📝 Primeros 300 caracteres del texto extraído:")
            print("-" * 50)
            print(text_content[:300] + "..." if len(text_content) > 300 else text_content)

            # Análisis de estructura
            analysis = processor.analyze_document_structure(response)
            print(f"\n📊 Análisis del archivo:")
            for key, value in analysis.items():
                print(f"  • {key}: {value}")
        else:
            print("❌ No se pudo procesar el archivo local")


def demo_upload_processing(processor: MistralOCRProcessor):
    """Demuestra el procesamiento subiendo archivos a Mistral"""
    print_separator("PROCESAMIENTO CON SUBIDA DE ARCHIVOS")

    # Buscar archivos para subir
    all_files = list(Path("documents").rglob("*.*"))
    supported_extensions = ['.pdf', '.docx', '.pptx', '.jpg', '.jpeg', '.png', '.avif']
    supported_files = [f for f in all_files if f.suffix.lower() in supported_extensions]

    if not supported_files:
        print("📁 No se encontraron archivos soportados para subir")
        return

    # Subir y procesar el primer archivo
    file_to_upload = supported_files[0]
    print(f"☁️ Subiendo y procesando: {file_to_upload}")

    response = processor.upload_and_process_file(str(file_to_upload))

    if response:
        # Crear nombre de archivo para resultados
        result_filename = f"{file_to_upload.stem}_uploaded_ocr.json"
        result_file = processor.save_results(response, result_filename)

        # Extraer y mostrar texto
        text_content = processor.extract_text_content(response)
        print(f"\n📝 Primeros 300 caracteres del texto extraído:")
        print("-" * 50)
        print(text_content[:300] + "..." if len(text_content) > 300 else text_content)

        # Análisis de estructura
        analysis = processor.analyze_document_structure(response)
        print(f"\n📊 Análisis del archivo subido:")
        for key, value in analysis.items():
            print(f"  • {key}: {value}")
    else:
        print("❌ No se pudo procesar el archivo subido")


def interactive_menu(processor: MistralOCRProcessor):
    """Menú interactivo para probar diferentes funcionalidades"""
    while True:
        print("\n" + "=" * 60)
        print("🎯 MENÚ INTERACTIVO - MISTRAL OCR")
        print("=" * 60)
        print("1. 📄 Procesar PDF desde URL (arXiv paper)")
        print("2. 🖼️ Procesar imagen desde URL (recibo)")
        print("3. 📁 Procesar archivo local")
        print("4. ☁️ Subir y procesar archivo")
        print("5. 🔍 Ver archivos disponibles")
        print("6. 📊 Mostrar información del API")
        print("0. ❌ Salir")
        print("-" * 60)

        try:
            choice = input("Selecciona una opción (0-6): ").strip()

            if choice == "0":
                print("👋 ¡Hasta luego!")
                break
            elif choice == "1":
                demo_url_processing(processor)
            elif choice == "2":
                demo_image_processing(processor)
            elif choice == "3":
                demo_local_file_processing(processor)
            elif choice == "4":
                demo_upload_processing(processor)
            elif choice == "5":
                show_available_files()
            elif choice == "6":
                show_api_info(processor)
            else:
                print("❌ Opción no válida. Selecciona un número del 0 al 6.")

        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def show_available_files():
    """Muestra los archivos disponibles en las carpetas"""
    print_separator("ARCHIVOS DISPONIBLES")

    folders = ["documents/pdf", "documents/word", "documents/images"]

    for folder in folders:
        folder_path = Path(folder)
        if folder_path.exists():
            files = list(folder_path.glob("*.*"))
            print(f"\n📁 {folder}:")
            if files:
                for file in files:
                    size_kb = file.stat().st_size / 1024
                    print(f"  • {file.name} ({size_kb:.1f} KB)")
            else:
                print("  (vacía)")
        else:
            print(f"\n📁 {folder}: (no existe)")


def show_api_info(processor: MistralOCRProcessor):
    """Muestra información sobre el API y limitaciones"""
    print_separator("INFORMACIÓN DEL API")

    print("🔧 Configuración actual:")
    print(f"  • Modelo: {processor.model}")
    print(f"  • API Key configurada: {'✅ Sí' if processor.api_key else '❌ No'}")

    print("\n📋 Formatos soportados:")
    print("  • Documentos: PDF, DOCX, PPTX")
    print("  • Imágenes: PNG, JPEG/JPG, AVIF")

    print("\n⚠️ Limitaciones:")
    print("  • Tamaño máximo: 50 MB por archivo")
    print("  • Páginas máximas: 1,000 páginas")
    print("  • Solo texto e imágenes (no audio/video)")

    print("\n🎯 Capacidades:")
    print("  • Mantiene estructura del documento")
    print("  • Preserva formato (headers, párrafos, listas, tablas)")
    print("  • Salida en formato markdown")
    print("  • Layouts complejos y multi-columna")
    print("  • Procesamiento escalable con alta precisión")


def main():
    """Función principal del programa"""
    print("🚀 INICIANDO DEMO DE MISTRAL OCR")
    print("=" * 60)

    try:
        # Inicializar el procesador
        processor = MistralOCRProcessor()

        # Mostrar menú interactivo
        interactive_menu(processor)

    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("\n🔧 Para solucionar:")
        print("1. Crea un archivo .env en la raíz del proyecto")
        print("2. Añade tu API key: MISTRAL_API_KEY=tu_api_key_aqui")
        print("3. Obtén tu API key en: https://console.mistral.ai/")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()