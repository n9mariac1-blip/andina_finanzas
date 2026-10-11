# Distribuciones Andina Comercial S.A.S. — Dashboard Financiero Ejecutivo (2021–2025)

Sistema de inteligencia financiera, analítica de rentabilidad y visualización interactiva desarrollado para la Junta Directiva y Alta Dirección de **Distribuciones Andina Comercial S.A.S.**

---

## 🌟 Características Principales del Dashboard

1. **Scorecard Ejecutivo C-Suite:**
   - Métricas clave en tiempo real: Ingresos, EBITDA, Utilidad Neta, ROE, Deuda Neta/EBITDA y Ciclo de Conversión de Efectivo (CCC).
   - Semáforo de salud financiera multidimensional (Rentabilidad, Eficiencia Operativa, Liquidez y Estructura de Capital).
   - Comparativas interanuales automáticas (YoY) y variaciones absolutas/porcentuales.

2. **Estado de Resultados Integral (P&L):**
   - Gráfico de cascada (*Waterfall chart*) interactivo desde Ingresos hasta Utilidad Neta.
   - Análisis de comportamiento de márgenes: Margen Bruto (25.0% estable), expansión de Margen EBITDA (8.7% a 10.5%) y Margen Neto (3.7% a 5.6%).
   - Análisis vertical de estructura de costos y gastos operativos (% sobre ventas).

3. **Balance General, Liquidez & Estructura de Capital:**
   - Descomposición visual de Activos, Pasivos y Patrimonio.
   - Indicadores de liquidez: Razón Corriente (1.92x a 2.14x), Prueba Ácida (1.05x a 1.41x) y Razón de Efectivo (0.06x a 0.63x).
   - Evolución de reservas patrimoniales y resultados acumulados.

4. **Capital de Trabajo y Ciclo de Conversión de Efectivo (CCC):**
   - Diagnóstico del punto de inflexión del caso: En 2021 la empresa *vendía sin generar caja* debido a un ciclo de 75 días.
   - Reducción del ciclo a **56 días en 2025** (-19 días):
     - Días de cartera (DSO): de 50 a 43 días.
     - Días de inventario (DIO): de 65 a 58 días.
     - Días de proveedores (DPO): de 40 a 45 días.
   - Productividad del Capital de Trabajo (PKT) mejoró del 18.84% al 14.45% de las ventas.
   - Cuantificación de caja liberada: **+$7,315 Millones COP**.

5. **Flujo de Caja, CAPEX y Dinámica de Deuda:**
   - Descomposición de Flujo Operativo (CFO), Inversión (CFI / CAPEX) y Financiación (CFF).
   - El Flujo de Caja Libre Operativo pasó de -$288M en 2021 a +$4,288M en 2025.
   - Desapalancamiento neto acelerado: El ratio Deuda Neta / EBITDA colapsó de 1.69x a **0.51x**.
   - Crecimiento de dividendos decretados con payout del 35%.

6. **Descomposición DuPont:**
   - Desagregación matemática del ROE (que escaló de 16.58% a 21.14%) demostrando que fue impulsado por la expansión del margen neto y no por apalancamiento riesgoso.

7. **Simulador Gerencial "What-If" (Proyecciones 2026):**
   - Herramienta predictiva con sliders para simular crecimiento de ventas, margen bruto, metas de días de capital de trabajo, presupuesto de CAPEX y dividendos.

8. **Diagnóstico Estratégico & Business Model Canvas B2B:**
   - Integración cualitativa completa de los 9 bloques del Canvas para el modelo B2B de seguridad electrónica y herramientas.
   - Recomendaciones estratégicas para la Junta Directiva.

---

## 🚀 Cómo Ejecutar la Aplicación

Asegúrate de contar con Python 3.10+ y los paquetes listados en los requerimientos.

```bash
# Iniciar el servidor de Streamlit
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado en `http://localhost:8501`.

---

## 📁 Estructura del Proyecto

```text
andina_finanzas/
├── ARCHIVOS/
│   ├── balance_general.xlsx              # Estados de balance 2021-2025
│   ├── estado_de_resultados.xlsx         # P&L histórico 2021-2025
│   ├── estado_flujo_efectivo.xlsx        # Flujo de efectivo método indirecto
│   └── Caso Distribuciones Andina...docx # Documento de estudio cualitativo
├── app.py                                # Aplicación principal Streamlit
├── data_loader.py                        # Módulo de procesamiento y cálculo financiero
├── README.md                             # Documentación técnica y gerencial
```
