"""
Demo Avanzado de Mistral OCR
Incluye todas las funcionalidades y casos de uso avanzados
"""

import sys
import time
from pathlib import Path

# Añadir src al path
sys.path.append(str(Path(__file__).parent / "src"))

from src.ocr_processor import MistralOCRProcessor
from src.utils import (
    analyze_ocr_results,
    generate_ocr_report,
    compare_ocr_methods,
    extract_structured_data,
    batch_process_folder,
    performance_benchmark,
    create_word_cloud
)


def advanced_text_analysis_demo(processor: MistralOCRProcessor):
    """Demo de análisis avanzado de texto extraído"""
    print("\n" + "=" * 70)
    print("🔬 DEMO: ANÁLISIS AVANZADO DE TEXTO")
    print("=" * 70)

    # Procesar un documento de ejemplo
    print("📄 Procesando documento de ejemplo para análisis...")

    # URL de un paper científico
    paper_url = "https://arxiv.org/pdf/2201.04234"
    response = processor.process_document_from_url(paper_url, "document_url")

    if response:
        text_content = processor.extract_text_content(response)

        print(f"📊 Análisis básico:")
        print(f"  • Caracteres: {len(text_content):,}")
        print(f"  • Palabras: {len(text_content.split()):,}")
        print(f"  • Líneas: {len(text_content.split('\\n')):,}")

        # Extraer datos estructurados
        print("\n🔍 Extrayendo datos estructurados...")
        structured_data = extract_structured_data(text_content)

        for data_type, items in structured_data.items():
            if items:
                print(f"  • {data_type.capitalize()}: {len(items)} encontrados")
                if len(items) <= 5:  # Mostrar solo algunos ejemplos
                    for item in items[:3]:
                        print(f"    - {item}")
                    if len(items) > 3:
                        print(f"    ... y {len(items) - 3} más")

        # Crear nube de palabras
        print("\n☁️ Generando nube de palabras...")
        try:
            create_word_cloud(text_content, "results/paper_wordcloud.png")
        except Exception as e:
            print(f"❌ Error al crear nube de palabras: {e}")
            print("💡 Instala wordcloud y matplotlib: pip install wordcloud matplotlib")

    else:
        print("❌ No se pudo procesar el documento para análisis")


def batch_processing_demo(processor: MistralOCRProcessor):
    """Demo de procesamiento en lote"""
    print("\n" + "=" * 70)
    print("📦 DEMO: PROCESAMIENTO EN LOTE")
    print("=" * 70)

    # Verificar si hay archivos para procesar
    folders_to_check = ["documents/pdf", "documents/word", "documents/images"]

    total_files = 0
    for folder in folders_to_check:
        folder_path = Path(folder)
        if folder_path.exists():
            files = list(folder_path.rglob("*.*"))
            supported_files = [f for f in files if
                               f.suffix.lower() in ['.pdf', '.docx', '.pptx', '.jpg', '.jpeg', '.png', '.avif']]
            total_files += len(supported_files)
            print(f"📁 {folder}: {len(supported_files)} archivos soportados")

    if total_files == 0:
        print("📂 No hay archivos para procesar en lote.")
        print("💡 Coloca algunos archivos en las carpetas documents/ para probar esta función.")
        return

    print(f"\n🚀 Iniciando procesamiento en lote de {total_files} archivos...")

    # Procesar cada carpeta
    for folder in folders_to_check:
        folder_path = Path(folder)
        if folder_path.exists():
            files = list(folder_path.rglob("*.*"))
            if files:
                print(f"\n📂 Procesando carpeta: {folder}")
                batch_results = batch_process_folder(str(folder_path), processor)

                if "error" not in batch_results:
                    print(f"✅ Procesados: {batch_results['processed_files']}/{batch_results['total_files']}")
                    print(f"📊 Total caracteres: {batch_results['summary']['total_characters']:,}")
                    print(f"📝 Total palabras: {batch_results['summary']['total_words']:,}")


def comparison_demo(processor: MistralOCRProcessor):
    """Demo de comparación de métodos"""
    print("\n" + "=" * 70)
    print("⚖️ DEMO: COMPARACIÓN DE MÉTODOS")
    print("=" * 70)

    # Buscar un archivo para comparar
    test_files = []
    for folder in ["documents/pdf", "documents/word", "documents/images"]:
        folder_path = Path(folder)
        if folder_path.exists():
            files = list(folder_path.glob("*.*"))
            test_files.extend(
                [f for f in files if f.suffix.lower() in ['.pdf', '.docx', '.pptx', '.jpg', '.jpeg', '.png']])

    if not test_files:
        print("📂 No hay archivos para comparar.")
        print("💡 Coloca un archivo en documents/ para probar esta función.")
        return

    test_file = test_files[0]
    print(f"🔬 Comparando métodos para: {test_file.name}")

    comparison_results = compare_ocr_methods(str(test_file), processor)

    print(f"\n📊 Resultados de la comparación:")
    for method, results in comparison_results["methods"].items():
        if results.get("success"):
            print(f"  ✅ {method.capitalize()}:")
            print(f"    • Caracteres: {results['character_count']:,}")
            print(f"    • Palabras: {results['word_count']:,}")
            print(f"    • Tipo: {results['processing_type']}")
        else:
            print(f"  ❌ {method.capitalize()}: Falló")

    if comparison_results["best_method"]:
        print(f"\n🏆 Mejor método: {comparison_results['best_method'].upper()}")

    if comparison_results["recommendations"]:
        print(f"\n💡 Recomendaciones:")
        for rec in comparison_results["recommendations"]:
            print(f"  • {rec}")


def performance_benchmark_demo(processor: MistralOCRProcessor):
    """Demo de benchmark de rendimiento"""
    print("\n" + "=" * 70)
    print("⏱️ DEMO: BENCHMARK DE RENDIMIENTO")
    print("=" * 70)

    # Recopilar archivos de prueba
    test_files = []
    for folder in ["documents/pdf", "documents/word", "documents/images"]:
        folder_path = Path(folder)
        if folder_path.exists():
            files = list(folder_path.glob("*.*"))
            test_files.extend([str(f) for f in files if f.suffix.lower() in ['.pdf', '.docx', '.jpg', '.jpeg', '.png']])

    # Limitar a máximo 3 archivos para el demo
    test_files = test_files[:3]

    if not test_files:
        print("📂 No hay archivos para el benchmark.")
        print("💡 Coloca algunos archivos en documents/ para probar esta función.")
        return

    print(f"🏁 Iniciando benchmark con {len(test_files)} archivos...")

    benchmark_results = performance_benchmark(processor, test_files)

    print(f"\n📊 Resultados del Benchmark:")
    print(f"  • Tiempo total: {benchmark_results['total_time']:.2f} segundos")
    print(f"  • Tiempo promedio: {benchmark_results['average_time']:.2f} segundos/archivo")
    print(f"  • Caracteres por segundo: {benchmark_results['characters_per_second']:.0f}")
    print(f"  • Palabras por segundo: {benchmark_results['words_per_second']:.1f}")

    print(f"\n📁 Detalles por archivo:")
    for result in benchmark_results["results"]:
        if result.get("success"):
            print(f"  ✅ {result['filename']}: {result['processing_time']:.2f}s "
                  f"({result['chars_per_second']:.0f} chars/s)")
        else:
            print(f"  ❌ {result['filename']}: Error")


def results_analysis_demo():
    """Demo de análisis de resultados guardados"""
    print("\n" + "=" * 70)
    print("📈 DEMO: ANÁLISIS DE RESULTADOS")
    print("=" * 70)

    # Analizar resultados existentes
    print("🔍 Analizando resultados guardados...")
    stats = analyze_ocr_results("results")

    if "error" in stats:
        print(f"❌ {stats['error']}")
        print("💡 Ejecuta primero algunos procesamientos OCR para generar resultados.")
        return

    print(f"📊 Estadísticas generales:")
    print(f"  • Total de archivos analizados: {stats['total_files']}")
    print(f"  • Total de caracteres: {stats['total_characters']:,}")
    print(f"  • Total de palabras: {stats['total_words']:,}")
    print(f"  • Promedio de palabras por archivo: {stats['total_words'] // max(stats['total_files'], 1):,}")

    print(f"\n📁 Archivos procesados:")
    for i, filename in enumerate(stats['files_processed'], 1):
        print(f"  {i}. {filename}")

    # Generar reporte completo
    print(f"\n📋 Generando reporte completo...")
    report_path = generate_ocr_report("results")
    if report_path:
        print(f"✅ Reporte guardado en: {report_path}")


def create_sample_files():
    """Crea archivos de muestra para testing"""
    print("\n" + "=" * 70)
    print("📝 CREANDO ARCHIVOS DE MUESTRA")
    print("=" * 70)

    # Crear carpetas si no existen
    Path("documents/samples").mkdir(parents=True, exist_ok=True)

    # URLs de documentos de muestra
    sample_urls = {
        "paper_nlp.pdf": "https://arxiv.org/pdf/2201.04234",
        "receipt.png": "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
    }

    print("🌐 Descargando archivos de muestra...")

    try:
        import requests

        for filename, url in sample_urls.items():
            file_path = Path("documents/samples") / filename

            if not file_path.exists():
                print(f"⬇️ Descargando {filename}...")
                response = requests.get(url)
                response.raise_for_status()

                with open(file_path, 'wb') as f:
                    f.write(response.content)

                print(f"✅ {filename} descargado")
            else:
                print(f"✅ {filename} ya existe")

        print(f"\n📁 Archivos de muestra creados en: documents/samples/")

    except ImportError:
        print("❌ Módulo 'requests' no disponible. Instala con: pip install requests")
    except Exception as e:
        print(f"❌ Error al descargar archivos: {e}")


def interactive_advanced_menu(processor: MistralOCRProcessor):
    """Menú interactivo avanzado con todas las funcionalidades"""
    while True:
        print("\n" + "=" * 70)
        print("🚀 MENÚ AVANZADO - MISTRAL OCR")
        print("=" * 70)
        print("📊 ANÁLISIS Y PROCESAMIENTO:")
        print("  1. 🔬 Análisis avanzado de texto")
        print("  2. 📦 Procesamiento en lote")
        print("  3. ⚖️ Comparación de métodos")
        print("  4. ⏱️ Benchmark de rendimiento")
        print("  5. 📈 Análisis de resultados guardados")
        print()
        print("🛠️ UTILIDADES:")
        print("  6. 📝 Crear archivos de muestra")
        print("  7. 🧹 Limpiar carpeta de resultados")
        print("  8. 📋 Generar reporte completo")
        print("  9. 🔍 Explorar archivo específico")
        print()
        print("📄 PROCESAMIENTO BÁSICO:")
        print("  10. 📄 Procesar PDF desde URL")
        print("  11. 🖼️ Procesar imagen desde URL")
        print("  12. 📁 Procesar archivo local")
        print()
        print("  0. ❌ Salir")
        print("-" * 70)

        try:
            choice = input("Selecciona una opción (0-12): ").strip()

            if choice == "0":
                print("👋 ¡Hasta luego!")
                break
            elif choice == "1":
                advanced_text_analysis_demo(processor)
            elif choice == "2":
                batch_processing_demo(processor)
            elif choice == "3":
                comparison_demo(processor)
            elif choice == "4":
                performance_benchmark_demo(processor)
            elif choice == "5":
                results_analysis_demo()
            elif choice == "6":
                create_sample_files()
            elif choice == "7":
                clean_results_folder()
            elif choice == "8":
                generate_complete_report()
            elif choice == "9":
                explore_specific_file(processor)
            elif choice == "10":
                demo_pdf_url_processing(processor)
            elif choice == "11":
                demo_image_url_processing(processor)
            elif choice == "12":
                demo_local_file_processing(processor)
            else:
                print("❌ Opción no válida. Selecciona un número del 0 al 12.")

        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

        # Pausa para que el usuario pueda leer los resultados
        input("\n⏸️ Presiona Enter para continuar...")


def clean_results_folder():
    """Limpia la carpeta de resultados"""
    print("\n" + "=" * 70)
    print("🧹 LIMPIAR CARPETA DE RESULTADOS")
    print("=" * 70)

    results_path = Path("results")

    if not results_path.exists():
        print("📁 La carpeta 'results' no existe.")
        return

    files = list(results_path.glob("*.*"))

    if not files:
        print("📁 La carpeta 'results' ya está vacía.")
        return

    print(f"📁 Se encontraron {len(files)} archivos en 'results':")
    for file in files:
        print(f"  • {file.name}")

    confirm = input("\n❓ ¿Estás seguro de que quieres eliminar todos los archivos? (s/N): ").strip().lower()

    if confirm in ['s', 'sí', 'si', 'y', 'yes']:
        try:
            for file in files:
                file.unlink()
            print("✅ Carpeta de resultados limpiada correctamente.")
        except Exception as e:
            print(f"❌ Error al limpiar carpeta: {e}")
    else:
        print("❌ Operación cancelada.")


def generate_complete_report():
    """Genera un reporte completo de todo el sistema"""
    print("\n" + "=" * 70)
    print("📋 GENERAR REPORTE COMPLETO")
    print("=" * 70)

    try:
        # Generar reporte principal
        report_path = generate_ocr_report("results")

        if report_path:
            print(f"✅ Reporte principal generado: {report_path}")

        # Estadísticas adicionales
        stats = analyze_ocr_results("results")

        if "error" not in stats:
            print(f"📊 Estadísticas incluidas en el reporte:")
            print(f"  • {stats['total_files']} archivos analizados")
            print(f"  • {stats['total_characters']:,} caracteres totales")
            print(f"  • {stats['total_words']:,} palabras totales")

        print(f"\n💡 El reporte completo está disponible en: {report_path}")

    except Exception as e:
        print(f"❌ Error al generar reporte: {e}")


def explore_specific_file(processor: MistralOCRProcessor):
    """Explora un archivo específico en detalle"""
    print("\n" + "=" * 70)
    print("🔍 EXPLORAR ARCHIVO ESPECÍFICO")
    print("=" * 70)

    # Mostrar archivos disponibles
    all_files = []
    for folder in ["documents/pdf", "documents/word", "documents/images", "documents/samples"]:
        folder_path = Path(folder)
        if folder_path.exists():
            files = list(folder_path.rglob("*.*"))
            supported_files = [f for f in files if
                               f.suffix.lower() in ['.pdf', '.docx', '.pptx', '.jpg', '.jpeg', '.png', '.avif']]
            all_files.extend(supported_files)

    if not all_files:
        print("📁 No se encontraron archivos soportados.")
        print("💡 Coloca algunos archivos en las carpetas documents/")
        return

    print(f"📁 Archivos disponibles:")
    for i, file_path in enumerate(all_files, 1):
        size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"  {i}. {file_path.name} ({size_mb:.2f} MB) - {file_path.parent}")

    try:
        choice = int(input(f"\nSelecciona un archivo (1-{len(all_files)}): "))

        if 1 <= choice <= len(all_files):
            selected_file = all_files[choice - 1]

            print(f"\n🔍 Explorando: {selected_file.name}")
            print(f"📁 Ubicación: {selected_file}")
            print(f"📏 Tamaño: {selected_file.stat().st_size / (1024 * 1024):.2f} MB")

            # Procesar archivo
            print(f"\n🔄 Procesando archivo...")
            start_time = time.time()

            response = processor.process_local_file(str(selected_file))

            end_time = time.time()
            processing_time = end_time - start_time

            if response:
                # Guardar resultado
                result_filename = f"explore_{selected_file.stem}_ocr.json"
                processor.save_results(response, result_filename)

                # Análisis detallado
                text_content = processor.extract_text_content(response)
                analysis = processor.analyze_document_structure(response)
                structured_data = extract_structured_data(text_content)

                print(f"\n📊 Análisis completo:")
                print(f"  • Tiempo de procesamiento: {processing_time:.2f} segundos")
                print(f"  • Caracteres extraídos: {len(text_content):,}")
                print(f"  • Palabras extraídas: {len(text_content.split()):,}")
                print(f"  • Líneas: {len(text_content.split('\\n')):,}")

                # Mostrar datos estructurados encontrados
                print(f"\n🔍 Datos estructurados encontrados:")
                for data_type, items in structured_data.items():
                    if items:
                        print(f"  • {data_type.capitalize()}: {len(items)}")

                # Mostrar muestra del texto
                print(f"\n📝 Muestra del texto extraído (primeros 300 caracteres):")
                print("-" * 50)
                print(text_content[:300] + "..." if len(text_content) > 300 else text_content)

                print(f"\n💾 Resultado guardado en: {result_filename}")

            else:
                print("❌ No se pudo procesar el archivo.")

        else:
            print("❌ Selección no válida.")

    except ValueError:
        print("❌ Por favor, introduce un número válido.")
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_pdf_url_processing(processor: MistralOCRProcessor):
    """Demo simple de procesamiento de PDF desde URL"""
    print("\n🔄 Procesando PDF desde URL...")

    pdf_url = "https://arxiv.org/pdf/2201.04234"
    response = processor.process_document_from_url(pdf_url, "document_url")

    if response:
        processor.save_results(response, "demo_pdf_url.json")
        text = processor.extract_text_content(response)
        print(f"✅ PDF procesado: {len(text.split())} palabras extraídas")
        print(f"📝 Primeros 200 caracteres: {text[:200]}...")
    else:
        print("❌ Error al procesar PDF")


def demo_image_url_processing(processor: MistralOCRProcessor):
    """Demo simple de procesamiento de imagen desde URL"""
    print("\n🔄 Procesando imagen desde URL...")

    image_url = "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
    response = processor.process_document_from_url(image_url, "image_url")

    if response:
        processor.save_results(response, "demo_image_url.json")
        text = processor.extract_text_content(response)
        print(f"✅ Imagen procesada: {len(text.split())} palabras extraídas")
        print(f"📝 Texto extraído: {text}")
    else:
        print("❌ Error al procesar imagen")


def demo_local_file_processing(processor: MistralOCRProcessor):
    """Demo simple de procesamiento de archivo local"""
    # Buscar archivos disponibles
    all_files = []
    for folder in ["documents/pdf", "documents/word", "documents/images", "documents/samples"]:
        folder_path = Path(folder)
        if folder_path.exists():
            files = list(folder_path.rglob("*.*"))
            supported_files = [f for f in files if
                               f.suffix.lower() in ['.pdf', '.docx', '.pptx', '.jpg', '.jpeg', '.png', '.avif']]
            all_files.extend(supported_files)

    if not all_files:
        print("❌ No hay archivos locales para procesar")
        print("💡 Coloca algunos archivos en las carpetas documents/")
        return

    file_to_process = all_files[0]
    print(f"\n🔄 Procesando archivo local: {file_to_process.name}")

    response = processor.process_local_file(str(file_to_process))

    if response:
        processor.save_results(response, f"demo_local_{file_to_process.stem}.json")
        text = processor.extract_text_content(response)
        print(f"✅ Archivo procesado: {len(text.split())} palabras extraídas")
        print(f"📝 Primeros 200 caracteres: {text[:200]}...")
    else:
        print("❌ Error al procesar archivo local")


def main_advanced():
    """Función principal del demo avanzado"""
    print("🚀 DEMO AVANZADO DE MISTRAL OCR")
    print("=" * 70)
    print("Este demo incluye todas las funcionalidades avanzadas:")
    print("• Análisis de texto estructurado")
    print("• Procesamiento en lote")
    print("• Comparación de métodos")
    print("• Benchmarking de rendimiento")
    print("• Generación de reportes")
    print("• Y mucho más...")
    print("=" * 70)

    try:
        # Inicializar procesador
        processor = MistralOCRProcessor()

        # Mostrar menú avanzado
        interactive_advanced_menu(processor)

    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("\n🔧 Para solucionar:")
        print("1. Crea un archivo .env en la raíz del proyecto")
        print("2. Añade tu API key: MISTRAL_API_KEY=tu_api_key_aqui")
        print("3. Obtén tu API key en: https://console.mistral.ai/")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main_advanced()