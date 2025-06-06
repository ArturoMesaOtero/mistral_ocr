"""
Utilidades adicionales para el proyecto Mistral OCR
Funciones helper para análisis y procesamiento
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def analyze_ocr_results(results_folder: str = "results") -> Dict[str, Any]:
    """
    Analiza todos los resultados OCR guardados

    Args:
        results_folder (str): Carpeta con los resultados

    Returns:
        dict: Estadísticas generales
    """
    results_path = Path(results_folder)

    if not results_path.exists():
        return {"error": "Carpeta de resultados no existe"}

    json_files = list(results_path.glob("*.json"))

    if not json_files:
        return {"error": "No se encontraron archivos de resultados"}

    stats = {
        "total_files": len(json_files),
        "total_characters": 0,
        "total_words": 0,
        "document_types": {},
        "processing_dates": [],
        "files_processed": []
    }

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extraer texto
            text_content = extract_text_from_result(data)

            if text_content:
                stats["total_characters"] += len(text_content)
                stats["total_words"] += len(text_content.split())

            stats["files_processed"].append(json_file.name)

        except Exception as e:
            print(f"Error al analizar {json_file}: {e}")

    return stats


def extract_text_from_result(result_data: Dict[str, Any]) -> str:
    """
    Extrae texto de un resultado OCR guardado

    Args:
        result_data (dict): Datos del resultado OCR

    Returns:
        str: Texto extraído
    """
    # Buscar texto en diferentes ubicaciones posibles
    if 'content' in result_data:
        if isinstance(result_data['content'], dict) and 'text' in result_data['content']:
            return result_data['content']['text']
        elif isinstance(result_data['content'], str):
            return result_data['content']

    if 'text' in result_data:
        return result_data['text']

    # Buscar recursivamente
    def find_text(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'text' and isinstance(value, str):
                    return value
                result = find_text(value)
                if result:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = find_text(item)
                if result:
                    return result
        return None

    return find_text(result_data) or ""


def create_word_cloud(text: str, output_path: str = "results/wordcloud.png"):
    """
    Crea una nube de palabras del texto extraído

    Args:
        text (str): Texto para la nube de palabras
        output_path (str): Ruta de salida
    """
    try:
        # Limpiar texto
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        clean_text = re.sub(r'\s+', ' ', clean_text)

        # Crear nube de palabras
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=100,
            colormap='viridis'
        ).generate(clean_text)

        # Guardar imagen
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Nube de Palabras - Texto Extraído por OCR')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✅ Nube de palabras guardada en: {output_path}")

    except Exception as e:
        print(f"❌ Error al crear nube de palabras: {e}")


def generate_ocr_report(results_folder: str = "results") -> str:
    """
    Genera un reporte completo de todos los análisis OCR

    Args:
        results_folder (str): Carpeta con los resultados

    Returns:
        str: Ruta del reporte generado
    """
    report_path = Path(results_folder) / "ocr_analysis_report.md"

    try:
        stats = analyze_ocr_results(results_folder)

        if "error" in stats:
            return f"Error: {stats['error']}"

        # Generar reporte en Markdown
        report_content = f"""# 📊 Reporte de Análisis OCR - Mistral Document AI

## 📈 Estadísticas Generales

- **Total de archivos procesados**: {stats['total_files']}
- **Total de caracteres extraídos**: {stats['total_characters']:,}
- **Total de palabras extraídas**: {stats['total_words']:,}
- **Promedio de palabras por documento**: {stats['total_words'] // max(stats['total_files'], 1):,}

## 📁 Archivos Procesados

"""

        for i, filename in enumerate(stats['files_processed'], 1):
            report_content += f"{i}. `{filename}`\n"

        report_content += f"""

## 🔧 Información Técnica

- **Modelo utilizado**: mistral-ocr-latest
- **Fecha del análisis**: {Path().cwd()}
- **Formatos soportados**: PDF, DOCX, PPTX, PNG, JPEG, AVIF

## 💡 Recomendaciones

1. Para documentos con muchas imágenes, considera usar `include_image_base64=True`
2. Los archivos grandes (>10MB) pueden tardar más en procesarse
3. Para mejor precisión, usa imágenes con alta resolución
4. Los documentos estructurados (tablas, listas) se preservan en formato markdown

---
*Reporte generado automáticamente por MistralOCRProcessor*
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"📋 Reporte generado en: {report_path}")
        return str(report_path)

    except Exception as e:
        print(f"❌ Error al generar reporte: {e}")
        return ""


def compare_ocr_methods(file_path: str, processor) -> Dict[str, Any]:
    """
    Compara diferentes métodos de procesamiento OCR para el mismo archivo

    Args:
        file_path (str): Ruta del archivo a comparar
        processor: Instancia de MistralOCRProcessor

    Returns:
        dict: Comparación de métodos
    """
    print(f"🔍 Comparando métodos OCR para: {file_path}")

    comparison = {
        "file": file_path,
        "methods": {},
        "best_method": None,
        "recommendations": []
    }

    try:
        # Método 1: Procesamiento local
        print("📁 Probando método local...")
        local_response = processor.process_local_file(file_path)
        if local_response:
            local_text = processor.extract_text_content(local_response)
            comparison["methods"]["local"] = {
                "success": True,
                "character_count": len(local_text),
                "word_count": len(local_text.split()),
                "processing_type": "Base64 encoding"
            }
        else:
            comparison["methods"]["local"] = {"success": False}

        # Método 2: Subida de archivo
        print("☁️ Probando método de subida...")
        upload_response = processor.upload_and_process_file(file_path)
        if upload_response:
            upload_text = processor.extract_text_content(upload_response)
            comparison["methods"]["upload"] = {
                "success": True,
                "character_count": len(upload_text),
                "word_count": len(upload_text.split()),
                "processing_type": "File upload"
            }
        else:
            comparison["methods"]["upload"] = {"success": False}

        # Determinar el mejor método
        successful_methods = {k: v for k, v in comparison["methods"].items() if v.get("success")}

        if successful_methods:
            best_method = max(successful_methods.items(), key=lambda x: x[1].get("character_count", 0))
            comparison["best_method"] = best_method[0]

            # Generar recomendaciones
            if len(successful_methods) > 1:
                comparison["recommendations"].append("Ambos métodos funcionaron correctamente")

            file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
            if file_size_mb > 10:
                comparison["recommendations"].append(
                    "Para archivos grandes, el método de subida puede ser más eficiente")
            else:
                comparison["recommendations"].append("Para archivos pequeños, el método local es más rápido")

        return comparison

    except Exception as e:
        print(f"❌ Error en comparación: {e}")
        comparison["error"] = str(e)
        return comparison


def extract_structured_data(text: str) -> Dict[str, List[str]]:
    """
    Extrae datos estructurados del texto OCR

    Args:
        text (str): Texto extraído por OCR

    Returns:
        dict: Datos estructurados extraídos
    """
    structured_data = {
        "emails": [],
        "phones": [],
        "urls": [],
        "dates": [],
        "numbers": [],
        "headers": []
    }

    try:
        # Expresiones regulares para diferentes tipos de datos
        patterns = {
            "emails": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phones": r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            "urls": r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            "dates": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
            "numbers": r'\b\d+\.?\d*\b'
        }

        for data_type, pattern in patterns.items():
            matches = re.findall(pattern, text)
            structured_data[data_type] = list(set(matches))  # Eliminar duplicados

        # Extraer headers (líneas que empiezan con # en markdown)
        headers = re.findall(r'^#+\s*(.+)$', text, re.MULTILINE)
        structured_data["headers"] = headers

        return structured_data

    except Exception as e:
        print(f"❌ Error al extraer datos estructurados: {e}")
        return structured_data


def batch_process_folder(folder_path: str, processor) -> Dict[str, Any]:
    """
    Procesa todos los archivos de una carpeta en lote

    Args:
        folder_path (str): Ruta de la carpeta
        processor: Instancia de MistralOCRProcessor

    Returns:
        dict: Resultados del procesamiento en lote
    """
    print(f"📂 Procesando carpeta en lote: {folder_path}")

    folder = Path(folder_path)
    if not folder.exists():
        return {"error": f"La carpeta {folder_path} no existe"}

    # Extensiones soportadas
    supported_extensions = ['.pdf', '.docx', '.pptx', '.jpg', '.jpeg', '.png', '.avif']
    files_to_process = []

    for ext in supported_extensions:
        files_to_process.extend(folder.glob(f"*{ext}"))
        files_to_process.extend(folder.glob(f"*{ext.upper()}"))

    if not files_to_process:
        return {"error": "No se encontraron archivos soportados en la carpeta"}

    batch_results = {
        "total_files": len(files_to_process),
        "processed_files": 0,
        "failed_files": 0,
        "results": [],
        "summary": {
            "total_characters": 0,
            "total_words": 0,
            "processing_errors": []
        }
    }

    print(f"📋 Encontrados {len(files_to_process)} archivos para procesar")

    for i, file_path in enumerate(files_to_process, 1):
        print(f"🔄 Procesando {i}/{len(files_to_process)}: {file_path.name}")

        try:
            response = processor.process_local_file(str(file_path))

            if response:
                # Guardar resultado individual
                result_filename = f"batch_{file_path.stem}_ocr.json"
                processor.save_results(response, result_filename)

                # Extraer texto y análisis
                text_content = processor.extract_text_content(response)
                analysis = processor.analyze_document_structure(response)

                file_result = {
                    "filename": file_path.name,
                    "success": True,
                    "character_count": len(text_content),
                    "word_count": len(text_content.split()),
                    "analysis": analysis,
                    "result_file": result_filename
                }

                batch_results["results"].append(file_result)
                batch_results["processed_files"] += 1
                batch_results["summary"]["total_characters"] += len(text_content)
                batch_results["summary"]["total_words"] += len(text_content.split())

            else:
                batch_results["failed_files"] += 1
                batch_results["summary"]["processing_errors"].append(f"Error procesando {file_path.name}")

        except Exception as e:
            print(f"❌ Error procesando {file_path.name}: {e}")
            batch_results["failed_files"] += 1
            batch_results["summary"]["processing_errors"].append(f"{file_path.name}: {str(e)}")

    # Generar reporte de lote
    generate_batch_report(batch_results)

    return batch_results


def generate_batch_report(batch_results: Dict[str, Any]) -> str:
    """
    Genera un reporte del procesamiento en lote

    Args:
        batch_results (dict): Resultados del lote

    Returns:
        str: Ruta del reporte
    """
    report_path = Path("results") / "batch_processing_report.md"

    try:
        report_content = f"""# 📊 Reporte de Procesamiento en Lote

## 📈 Resumen General

- **Total de archivos**: {batch_results['total_files']}
- **Archivos procesados exitosamente**: {batch_results['processed_files']}
- **Archivos con errores**: {batch_results['failed_files']}
- **Tasa de éxito**: {(batch_results['processed_files'] / max(batch_results['total_files'], 1) * 100):.1f}%

## 📊 Estadísticas de Contenido

- **Total de caracteres extraídos**: {batch_results['summary']['total_characters']:,}
- **Total de palabras extraídas**: {batch_results['summary']['total_words']:,}
- **Promedio de palabras por archivo**: {batch_results['summary']['total_words'] // max(batch_results['processed_files'], 1):,}

## 📁 Archivos Procesados

"""

        for result in batch_results['results']:
            if result['success']:
                report_content += f"""### ✅ {result['filename']}
- **Caracteres**: {result['character_count']:,}
- **Palabras**: {result['word_count']:,}
- **Archivo de resultado**: `{result['result_file']}`

"""

        if batch_results['summary']['processing_errors']:
            report_content += "## ❌ Errores de Procesamiento\n\n"
            for error in batch_results['summary']['processing_errors']:
                report_content += f"- {error}\n"

        report_content += f"""

## 🔧 Detalles Técnicos

- **Modelo OCR**: mistral-ocr-latest
- **Método de procesamiento**: Local (Base64)
- **Formatos procesados**: PDF, DOCX, PPTX, imágenes

---
*Reporte generado automáticamente*
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"📋 Reporte de lote guardado en: {report_path}")
        return str(report_path)

    except Exception as e:
        print(f"❌ Error al generar reporte de lote: {e}")
        return ""


def performance_benchmark(processor, test_files: List[str]) -> Dict[str, Any]:
    """
    Realiza un benchmark de rendimiento del OCR

    Args:
        processor: Instancia de MistralOCRProcessor
        test_files (list): Lista de archivos para probar

    Returns:
        dict: Resultados del benchmark
    """
    import time

    benchmark_results = {
        "test_files": len(test_files),
        "results": [],
        "average_time": 0,
        "total_time": 0,
        "characters_per_second": 0,
        "words_per_second": 0
    }

    total_time = 0
    total_characters = 0
    total_words = 0

    print(f"⏱️ Iniciando benchmark con {len(test_files)} archivos...")

    for i, file_path in enumerate(test_files, 1):
        print(f"🔄 Benchmark {i}/{len(test_files)}: {Path(file_path).name}")

        start_time = time.time()

        try:
            response = processor.process_local_file(file_path)

            end_time = time.time()
            processing_time = end_time - start_time

            if response:
                text_content = processor.extract_text_content(response)
                char_count = len(text_content)
                word_count = len(text_content.split())

                file_result = {
                    "filename": Path(file_path).name,
                    "processing_time": processing_time,
                    "character_count": char_count,
                    "word_count": word_count,
                    "chars_per_second": char_count / processing_time if processing_time > 0 else 0,
                    "success": True
                }

                total_time += processing_time
                total_characters += char_count
                total_words += word_count

            else:
                file_result = {
                    "filename": Path(file_path).name,
                    "processing_time": processing_time,
                    "success": False
                }

            benchmark_results["results"].append(file_result)

        except Exception as e:
            print(f"❌ Error en benchmark para {file_path}: {e}")
            file_result = {
                "filename": Path(file_path).name,
                "error": str(e),
                "success": False
            }
            benchmark_results["results"].append(file_result)

    # Calcular estadísticas finales
    successful_results = [r for r in benchmark_results["results"] if r.get("success")]

    if successful_results:
        benchmark_results["average_time"] = total_time / len(successful_results)
        benchmark_results["total_time"] = total_time
        benchmark_results["characters_per_second"] = total_characters / total_time if total_time > 0 else 0
        benchmark_results["words_per_second"] = total_words / total_time if total_time > 0 else 0

    print(f"⏱️ Benchmark completado en {total_time:.2f} segundos")

    return benchmark_results