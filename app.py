"""
=============================================================================
DISTRIBUCIONES ANDINA COMERCIAL S.A.S.
DASHBOARD FINANCIERO Y ESTRATÉGICO EJECUTIVO (2021 - 2025)
Desarrollado por: Analista Financiero Senior & Especialista en Visualización
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

from data_loader import load_and_process_financial_data

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Andina Comercial | Dashboard Financiero",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (ESTÉTICA CORPORATIVA PREMIUM FINTECH)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Estructura general */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F284E 100%);
        padding: 24px 32px;
        border-radius: 14px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .main-header h1 {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        color: #F8FAFC;
    }
    .main-header p {
        font-size: 14px;
        color: #94A3B8;
        margin: 6px 0 0 0;
        font-weight: 400;
    }
    .badge-tag {
        display: inline-block;
        background: rgba(14, 165, 233, 0.15);
        color: #38BDF8;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* Tarjetas KPI */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 12px;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
    }
    .kpi-title {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 6px;
    }
    .kpi-sub {
        font-size: 12px;
        font-weight: 500;
    }
    .kpi-pos {
        color: #10B981;
    }
    .kpi-neg {
        color: #EF4444;
    }
    .kpi-neu {
        color: #64748B;
    }

    /* Tarjetas de Diagnóstico */
    .health-card {
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        border-left: 5px solid;
    }
    .health-green {
        background-color: #F0FDF4;
        border-color: #22C55E;
        color: #14532D;
    }
    .health-blue {
        background-color: #EFF6FF;
        border-color: #3B82F6;
        color: #1E3A8A;
    }
    .health-amber {
        background-color: #FFFBEB;
        border-color: #F59E0B;
        color: #78350F;
    }
    
    /* Contenedor Canvas */
    .canvas-box {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 14px;
        height: 100%;
        min-height: 200px;
    }
    .canvas-header {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        color: #1E293B;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 6px;
        margin-bottom: 10px;
    }
    
    /* Tabs personalizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CARGA DE DATOS CON CACHÉ
# -----------------------------------------------------------------------------
@st.cache_data
def get_data():
    return load_and_process_financial_data()

try:
    fin_data = get_data()
except Exception as e:
    st.error(f"Error cargando los datos financieros: {str(e)}")
    st.stop()

years = fin_data['years']
summary_df = fin_data['summary']
er_table = fin_data['er_table']
bg_table = fin_data['bg_table']
cfs_table = fin_data['cfs_table']
arr = fin_data['arrays']

# Colores de la paleta corporativa
NAVY_PRIMARY = "#0F284E"
BLUE_ACCENT = "#2563EB"
TEAL_SUCCESS = "#10B981"
AMBER_WARNING = "#F59E0B"
RED_ALERT = "#EF4444"
SLATE_GRAY = "#64748B"
PURPLE_ACCENT = "#8B5CF6"

# -----------------------------------------------------------------------------
# SIDEBAR: CONTROLES & NAVEGACIÓN
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
    st.markdown("### **Distribuciones Andina Comercial S.A.S.**")
    st.caption("NIT: 900.845.120-4 | Sector: B2B Distribución & Logística")
    st.markdown("---")
    
    selected_year = st.selectbox(
        "📅 **Año de Análisis Focal:**",
        years,
        index=len(years) - 1,
        help="Seleccione el periodo contable principal para cálculos, KPIs y comparativas."
    )
    y_idx = years.index(selected_year)
    prev_idx = y_idx - 1 if y_idx > 0 else None
    
    st.markdown("---")
    st.markdown("##### 📌 **Resumen Rápido del Año**")
    st.metric(
        "Ventas Totales",
        f"${arr['rev'][y_idx]:,.0f}M",
        f"{((arr['rev'][y_idx]/arr['rev'][prev_idx]-1)*100):+.1f}% YoY" if prev_idx is not None else "Año Base"
    )
    st.metric(
        "EBITDA Operativo",
        f"${arr['ebitda'][y_idx]:,.0f}M",
        f"{((arr['ebitda'][y_idx]/arr['ebitda'][prev_idx]-1)*100):+.1f}% YoY" if prev_idx is not None else "Año Base"
    )
    st.metric(
        "Ciclo de Caja (CCC)",
        f"{arr['ccc'][y_idx]:.0f} días",
        f"{(arr['ccc'][y_idx] - arr['ccc'][prev_idx]):+.1f} d" if prev_idx is not None else "Año Base",
        delta_color="inverse"
    )
    
    st.markdown("---")
    st.markdown("##### 📥 **Descarga de Estados Financieros**")
    
    # Botón de exportación a Excel
    output_buffer = io.BytesIO()
    with pd.ExcelWriter(output_buffer, engine='openpyxl') as writer:
        summary_df.to_excel(writer, sheet_name='KPIs_Consolidado', index=False)
        er_table.to_excel(writer, sheet_name='Estado_Resultados', index=False)
        bg_table.to_excel(writer, sheet_name='Balance_General', index=False)
        cfs_table.to_excel(writer, sheet_name='Flujo_Efectivo', index=False)
    excel_bytes = output_buffer.getvalue()
    
    st.download_button(
        label="📊 Descargar Modelo Completo (.xlsx)",
        data=excel_bytes,
        file_name="Andina_Comercial_Modelo_Financiero_2021_2025.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    
    st.markdown("---")
    st.caption("Desarrollado para: Junta Directiva & Alta Dirección")
    st.caption("Cifras expresadas en Millones de Pesos Colombianos ($ COP M)")

# -----------------------------------------------------------------------------
# HEADER PRINCIPAL
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1>DISTRIBUCIONES ANDINA COMERCIAL S.A.S.</h1>
            <p>PANEL INTEGRADO DE INTELIGENCIA FINANCIERA, RENTABILIDAD Y DIAGNÓSTICO ESTRATÉGICO (2021–2025)</p>
            <div class="badge-tag">B2B Distribución de Tecnología, Seguridad y Herramientas | Colombia</div>
        </div>
        <div style="text-align: right; margin-top: 10px;">
            <div style="font-size: 13px; color: #94A3B8;">PERIODO FOCAL SELECCIONADO</div>
            <div style="font-size: 32px; font-weight: 800; color: #38BDF8;">{selected_year}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PESTAÑAS PRINCIPALES DEL DASHBOARD
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🌟 Resumen Ejecutivo",
    "📊 Rentabilidad (P&L)",
    "⚖️ Balance & Liquidez",
    "🔄 Capital de Trabajo & CCC",
    "💰 Flujo de Caja & Deuda",
    "🎯 Análisis DuPont & Valor",
    "🔮 Simulador 'What-If' 2026",
    "📑 Diagnóstico & Canvas B2B"
])

# =============================================================================
# TAB 1: RESUMEN EJECUTIVO & SCORECARD C-SUITE
# =============================================================================
with tab1:
    st.markdown("### 🏆 Scorecard Financiero Ejecutivo")
    st.caption(f"Visualización de indicadores clave para el ejercicio fiscal **{selected_year}** con comparativa frente al año previo.")
    
    # Fila de KPIs Principales
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    
    def format_delta(curr, prev, is_pct=False, is_ratio=False, inverse=False):
        if prev is None:
            return "Año Base", "kpi-neu"
        diff = curr - prev
        if is_pct:
            txt = f"{diff:+.2f} pp"
        elif is_ratio:
            txt = f"{diff:+.2f}x"
        else:
            pct_change = (diff / abs(prev)) * 100 if prev != 0 else 0
            txt = f"{pct_change:+.1f}% YoY"
        
        if (diff > 0 and not inverse) or (diff < 0 and inverse):
            return txt, "kpi-pos"
        elif diff == 0:
            return txt, "kpi-neu"
        else:
            return txt, "kpi-neg"

    prev_y = prev_idx

    # KPI 1: Ingresos
    d_txt, d_cls = format_delta(arr['rev'][y_idx], arr['rev'][prev_y] if prev_y is not None else None)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Ingresos Operacionales</div>
            <div class="kpi-value">${arr['rev'][y_idx]:,.0f}M</div>
            <div class="kpi-sub {d_cls}">▲ {d_txt}</div>
        </div>
        """, unsafe_allow_html=True)

    # KPI 2: EBITDA & Margen
    d_txt, d_cls = format_delta(arr['ebitda'][y_idx], arr['ebitda'][prev_y] if prev_y is not None else None)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">EBITDA ({arr['ebitda_margin'][y_idx]:.1f}%)</div>
            <div class="kpi-value">${arr['ebitda_margin'][y_idx]:.1f}%</div>
            <div class="kpi-sub {d_cls}">▲ ${arr['ebitda'][y_idx]:,.0f}M ({d_txt})</div>
        </div>
        """, unsafe_allow_html=True)

    # KPI 3: Utilidad Neta
    d_txt, d_cls = format_delta(arr['net_income'][y_idx], arr['net_income'][prev_y] if prev_y is not None else None)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Utilidad Neta ({arr['net_margin'][y_idx]:.1f}%)</div>
            <div class="kpi-value">${arr['net_income'][y_idx]:,.0f}M</div>
            <div class="kpi-sub {d_cls}">▲ {d_txt}</div>
        </div>
        """, unsafe_allow_html=True)

    # KPI 4: ROE
    d_txt, d_cls = format_delta(arr['roe'][y_idx], arr['roe'][prev_y] if prev_y is not None else None, is_pct=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Rentabilidad ROE</div>
            <div class="kpi-value">{arr['roe'][y_idx]:.1f}%</div>
            <div class="kpi-sub {d_cls}">▲ {d_txt}</div>
        </div>
        """, unsafe_allow_html=True)

    # KPI 5: Deuda Neta / EBITDA
    d_txt, d_cls = format_delta(arr['net_debt_to_ebitda'][y_idx], arr['net_debt_to_ebitda'][prev_y] if prev_y is not None else None, is_ratio=True, inverse=True)
    with k5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Deuda Neta / EBITDA</div>
            <div class="kpi-value">{arr['net_debt_to_ebitda'][y_idx]:.2f}x</div>
            <div class="kpi-sub {d_cls}">▼ {d_txt}</div>
        </div>
        """, unsafe_allow_html=True)

    # KPI 6: Ciclo de Conversión de Efectivo
    d_txt, d_cls = format_delta(arr['ccc'][y_idx], arr['ccc'][prev_y] if prev_y is not None else None, inverse=True)
    with k6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Ciclo de Efectivo (CCC)</div>
            <div class="kpi-value">{arr['ccc'][y_idx]:.0f} Días</div>
            <div class="kpi-sub {d_cls}">▼ {d_txt}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Paneles de Diagnóstico de Salud Financiera
    st.markdown("#### 🚦 Semáforo de Salud Financiera & Diagnóstico Gerencial")
    
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    with col_d1:
        st.markdown("""
        <div class="health-card health-green">
            <strong>✅ Rentabilidad & Márgenes</strong><br>
            <small>Expansión consistente de márgenes. El margen EBITDA subió de 8.7% a 10.5% impulsado por apalancamiento operativo en gastos fijos y digitalización B2B.</small>
        </div>
        """, unsafe_allow_html=True)
    with col_d2:
        st.markdown("""
        <div class="health-card health-green">
            <strong>✅ Gestión de Capital de Trabajo</strong><br>
            <small>Reducción drástica del CCC de 75 a 56 días (-19 días). Recuperación ágil de cartera y optimización de rotación de inventarios liberaron caja masiva.</small>
        </div>
        """, unsafe_allow_html=True)
    with col_d3:
        st.markdown("""
        <div class="health-card health-blue">
            <strong>🛡️ Liquidez & Solvencia</strong><br>
            <small>Razón corriente de 2.14x y prueba ácida de 1.41x con caja récord de $12,450M en 2025. Cobertura suficiente para obligaciones operativas inmediatas.</small>
        </div>
        """, unsafe_allow_html=True)
    with col_d4:
        st.markdown("""
        <div class="health-card health-green">
            <strong>🎯 Estructura de Deuda</strong><br>
            <small>Desapalancamiento neto sobresaliente: Deuda Neta/EBITDA bajó de 1.69x a 0.51x. Cobertura de intereses pasó de 3.84x a 7.59x con perfil conservador.</small>
        </div>
        """, unsafe_allow_html=True)

    # Gráficos Macro: Evolución Histórica
    c_g1, c_g2 = st.columns(2)
    
    with c_g1:
        fig_rev_ebitda = go.Figure()
        fig_rev_ebitda.add_trace(go.Bar(
            x=years,
            y=arr['rev'],
            name='Ingresos Operacionales',
            marker_color='#1E3A8A',
            hovertemplate='<b>Año %{x}</b><br>Ingresos: $%{y:,.0f}M<extra></extra>'
        ))
        fig_rev_ebitda.add_trace(go.Scatter(
            x=years,
            y=arr['ebitda'],
            name='EBITDA',
            yaxis='y2',
            mode='lines+markers+text',
            line=dict(color='#10B981', width=3),
            marker=dict(size=8, color='#10B981'),
            text=[f"${v:,.0f}M" for v in arr['ebitda']],
            textposition="top center",
            hovertemplate='<b>Año %{x}</b><br>EBITDA: $%{y:,.0f}M<extra></extra>'
        ))
        fig_rev_ebitda.update_layout(
            title="<b>Evolución de Ingresos y EBITDA (2021 - 2025)</b>",
            yaxis=dict(title="Ingresos ($ COP M)", showgrid=True, gridcolor='#F1F5F9'),
            yaxis2=dict(title="EBITDA ($ COP M)", overlaying='y', side='right', showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=380
        )
        st.plotly_chart(fig_rev_ebitda, use_container_width=True)

    with c_g2:
        fig_cash_fcf = go.Figure()
        fig_cash_fcf.add_trace(go.Bar(
            x=years,
            y=arr['cfo'],
            name='Flujo Operativo (CFO)',
            marker_color='#3B82F6',
            hovertemplate='CFO: $%{y:,.0f}M<extra></extra>'
        ))
        fig_cash_fcf.add_trace(go.Bar(
            x=years,
            y=arr['capex'],
            name='CAPEX Inversión',
            marker_color='#EF4444',
            hovertemplate='CAPEX: $%{y:,.0f}M<extra></extra>'
        ))
        fig_cash_fcf.add_trace(go.Scatter(
            x=years,
            y=arr['fcf'],
            name='Flujo Caja Libre (FCF)',
            mode='lines+markers+text',
            line=dict(color='#047857', width=3),
            marker=dict(size=8),
            text=[f"${v:,.0f}M" for v in arr['fcf']],
            textposition="top center",
            hovertemplate='FCF: $%{y:,.0f}M<extra></extra>'
        ))
        fig_cash_fcf.update_layout(
            title="<b>Generación de Caja Operativa vs Inversión en CAPEX</b>",
            barmode='relative',
            yaxis=dict(title="$ COP M", showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=380
        )
        st.plotly_chart(fig_cash_fcf, use_container_width=True)

    # Tabla Resumen Histórico Consolidado
    st.markdown("#### 📋 Matriz Multianual Consolidada")
    preview_df = summary_df[[
        'Año', 'Ingresos', 'Crecimiento Ingresos (%)', 'EBITDA', 'Margen EBITDA (%)',
        'Utilidad Neta', 'Margen Neto (%)', 'ROA (%)', 'ROE (%)', 'CCC (Ciclo Efectivo)',
        'Deuda Neta / EBITDA', 'Efectivo'
    ]].copy()
    
    st.dataframe(
        preview_df.style.format({
            'Ingresos': '${:,.0f}M',
            'Crecimiento Ingresos (%)': '{:.1f}%',
            'EBITDA': '${:,.0f}M',
            'Margen EBITDA (%)': '{:.2f}%',
            'Utilidad Neta': '${:,.0f}M',
            'Margen Neto (%)': '{:.2f}%',
            'ROA (%)': '{:.2f}%',
            'ROE (%)': '{:.2f}%',
            'CCC (Ciclo Efectivo)': '{:.1f} d',
            'Deuda Neta / EBITDA': '{:.2f}x',
            'Efectivo': '${:,.0f}M'
        }),
        use_container_width=True
    )

# =============================================================================
# TAB 2: ESTADO DE RESULTADOS & RENTABILIDAD (P&L)
# =============================================================================
with tab2:
    st.markdown(f"### 📊 Estado de Resultados Integral ({selected_year})")
    st.caption("Desagregación analítica de ingresos, costos de mercancía, gastos operacionales e impuestos.")
    
    col_p1, col_p2 = st.columns([3, 2])
    
    with col_p1:
        # Gráfico Waterfall para el año seleccionado
        rev_y = arr['rev'][y_idx]
        cogs_y = arr['cogs'][y_idx]
        adm_y = er_table.iloc[3][str(selected_year)] # negative
        sales_y = er_table.iloc[4][str(selected_year)] # negative
        depr_y = er_table.iloc[5][str(selected_year)] # negative
        fin_y = er_table.iloc[7][str(selected_year)] # negative
        tax_y = er_table.iloc[9][str(selected_year)] # negative
        net_y = arr['net_income'][y_idx]
        
        fig_waterfall = go.Figure(go.Waterfall(
            name="P&L Waterfall",
            orientation="v",
            measure=["absolute", "relative", "total", "relative", "relative", "total", "relative", "relative", "total"],
            x=[
                "Ingresos", "Costo Ventas", "Utilidad Bruta",
                "Gastos Admon", "Gastos Ventas", "EBITDA",
                "Deprec & Amort", "Gastos Fin & Imp", "Utilidad Neta"
            ],
            textposition="outside",
            text=[
                f"${rev_y:,.0f}M", f"-${cogs_y:,.0f}M", f"${rev_y-cogs_y:,.0f}M",
                f"${abs(adm_y):,.0f}M", f"${abs(sales_y):,.0f}M", f"${arr['ebitda'][y_idx]:,.0f}M",
                f"${abs(depr_y):,.0f}M", f"${abs(fin_y)+abs(tax_y):,.0f}M", f"${net_y:,.0f}M"
            ],
            y=[
                rev_y, -cogs_y, 0,
                adm_y, sales_y, 0,
                depr_y, fin_y + tax_y, 0
            ],
            connector={"line": {"color": "#94A3B8"}},
            decreasing={"marker": {"color": "#EF4444"}},
            increasing={"marker": {"color": "#10B981"}},
            totals={"marker": {"color": "#1E3A8A"}}
        ))
        fig_waterfall.update_layout(
            title=f"<b>Cascada de Ingresos a Utilidad Neta ({selected_year})</b>",
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            yaxis=dict(title="$ COP M", showgrid=True, gridcolor='#F1F5F9'),
            margin=dict(l=40, r=40, t=50, b=40),
            height=420
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with col_p2:
        # Estructura Porcentual de Costos y Gastos (% de Ventas)
        cogs_pct = (cogs_y / rev_y) * 100
        adm_pct = (abs(adm_y) / rev_y) * 100
        sales_pct = (abs(sales_y) / rev_y) * 100
        depr_pct = (abs(depr_y) / rev_y) * 100
        fin_pct = (abs(fin_y) / rev_y) * 100
        tax_pct = (abs(tax_y) / rev_y) * 100
        net_pct = (net_y / rev_y) * 100
        
        donut_labels = ['Costo de Ventas', 'Gastos Ventas', 'Gastos Admon', 'Impuestos', 'Financieros', 'D&A', 'Utilidad Neta']
        donut_values = [cogs_pct, sales_pct, adm_pct, tax_pct, fin_pct, depr_pct, net_pct]
        donut_colors = ['#EF4444', '#F97316', '#FBBF24', '#A855F7', '#EC4899', '#64748B', '#10B981']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=donut_labels,
            values=donut_values,
            hole=.5,
            marker_colors=donut_colors,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b>: %{percent:.1f} de las Ventas<extra></extra>'
        )])
        fig_donut.update_layout(
            title=f"<b>Distribución del Ingreso (% Ventas en {selected_year})</b>",
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=50, b=20),
            height=420
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Tendencia de Márgenes a lo largo del tiempo
    st.markdown("#### 📈 Evolución y Expansión de Márgenes (2021 - 2025)")
    fig_margins = go.Figure()
    fig_margins.add_trace(go.Scatter(
        x=years, y=arr['gross_margin'], name='Margen Bruto',
        mode='lines+markers', line=dict(color='#3B82F6', width=3)
    ))
    fig_margins.add_trace(go.Scatter(
        x=years, y=arr['ebitda_margin'], name='Margen EBITDA',
        mode='lines+markers', line=dict(color='#10B981', width=3)
    ))
    fig_margins.add_trace(go.Scatter(
        x=years, y=arr['ebit_margin'], name='Margen EBIT (Operacional)',
        mode='lines+markers', line=dict(color='#8B5CF6', width=2, dash='dot')
    ))
    fig_margins.add_trace(go.Scatter(
        x=years, y=arr['net_margin'], name='Margen Neto',
        mode='lines+markers', line=dict(color='#F59E0B', width=3)
    ))
    fig_margins.update_layout(
        title="<b>Comportamiento de Márgenes Clave</b> (El Margen Bruto se mantiene en 25% mientras EBITDA y Neto se expanden)",
        yaxis=dict(title="Margen (%)", range=[0, 30], showgrid=True, gridcolor='#F1F5F9'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=50, b=40),
        height=350
    )
    st.plotly_chart(fig_margins, use_container_width=True)

    # Tabla P&L Oficial con formato contable
    st.markdown("#### 📑 Estado de Resultados Oficial Detallado")
    formatted_er = er_table.copy()
    for y in years:
        formatted_er[str(y)] = formatted_er[str(y)].apply(lambda v: f"${v:,.0f}M" if v >= 0 else f"-${abs(v):,.0f}M")
    st.dataframe(formatted_er, use_container_width=True)

# =============================================================================
# TAB 3: BALANCE GENERAL, LIQUIDEZ & ESTRUCTURA DE CAPITAL
# =============================================================================
with tab3:
    st.markdown("### ⚖️ Balance General, Solvencia y Apalancamiento")
    st.caption("Evaluación de la solidez patrimonial, liquidez corriente y estructura de fondeo.")
    
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        # Composición de Activos
        fig_assets = go.Figure()
        fig_assets.add_trace(go.Bar(
            x=years, y=arr['cash'], name='Efectivo y Equivalentes', marker_color='#10B981'
        ))
        fig_assets.add_trace(go.Bar(
            x=years, y=arr['cxc'], name='Cuentas por Cobrar', marker_color='#3B82F6'
        ))
        fig_assets.add_trace(go.Bar(
            x=years, y=arr['inv'], name='Inventarios', marker_color='#F59E0B'
        ))
        fig_assets.add_trace(go.Bar(
            x=years, y=[1200]*len(years), name='Otros Activos Corrientes', marker_color='#94A3B8'
        ))
        fig_assets.add_trace(go.Bar(
            x=years, y=fin_data['summary']['Activo Total'] - arr['total_ca'],
            name='Activos Fijos e Intangibles (No Ctes)', marker_color='#1E3A8A'
        ))
        fig_assets.update_layout(
            barmode='stack',
            title="<b>Estructura y Crecimiento de Activos ($ COP M)</b>",
            yaxis=dict(title="$ COP M", showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=380
        )
        st.plotly_chart(fig_assets, use_container_width=True)

    with col_b2:
        # Estructura Pasivo + Patrimonio
        fig_liab_eq = go.Figure()
        fig_liab_eq.add_trace(go.Bar(
            x=years, y=arr['cxp'], name='Proveedores', marker_color='#EF4444'
        ))
        fig_liab_eq.add_trace(go.Bar(
            x=years, y=summary_df['Deuda CP'], name='Deuda Bancaria CP', marker_color='#DC2626'
        ))
        fig_liab_eq.add_trace(go.Bar(
            x=years, y=summary_df['Pasivo Corriente'] - arr['cxp'] - summary_df['Deuda CP'],
            name='Otros Pasivos Ctes', marker_color='#F87171'
        ))
        fig_liab_eq.add_trace(go.Bar(
            x=years, y=summary_df['Deuda LP'], name='Deuda Bancaria LP', marker_color='#7C3AED'
        ))
        fig_liab_eq.add_trace(go.Bar(
            x=years, y=arr['total_equity'], name='Patrimonio Total', marker_color='#0284C7'
        ))
        fig_liab_eq.update_layout(
            barmode='stack',
            title="<b>Estructura de Fondeo: Pasivos y Patrimonio ($ COP M)</b>",
            yaxis=dict(title="$ COP M", showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=380
        )
        st.plotly_chart(fig_liab_eq, use_container_width=True)

    # Indicadores de Liquidez
    st.markdown("#### 💧 Indicadores de Liquidez vs Estándares de Seguridad")
    
    liq_col1, liq_col2, liq_col3 = st.columns(3)
    with liq_col1:
        st.metric(
            "Razón Corriente (Activo Cte / Pasivo Cte)",
            f"{arr['current_ratio'][y_idx]:.2f}x",
            f"Óptimo > 1.5x ({'Excelente' if arr['current_ratio'][y_idx]>=1.5 else 'Riesgo'})"
        )
    with liq_col2:
        st.metric(
            "Prueba Ácida (Sin Inventarios)",
            f"{arr['quick_ratio'][y_idx]:.2f}x",
            f"Óptimo > 1.0x ({'Excelente' if arr['quick_ratio'][y_idx]>=1.0 else 'Riesgo'})"
        )
    with liq_col3:
        st.metric(
            "Razón de Efectivo Puro (Caja / Pasivo Cte)",
            f"{(arr['cash'][y_idx] / arr['total_cl'][y_idx]):.2f}x",
            f"De 0.06x (2021) a {arr['cash'][y_idx]/arr['total_cl'][y_idx]:.2f}x (2025)"
        )

    fig_liquidity = go.Figure()
    fig_liquidity.add_trace(go.Scatter(
        x=years, y=arr['current_ratio'], name='Razón Corriente',
        mode='lines+markers', line=dict(color='#2563EB', width=3)
    ))
    fig_liquidity.add_trace(go.Scatter(
        x=years, y=arr['quick_ratio'], name='Prueba Ácida',
        mode='lines+markers', line=dict(color='#10B981', width=3)
    ))
    fig_liquidity.add_hline(y=1.5, line_dash="dash", line_color="#2563EB", annotation_text="Benchmark Razón Cte (1.5x)")
    fig_liquidity.add_hline(y=1.0, line_dash="dash", line_color="#10B981", annotation_text="Benchmark Prueba Ácida (1.0x)")
    fig_liquidity.update_layout(
        title="<b>Evolución de Ratios de Liquidez (2021 - 2025)</b>",
        yaxis=dict(title="Veces (x)", range=[0.5, 2.5], showgrid=True, gridcolor='#F1F5F9'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=50, b=40),
        height=320
    )
    st.plotly_chart(fig_liquidity, use_container_width=True)

    # Tabla Balance General
    st.markdown("#### 📑 Balance General Clasificado")
    formatted_bg = bg_table.copy()
    for y in years:
        formatted_bg[str(y)] = formatted_bg[str(y)].apply(lambda v: f"${v:,.0f}M")
    st.dataframe(formatted_bg, use_container_width=True)

# =============================================================================
# TAB 4: CAPITAL DE TRABAJO & CICLO DE EFECTIVO (CCC & KTNO)
# =============================================================================
with tab4:
    st.markdown("### 🔄 Gestión de Capital de Trabajo y Ciclo de Conversión de Efectivo")
    st.markdown("""
    > [!IMPORTANT]
    > **El Núcleo Estratégico del Caso Andina:** En 2021 la empresa crecía en ventas pero *vendía sin generar caja* debido a que el efectivo quedaba atrapado en cartera (50 días) e inventarios (65 días). Las decisiones gerenciales de 2022-2025 renegociaron condiciones con proveedores y disciplinaron compras y cobros, contrayendo el ciclo de conversión de efectivo de **75 a 56 días** y liberando millones en caja operativa.
    """)
    
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        st.metric("DSO (Días Cartera / Cobro)", f"{arr['dso'][y_idx]:.1f} días", f"{(arr['dso'][y_idx]-arr['dso'][0]):.1f} d vs 2021", delta_color="inverse")
    with col_c2:
        st.metric("DIO (Días Inventario en Bodega)", f"{arr['dio'][y_idx]:.1f} días", f"{(arr['dio'][y_idx]-arr['dio'][0]):.1f} d vs 2021", delta_color="inverse")
    with col_c3:
        st.metric("DPO (Días Pago a Proveedores)", f"{arr['dpo'][y_idx]:.1f} días", f"{(arr['dpo'][y_idx]-arr['dpo'][0]):+.1f} d vs 2021")
    with col_c4:
        st.metric("CCC (Ciclo Total de Caja)", f"{arr['ccc'][y_idx]:.1f} días", f"{(arr['ccc'][y_idx]-arr['ccc'][0]):.1f} d vs 2021", delta_color="inverse")

    # Gráfico del Ciclo de Efectivo
    col_g_c1, col_g_c2 = st.columns(2)
    
    with col_g_c1:
        fig_ccc = go.Figure()
        fig_ccc.add_trace(go.Bar(x=years, y=arr['dso'], name='(+) Días Cartera (DSO)', marker_color='#3B82F6'))
        fig_ccc.add_trace(go.Bar(x=years, y=arr['dio'], name='(+) Días Inventario (DIO)', marker_color='#F59E0B'))
        fig_ccc.add_trace(go.Bar(x=years, y=[-v for v in arr['dpo']], name='(-) Días Proveedores (DPO)', marker_color='#EF4444'))
        fig_ccc.add_trace(go.Scatter(
            x=years, y=arr['ccc'], name='(=) Ciclo Conversión Efectivo (CCC)',
            mode='lines+markers+text',
            line=dict(color='#10B981', width=3),
            marker=dict(size=9),
            text=[f"{v:.0f} d" for v in arr['ccc']],
            textposition="top center"
        ))
        fig_ccc.update_layout(
            title="<b>Desglose del Ciclo de Conversión de Efectivo (Días)</b>",
            yaxis=dict(title="Días de Operación", showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=380
        )
        st.plotly_chart(fig_ccc, use_container_width=True)

    with col_g_c2:
        # Productividad del Capital de Trabajo (PKT) y KTNO
        fig_pkt = go.Figure()
        fig_pkt.add_trace(go.Bar(
            x=years, y=arr['ktno'], name='KTNO ($ COP M)',
            marker_color='#1E3A8A', yaxis='y1'
        ))
        fig_pkt.add_trace(go.Scatter(
            x=years, y=arr['pkt'], name='PKT (% de Ventas)',
            mode='lines+markers+text',
            line=dict(color='#EC4899', width=3),
            marker=dict(size=8),
            text=[f"{v:.1f}%" for v in arr['pkt']],
            textposition="top center",
            yaxis='y2'
        ))
        fig_pkt.update_layout(
            title="<b>KTNO y Productividad del Capital de Trabajo (PKT)</b>",
            yaxis=dict(title="KTNO ($ COP M)", showgrid=True, gridcolor='#F1F5F9'),
            yaxis2=dict(title="PKT (% sobre Ventas)", overlaying='y', side='right', range=[10, 22], showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=380
        )
        st.plotly_chart(fig_pkt, use_container_width=True)

    # Análisis del Efectivo Liberado por Eficiencia en Capital de Trabajo
    st.markdown("#### 💡 Cuantificación del Valor: Caja Liberada por Eficiencia Operativa")
    
    # Si la empresa hubiera mantenido el CCC de 2021 (75 días) en 2025:
    # KTNO a 75 días con ventas de 120,000 = (75 / 365) * 120,000 = ~24,657M
    # KTNO real 2025 = 17,342M
    # Caja liberada = 24,657 - 17,342 = ~7,315 Millones de COP!
    ktno_sin_eficiencia_2025 = (arr['ccc'][0] / 365) * arr['rev'][-1]
    ktno_real_2025 = arr['ktno'][-1]
    caja_liberada_estimada = ktno_sin_eficiencia_2025 - ktno_real_2025
    
    c_inf1, c_inf2 = st.columns([2, 3])
    with c_inf1:
        st.markdown(f"""
        <div style="background: #F0FDF4; border: 2px solid #22C55E; border-radius: 12px; padding: 20px;">
            <div style="font-size: 13px; color: #166534; font-weight: 700;">CAJA LIBERADA EN 2025 GRACIAS AL NUEVO CCC</div>
            <div style="font-size: 32px; font-weight: 800; color: #15803D; margin: 8px 0;">+${caja_liberada_estimada:,.0f}M COP</div>
            <div style="font-size: 13px; color: #14532D;">
                Si Andina hubiera operado en 2025 con los 75 días de ciclo de 2021, habría tenido que inmovilizar <strong>${ktno_sin_eficiencia_2025:,.0f}M</strong> en capital de trabajo. La optimización a 56 días liberó <strong>${caja_liberada_estimada:,.0f}M</strong> directamente a la cuenta bancaria.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c_inf2:
        st.markdown("""
        **Hallazgos Clave de la Gestión Operativa:**
        - **Cobranza Preventiva:** Políticas de crédito redujeron el periodo de cobro en 7 días sin afectar ventas.
        - **Planificación de Compras:** La mejora de rotación de inventarios redujo el tiempo en bodega de 65 a 58 días mediante el ERP.
        - **Acuerdos Estratégicos:** Convenios comerciales de largo plazo con fabricantes e importadores aumentaron el financiamiento de proveedores de 40 a 45 días.
        - **Productividad:** Para vender $100 en 2021 la empresa requería $18.84 en KTNO; en 2025 solo requiere $14.45.
        """)

# =============================================================================
# TAB 5: FLUJO DE CAJA, INVERSIONES (CAPEX) & DEUDA
# =============================================================================
with tab5:
    st.markdown("### 💰 Flujo de Efectivo, CAPEX y Perfil de Deuda")
    st.caption("Origen y aplicación de fondos: de la tensión de liquidez inicial a la generación autónoma de caja.")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        # Flujo de Operación, Inversión y Financiación
        fig_cf_breakdown = go.Figure()
        fig_cf_breakdown.add_trace(go.Bar(x=years, y=arr['cfo'], name='Flujo Operación (CFO)', marker_color='#10B981'))
        fig_cf_breakdown.add_trace(go.Bar(x=years, y=arr['cfi'], name='Flujo Inversión (CFI)', marker_color='#EF4444'))
        fig_cf_breakdown.add_trace(go.Bar(x=years, y=arr['cff'], name='Flujo Financiación (CFF)', marker_color='#3B82F6'))
        fig_cf_breakdown.update_layout(
            title="<b>Flujos Netos por Actividad ($ COP M)</b>",
            yaxis=dict(title="$ COP M", showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=380
        )
        st.plotly_chart(fig_cf_breakdown, use_container_width=True)

    with col_f2:
        # Deuda Bruta vs Deuda Neta y Efectivo
        fig_debt_dynamic = go.Figure()
        fig_debt_dynamic.add_trace(go.Bar(x=years, y=arr['total_debt'], name='Deuda Financiera Total', marker_color='#94A3B8'))
        fig_debt_dynamic.add_trace(go.Bar(x=years, y=arr['cash'], name='Efectivo Disponible', marker_color='#0284C7'))
        fig_debt_dynamic.add_trace(go.Scatter(
            x=years, y=arr['net_debt'], name='Deuda Neta (Deuda - Efectivo)',
            mode='lines+markers+text',
            line=dict(color='#DC2626', width=3),
            marker=dict(size=8),
            text=[f"${v:,.0f}M" for v in arr['net_debt']],
            textposition="top center"
        ))
        fig_debt_dynamic.update_layout(
            title="<b>Deuda Financiera Bruta vs Deuda Neta ($ COP M)</b>",
            yaxis=dict(title="$ COP M", showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=380
        )
        st.plotly_chart(fig_debt_dynamic, use_container_width=True)

    # Indicadores de Cobertura y Desapalancamiento
    st.markdown("#### 🛡️ Ratios de Solvencia, Cobertura y Retorno al Accionista")
    c_deb1, c_deb2, c_deb3, c_deb4 = st.columns(4)
    with c_deb1:
        st.metric(
            "Deuda Neta / EBITDA",
            f"{arr['net_debt_to_ebitda'][y_idx]:.2f}x",
            f"De 1.69x (2021) a {arr['net_debt_to_ebitda'][-1]:.2f}x (2025)",
            delta_color="inverse"
        )
    with c_deb2:
        st.metric(
            "Cobertura de Intereses (EBIT / Gastos Fin)",
            f"{arr['interest_coverage'][y_idx]:.2f}x",
            f"+{(arr['interest_coverage'][y_idx]-arr['interest_coverage'][0]):.2f}x vs 2021"
        )
    with c_deb3:
        st.metric(
            "Conversión EBITDA a Caja (CFO/EBITDA)",
            f"{(arr['cfo'][y_idx]/arr['ebitda'][y_idx]*100):.1f}%",
            f"Subió de 31.8% a {(arr['cfo'][-1]/arr['ebitda'][-1]*100):.1f}%"
        )
    with c_deb4:
        st.metric(
            "Dividendos Pagados (% Payout)",
            f"${abs(arr['dividends'][y_idx]):,.0f}M ({arr['payout'][y_idx]:.0f}%)",
            f"Payout creció de 0% a 35%"
        )

    # Tabla Flujo de Efectivo
    st.markdown("#### 📑 Estado de Flujo de Efectivo Completo")
    formatted_cfs = cfs_table.copy()
    for y in years:
        formatted_cfs[str(y)] = formatted_cfs[str(y)].apply(lambda v: f"${v:,.0f}M" if v >= 0 else f"-${abs(v):,.0f}M")
    st.dataframe(formatted_cfs, use_container_width=True)

# =============================================================================
# TAB 6: DESCOMPOSICIÓN DUPONT & CREACIÓN DE VALOR
# =============================================================================
with tab6:
    st.markdown(f"### 🎯 Descomposición del Retorno sobre el Patrimonio (DuPont Analysis {selected_year})")
    st.caption("Explicación matemática de los inductores de rentabilidad para los accionistas.")
    
    nm_val = arr['net_margin'][y_idx] / 100
    at_val = arr['asset_turnover'][y_idx]
    em_val = arr['equity_multiplier'][y_idx]
    calc_roe = nm_val * at_val * em_val * 100
    
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.markdown(f"""
        <div style="background: #EFF6FF; border: 2px solid #3B82F6; border-radius: 10px; padding: 16px; text-align: center;">
            <div style="font-size: 11px; color: #1E40AF; font-weight: 700;">MARGEN NETO (Rentabilidad)</div>
            <div style="font-size: 26px; font-weight: 800; color: #1D4ED8; margin: 4px 0;">{arr['net_margin'][y_idx]:.2f}%</div>
            <div style="font-size: 11px; color: #64748B;">Utilidad Neta / Ingresos</div>
        </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown(f"""
        <div style="background: #FDF4FF; border: 2px solid #C084FC; border-radius: 10px; padding: 16px; text-align: center;">
            <div style="font-size: 11px; color: #6B21A8; font-weight: 700;">ROTACIÓN ACTIVOS (Eficiencia)</div>
            <div style="font-size: 26px; font-weight: 800; color: #7E22CE; margin: 4px 0;">{at_val:.2f}x</div>
            <div style="font-size: 11px; color: #64748B;">Ingresos / Activos Totales</div>
        </div>
        """, unsafe_allow_html=True)
    with d3:
        st.markdown(f"""
        <div style="background: #FFF7ED; border: 2px solid #FB923C; border-radius: 10px; padding: 16px; text-align: center;">
            <div style="font-size: 11px; color: #9A3412; font-weight: 700;">APALANCAMIENTO FINANCIERO</div>
            <div style="font-size: 26px; font-weight: 800; color: #C2410C; margin: 4px 0;">{em_val:.2f}x</div>
            <div style="font-size: 11px; color: #64748B;">Activos Totales / Patrimonio</div>
        </div>
        """, unsafe_allow_html=True)
    with d4:
        st.markdown(f"""
        <div style="background: #F0FDF4; border: 2px solid #22C55E; border-radius: 10px; padding: 16px; text-align: center;">
            <div style="font-size: 11px; color: #166534; font-weight: 700;">ROE RESULTANTE (DuPont)</div>
            <div style="font-size: 26px; font-weight: 800; color: #15803D; margin: 4px 0;">{calc_roe:.2f}%</div>
            <div style="font-size: 11px; color: #64748B;">Rentabilidad Total Accionista</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico DuPont Evolutivo
    fig_dupont = make_subplots(
        rows=1, cols=3,
        subplot_titles=("1. Margen Neto (%)", "2. Rotación de Activos (x)", "3. Multiplicador de Capital (x)")
    )
    fig_dupont.add_trace(go.Scatter(x=years, y=arr['net_margin'], mode='lines+markers', line=dict(color='#3B82F6', width=3)), row=1, col=1)
    fig_dupont.add_trace(go.Scatter(x=years, y=arr['asset_turnover'], mode='lines+markers', line=dict(color='#8B5CF6', width=3)), row=1, col=2)
    fig_dupont.add_trace(go.Scatter(x=years, y=arr['equity_multiplier'], mode='lines+markers', line=dict(color='#F97316', width=3)), row=1, col=3)
    fig_dupont.update_layout(
        title="<b>Dinámica de los 3 Inductores DuPont (2021–2025)</b>",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=50, b=40),
        height=320
    )
    st.plotly_chart(fig_dupont, use_container_width=True)

    st.markdown("""
    > [!TIP]
    > **Conclusión Analítica DuPont:** El aumento del ROE de **16.58% (2021)** a **21.14% (2025)** es de **altísima calidad orgánica**, ya que se produjo mientras el multiplicador de apalancamiento financiero se reducía de 2.13x a 2.01x. La ganancia en rentabilidad fue impulsada puramente por la **eficiencia operativa y expansión del Margen Neto** (que escaló de 3.73% a 5.57%).
    """)

# =============================================================================
# TAB 7: SIMULADOR GERENCIAL "WHAT-IF" (PROYECCIONES 2026)
# =============================================================================
with tab7:
    st.markdown("### 🔮 Simulador Estratégico Interactivo (Escenarios 2026)")
    st.caption("Modifique las variables gerenciales para proyectar los resultados financieros de Distribuciones Andina en 2026.")
    
    col_s1, col_s2 = st.columns([1, 2])
    
    with col_s1:
        st.markdown("##### 🎛️ Parámetros del Escenario 2026")
        sim_sales_growth = st.slider("Crecimiento Proyectado de Ventas (%):", min_value=0.0, max_value=25.0, value=10.0, step=0.5)
        sim_gross_margin = st.slider("Margen Bruto Esperado (%):", min_value=20.0, max_value=30.0, value=25.0, step=0.5)
        sim_opex_growth = st.slider("Crecimiento de Gastos Admin/Ventas (%):", min_value=0.0, max_value=20.0, value=7.0, step=0.5)
        
        st.markdown("---")
        st.markdown("##### ⏳ Metas de Capital de Trabajo")
        sim_dso = st.slider("Días de Cartera (DSO objetivo):", min_value=35, max_value=60, value=42, step=1)
        sim_dio = st.slider("Días de Inventario (DIO objetivo):", min_value=45, max_value=70, value=56, step=1)
        sim_dpo = st.slider("Días de Proveedores (DPO objetivo):", min_value=35, max_value=55, value=45, step=1)
        
        st.markdown("---")
        sim_capex = st.number_input("Presupuesto de Inversión CAPEX ($ COP M):", min_value=1000.0, max_value=8000.0, value=3800.0, step=100.0)
        sim_payout = st.slider("Tasa de Dividendos Payout (%):", min_value=0, max_value=60, value=35, step=5)

    # Cálculos de Simulación 2026
    base_rev_2025 = arr['rev'][-1] # 120,000
    sim_rev = base_rev_2025 * (1 + sim_sales_growth / 100)
    sim_cogs = sim_rev * (1 - sim_gross_margin / 100)
    sim_gp = sim_rev * (sim_gross_margin / 100)
    
    base_opex_2025 = summary_df['Gastos Admon'].iloc[-1] + summary_df['Gastos Ventas'].iloc[-1] # 7800 + 9600 = 17400
    sim_opex = base_opex_2025 * (1 + sim_opex_growth / 100)
    sim_da = 1700.0 # Proyección de depreciación
    sim_ebit = sim_gp - sim_opex - sim_da
    sim_ebitda = sim_ebit + sim_da
    
    sim_fin = 1400.0 # Gastos financieros estimados
    sim_ebt = sim_ebit - sim_fin
    sim_tax = sim_ebt * 0.30 if sim_ebt > 0 else 0
    sim_net = sim_ebt - sim_tax
    
    # Capital de trabajo proyectado
    sim_cxc = (sim_dso / 365) * sim_rev
    sim_inv = (sim_dio / 365) * sim_cogs
    sim_cxp = (sim_dpo / 365) * sim_cogs
    sim_ktno = sim_cxc + sim_inv - sim_cxp
    sim_ccc = sim_dso + sim_dio - sim_dpo
    
    # Flujo de caja libre estimado
    delta_ktno = sim_ktno - arr['ktno'][-1]
    sim_cfo = sim_net + sim_da - delta_ktno
    sim_fcf = sim_cfo - sim_capex
    sim_div = sim_net * (sim_payout / 100)
    sim_cash = arr['cash'][-1] + sim_fcf - sim_div
    
    with col_s2:
        st.markdown("##### 📊 Resultados Proyectados 2026 vs Cierre Real 2025")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Ventas 2026", f"${sim_rev:,.0f}M", f"{sim_sales_growth:+.1f}% vs 2025")
        m2.metric("EBITDA 2026", f"${sim_ebitda:,.0f}M", f"{(sim_ebitda/arr['ebitda'][-1]-1)*100:+.1f}% vs 2025")
        m3.metric("Utilidad Neta", f"${sim_net:,.0f}M", f"{(sim_net/arr['net_income'][-1]-1)*100:+.1f}% vs 2025")
        
        m4, m5, m6 = st.columns(3)
        m4.metric("Nuevo CCC", f"{sim_ccc:.0f} Días", f"{(sim_ccc - arr['ccc'][-1]):+.1f} d vs 2025", delta_color="inverse")
        m5.metric("CFO Proyectado", f"${sim_cfo:,.0f}M", f"{(sim_cfo - arr['cfo'][-1]):+,.0f}M")
        m6.metric("Caja Final 2026", f"${sim_cash:,.0f}M", f"{(sim_cash - arr['cash'][-1]):+,.0f}M")

        # Gráfico comparativo 2025 Real vs 2026 Proyectado
        comp_categories = ['Ingresos', 'EBITDA', 'Utilidad Neta', 'CFO', 'Caja Final']
        val_2025 = [arr['rev'][-1], arr['ebitda'][-1], arr['net_income'][-1], arr['cfo'][-1], arr['cash'][-1]]
        val_2026 = [sim_rev, sim_ebitda, sim_net, sim_cfo, sim_cash]
        
        fig_comp = go.Figure(data=[
            go.Bar(name='2025 Real', x=comp_categories, y=val_2025, marker_color='#1E3A8A'),
            go.Bar(name='2026 Simulado', x=comp_categories, y=val_2026, marker_color='#10B981')
        ])
        fig_comp.update_layout(
            barmode='group',
            title="<b>Impacto Proyectado: Métricas Clave 2025 vs 2026 ($ COP M)</b>",
            yaxis=dict(title="$ COP M", showgrid=True, gridcolor='#F1F5F9'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=340
        )
        st.plotly_chart(fig_comp, use_container_width=True)

# =============================================================================
# TAB 8: DIAGNÓSTICO ESTRATÉGICO & BUSINESS MODEL CANVAS
# =============================================================================
with tab8:
    st.markdown("### 📑 Diagnóstico Estratégico y Business Model Canvas B2B")
    st.caption("Alineación del desempeño financiero cuantitativo con la propuesta de valor y modelo de negocio del caso.")
    
    # Resumen del Caso
    st.markdown("""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 20px;">
        <h4 style="margin-top:0; color: #0F172A;">🏢 Perfil de Negocio: Distribuciones Andina Comercial S.A.S.</h4>
        <p style="font-size: 14px; color: #334155; line-height: 1.6;">
            Distribuidora B2B colombiana especializada en abastecer a integradores de seguridad electrónica, redes de datos y herramientas industriales para los sectores de construcción e industria. Su propuesta de valor no se basa en el precio más bajo, sino en la <strong>disponibilidad inmediata de stock, rapidez de entrega y acompañamiento preventa y posventa</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Visualización Canvas
    c_col1, c_col2, c_col3 = st.columns(3)
    with c_col1:
        st.markdown("""
        <div class="canvas-box">
            <div class="canvas-header">1. Segmentos de Clientes</div>
            <ul style="font-size: 13px; color: #334155; padding-left: 18px;">
                <li>Empresas del sector construcción e infraestructura.</li>
                <li>Plantas industriales y manufactura.</li>
                <li>Comercio especializado y distribuidores secundarios.</li>
                <li>Integradores de sistemas de seguridad electrónica y redes.</li>
            </ul>
            <div class="canvas-header" style="margin-top:15px;">4. Relaciones con Clientes</div>
            <ul style="font-size: 13px; color: #334155; padding-left: 18px;">
                <li>Cuentas clave (Key Accounts) B2B recurrentes.</li>
                <li>Asesoría técnica y soporte de ingeniería posventa.</li>
                <li>Fidelización basada en cumplimiento estricto de entregas.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_col2:
        st.markdown("""
        <div class="canvas-box">
            <div class="canvas-header">2. Propuesta de Valor</div>
            <ul style="font-size: 13px; color: #334155; padding-left: 18px;">
                <li><strong>Disponibilidad inmediata:</strong> inventario crítico sin demoras de importación.</li>
                <li><strong>Portafolio mixto:</strong> marcas premium importadas + marcas propias de alto margen.</li>
                <li><strong>Asesoría técnica:</strong> reducción de fallas y errores de instalación para contratistas.</li>
            </ul>
            <div class="canvas-header" style="margin-top:15px;">3. Canales de Distribución</div>
            <ul style="font-size: 13px; color: #334155; padding-left: 18px;">
                <li>Fuerza comercial consultiva externa.</li>
                <li>Venta asistida por cotizaciones y pedidos digitales.</li>
                <li><strong>Plataforma B2B Digital (2024-2025):</strong> autoservicio ágil con inventario en tiempo real.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_col3:
        st.markdown("""
        <div class="canvas-box">
            <div class="canvas-header">7. Actividades Clave</div>
            <ul style="font-size: 13px; color: #334155; padding-left: 18px;">
                <li>Gestión de abastecimiento e importación.</li>
                <li>Operación logística, alistamiento y despachos rápidos.</li>
                <li>Gestión de cobranza activa y control de riesgo de crédito.</li>
            </ul>
            <div class="canvas-header" style="margin-top:15px;">8. Aliados Clave</div>
            <ul style="font-size: 13px; color: #334155; padding-left: 18px;">
                <li>Fabricantes de tecnología internacionales y nacionales.</li>
                <li>Operadores logísticos de transporte intermunicipal.</li>
                <li>Entidades financieras (crédito rotativo y de mediano plazo).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Costos e Ingresos
    c_b1, c_b2 = st.columns(2)
    with c_b1:
        st.markdown("""
        <div class="canvas-box">
            <div class="canvas-header">Estructura de Costos & Capital</div>
            <ul style="font-size: 13px; color: #334155; padding-left: 18px;">
                <li><strong>Costo de Mercancía Vendida (75% de ventas):</strong> costo directo de importación.</li>
                <li><strong>Gastos Comerciales y Logísticos (8% de ventas):</strong> nómina de ventas y fletes.</li>
                <li><strong>Gastos Administrativos y TI (6.5% de ventas):</strong> sistemas ERP y bodega.</li>
                <li><strong>Costo Financiero (1.2% de ventas):</strong> intereses bancarios controlados.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c_b2:
        st.markdown("""
        <div class="canvas-box">
            <div class="canvas-header">Estructura de Ingresos & Rentabilidad</div>
            <ul style="font-size: 13px; color: #334155; padding-left: 18px;">
                <li><strong>Ventas mayoristas a crédito:</strong> contratos recurrentes con clientes B2B.</li>
                <li><strong>Captura de margen con marcas propias:</strong> sostiene el margen bruto en 25%.</li>
                <li><strong>Crecimiento sostenido (CAGR 10.7%):</strong> escalamiento con eficiencia digital.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🎯 Dictamen y Recomendaciones para la Junta Directiva")
    
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("""
        **1. Continuar Digitalización B2B**
        Invertir en la expansión de la plataforma digital para que el 40%+ de las compras recurrentes migren al portal, permitiendo escalar ventas sin contratar personal operativo proporcional.
        """)
    with r2:
        st.markdown("""
        **2. Optimización del Exceso de Caja**
        Con $12,450M en efectivo y Deuda Neta/EBITDA de solo 0.51x, la compañía debe estructurar una tesorería activa (inversión en rendimientos de corto plazo) o evaluar adquisiciones estratégicas.
        """)
    with r3:
        st.markdown("""
        **3. Blindar el Ciclo de Efectivo (CCC)**
        Institucionalizar la política de cobro a 43 días y pagos a 45 días para evitar recaer en el cuello de botella de 2021 ante eventuales ciclos de desaceleración macroeconómica.
        """)

# -----------------------------------------------------------------------------
# PIE DE PÁGINA CORPORATIVO
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 12px; padding: 10px 0;">
    Distribuciones Andina Comercial S.A.S. | Sistema de Información Financiera y Toma de Decisiones | Desarrollado con Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
