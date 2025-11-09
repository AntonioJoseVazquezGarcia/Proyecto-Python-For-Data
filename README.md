# Proyecto-Python-For-Data
Ejercicio práctico sobre el tratamiento de datos con Python


# Proyecto EDA con Python: Análisis de Campañas de Marketing Bancario

# 🎯 Objetivo del Proyecto

Este proyecto consiste en la aplicación de técnicas de **Análisis Exploratorio de Datos (EDA)** 
utilizando **Python** para investigar y extraer conclusiones significativas de conjuntos de datos relacionados
con campañas de marketing directo de una institución bancaria portuguesa. 
El foco está en identificar los factores que influyen en la suscripción de un depósito a plazo por parte de los clientes.

---

# ⚙️ Requisitos y Dependencias

Para ejecutar el análisis es necesario contar con un entorno de Python configurado.

# Herramientas Obligatorias (Según Enunciado)
* Python
* Pandas
* Visual Studio Code (o cualquier IDE de preferencia)

# Librerías de Python
Las dependencias requeridas para ejecutar el script `Proyecto Python for Data.02.py` son:

```bash
pandas
numpy
matplotlib
seaborn
openpyxl  # Para leer archivos .xlsx

# Puedes instalarlas usando pip:

pip install pandas numpy matplotlib seaborn openpyxl

# 📂 Estructura del Proyecto
El repositorio debe seguir la siguiente estructura, conforme a los requisitos de entrega:
/
├── README.md                           (Este archivo con el resumen y las instrucciones)
├── Proyecto Python for Data.02.py      (Script principal con el EDA)
├── DatosProyecto/
│   ├── bank-additional.csv             (Datos de campañas en bruto)
│   └── customer-details.xlsx           (Datos de clientes en bruto)
└── Informes/
    └── Informe_Analisis_Explicativo.docx (Plantilla o archivo final con los resultados y figuras)

# 🚀 Instrucciones de Ejecución
  1.- Clonar el Repositorio:

Bash

git clone [(https://github.com/AntonioJoseVazquezGarcia/Proyecto-Python-For-Data/tree/main)]

  2.- Configurar el Entorno: Asegúrate de que todas las Dependencias estén instaladas.

  3.- Colocar los Datos: Asegúrate de que los archivos bank-additional.csv y customer-details.xlsx se encuentren dentro de la carpeta /DatosProyecto.

Nota Importante sobre Rutas: El script utiliza rutas relativas (./DatosProyecto/...). Si la estructura de carpetas es diferente, las rutas en el archivo .py deben ajustarse.


Nota Importante sobre el CSV (Añadido por sugerencia del reporte): El archivo bank-additional.csv se lee explícitamente usando el separador de coma (sep=',')
en lugar de punto y coma, garantizando que todas las columnas se carguen correctamente.

  4.- Ejecutar el Análisis: Ejecuta el script principal desde tu terminal o IDE:

Bash

python "Proyecto Python for Data.02.py"
El script cargará, transformará, limpiará y analizará los datos, imprimiendo el resumen estadístico y las tasas de suscripción en la consola.
Además, generará las tres figuras visualizadas (Tasa por Ocupación, Impacto de Campaña e Ingresos vs. Suscripción).


# 🔍 Principales Hallazgos (Insights)


El análisis exploratorio reveló los siguientes patrones y conclusiones operacionales, que deben ser la base del informe explicativo final:

  1.- Influencia de la Duración de la Llamada: Existe una relación positiva significativa entre la duration (duración del último contacto)
       y la conversión (y). Aclaración: Este insight es útil para el EDA, pero la variable duration no debe usarse en modelos predictivos al ser conocida a posteriori.

  2.- Contexto Macroeconómico: Las variables macroeconómicas como euribor3m (tasa de interés) y nr.employed (número de empleados) muestran
       una relación negativa con la tasa de suscripción (y). Esto sugiere que la eficiencia de la campaña es inversamente proporcional a la fortaleza del ciclo económico.

  3.- Eficiencia Operacional de Campaña: La tasa de suscripción cae notablemente a partir de un umbral específico de contactos en la campaña (campaign).

      Recomendación Operacional: Se recomienda no superar 3 ó 4 contactos por cliente, ya que el esfuerzo adicional genera una
       conversión marginal decreciente.

  4.- Segmentación por Demografía: Se observaron diferencias claras en la tasa de suscripción según el estado civil y la ocupación:

      Estado Civil: El segmento 'desconocido' o 'viudo(a)' presenta las tasas más altas, mientras que los 'casados' muestran una tasa inferior.

      Ocupación: El top de suscripción se encuentra en los segmentos 'student' y 'retired', mientras que ocupaciones como 'services' o 'blue-collar'
    tienen las tasas más bajas (incluir porcentajes específicos del output).





