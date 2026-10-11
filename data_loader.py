"""
Módulo de Carga y Modelado Financiero
Distribuciones Andina Comercial S.A.S. (2021-2025)
Autor: Analista Financiero Senior
"""

import pandas as pd
import numpy as np

def load_and_process_financial_data(base_path='ARCHIVOS'):
    """
    Lee los estados financieros en Excel y calcula todos los indicadores
    financieros clave para Distribuciones Andina Comercial S.A.S.
    """
    # 1. Cargar datos
    bg_df = pd.read_excel(f'{base_path}/balance_general.xlsx')
    er_df = pd.read_excel(f'{base_path}/estado_de_resultados.xlsx')
    fe_df = pd.read_excel(f'{base_path}/estado_flujo_efectivo.xlsx')
    
    years = [2021, 2022, 2023, 2024, 2025]
    years_str = [str(y) for y in years]
    
    # 2. Extraer cuentas de Estado de Resultados
    # Índices basados en la estructura del archivo
    rev = er_df.iloc[0][years].values.astype(float)        # Ingresos operacionales
    cogs = er_df.iloc[1][years].values.astype(float)       # Costo de ventas
    gross_profit = er_df.iloc[2][years].values.astype(float)# Utilidad bruta
    admin_exp = er_df.iloc[3][years].values.astype(float)  # Gastos admin
    sales_exp = er_df.iloc[4][years].values.astype(float)  # Gastos ventas
    depr_amort = er_df.iloc[5][years].values.astype(float) # D&A
    ebit = er_df.iloc[6][years].values.astype(float)       # EBIT
    interest_exp = er_df.iloc[7][years].values.astype(float)# Gastos financieros
    ebt = er_df.iloc[8][years].values.astype(float)        # EBT
    tax = er_df.iloc[9][years].values.astype(float)        # Impuestos
    net_income = er_df.iloc[10][years].values.astype(float)# Utilidad neta
    
    ebitda = ebit + depr_amort
    total_opex = admin_exp + sales_exp
    
    # 3. Extraer cuentas de Balance General
    cash = bg_df.iloc[0][years].values.astype(float)         # Efectivo y equivalentes
    cxc = bg_df.iloc[1][years].values.astype(float)          # Cuentas por cobrar clientes
    inventories = bg_df.iloc[2][years].values.astype(float)  # Inventarios
    other_ca = bg_df.iloc[3][years].values.astype(float)     # Otros activos corrientes
    total_ca = bg_df.iloc[4][years].values.astype(float)     # Total activo corriente
    ppe_net = bg_df.iloc[5][years].values.astype(float)      # Propiedad, planta y equipo (neto)
    intangibles = bg_df.iloc[6][years].values.astype(float)  # Intangibles (neto)
    total_assets = bg_df.iloc[7][years].values.astype(float) # Total activos
    
    st_debt = bg_df.iloc[8][years].values.astype(float)      # Deuda corto plazo
    cxp_prov = bg_df.iloc[9][years].values.astype(float)     # Proveedores
    other_cl = bg_df.iloc[10][years].values.astype(float)    # Cuentas por pagar y otros
    tax_payable = bg_df.iloc[11][years].values.astype(float) # Impuestos por pagar
    total_cl = bg_df.iloc[12][years].values.astype(float)    # Total pasivo corriente
    lt_debt = bg_df.iloc[13][years].values.astype(float)     # Deuda largo plazo
    total_liab = bg_df.iloc[14][years].values.astype(float)  # Total pasivos
    
    capital = bg_df.iloc[15][years].values.astype(float)     # Capital social
    reserves = bg_df.iloc[16][years].values.astype(float)    # Reservas
    retained_earn = bg_df.iloc[17][years].values.astype(float)# Resultados acumulados
    total_equity = bg_df.iloc[18][years].values.astype(float)# Total patrimonio
    
    # 4. Extraer cuentas de Flujo de Efectivo
    cfo = fe_df.iloc[9][years].values.astype(float)          # Flujo Operación
    capex = fe_df.iloc[11][years].values.astype(float)       # CAPEX (negativo)
    cfi = fe_df.iloc[12][years].values.astype(float)         # Flujo Inversión
    debt_flow = fe_df.iloc[14][years].values.astype(float)   # Variación Deuda
    dividends = fe_df.iloc[15][years].values.astype(float)   # Dividendos
    cff = fe_df.iloc[16][years].values.astype(float)         # Flujo Financiación
    
    # Corrección técnica en 2021 si viene un separador decimal atípico (-1.472 en vez de -1472.0)
    cff[0] = debt_flow[0] + dividends[0]
    
    net_cash_change = fe_df.iloc[17][years].values.astype(float)
    cash_beg = fe_df.iloc[18][years].values.astype(float)
    cash_end = fe_df.iloc[19][years].values.astype(float)
    
    # 5. Cálculos de Indicadores Financieros
    # Rentabilidad y Márgenes (%)
    gross_margin = (gross_profit / rev) * 100
    ebitda_margin = (ebitda / rev) * 100
    ebit_margin = (ebit / rev) * 100
    net_margin = (net_income / rev) * 100
    roa = (net_income / total_assets) * 100
    roe = (net_income / total_equity) * 100
    
    # Capital de Trabajo y Ciclo de Conversión de Efectivo (Días)
    dso = (cxc / rev) * 365
    dio = (inventories / cogs) * 365
    dpo = (cxp_prov / cogs) * 365
    ccc = dso + dio - dpo
    ktno = cxc + inventories - cxp_prov
    pkt = (ktno / rev) * 100
    
    # Liquidez
    current_ratio = total_ca / total_cl
    quick_ratio = (total_ca - inventories) / total_cl
    cash_ratio = cash / total_cl
    net_working_capital = total_ca - total_cl
    
    # Endeudamiento y Estructura Financiera
    total_debt = st_debt + lt_debt
    net_debt = total_debt - cash
    leverage_ratio = (total_liab / total_assets) * 100
    debt_to_equity = (total_debt / total_equity) * 100
    debt_to_ebitda = total_debt / ebitda
    net_debt_to_ebitda = net_debt / ebitda
    interest_coverage = ebit / interest_exp
    
    # Flujo de Caja y Desempeño
    free_cash_flow = cfo + capex # capex is negative
    ebitda_to_cash_conv = (cfo / ebitda) * 100
    dividend_payout = np.zeros_like(net_income)
    for i in range(len(years)):
        if net_income[i] > 0:
            dividend_payout[i] = (abs(dividends[i]) / net_income[i]) * 100
            
    # DuPont Analysis
    asset_turnover = rev / total_assets
    equity_multiplier = total_assets / total_equity
    dupont_roe = (net_margin / 100) * asset_turnover * equity_multiplier * 100
    
    # Tasas de Crecimiento Interanual (YoY)
    rev_growth = [0.0] + [((rev[i] / rev[i-1]) - 1) * 100 for i in range(1, len(years))]
    ebitda_growth = [0.0] + [((ebitda[i] / ebitda[i-1]) - 1) * 100 for i in range(1, len(years))]
    net_income_growth = [0.0] + [((net_income[i] / net_income[i-1]) - 1) * 100 for i in range(1, len(years))]
    cfo_growth = [0.0] + [((cfo[i] / cfo[i-1]) - 1) * 100 for i in range(1, len(years))]

    # Organizar DataFrame Resumen Consolidado
    summary_df = pd.DataFrame({
        'Año': years,
        'Ingresos': rev,
        'Crecimiento Ingresos (%)': rev_growth,
        'Costo de Ventas': cogs,
        'Utilidad Bruta': gross_profit,
        'Margen Bruto (%)': gross_margin,
        'Gastos Admon': admin_exp,
        'Gastos Ventas': sales_exp,
        'EBITDA': ebitda,
        'Margen EBITDA (%)': ebitda_margin,
        'Crecimiento EBITDA (%)': ebitda_growth,
        'EBIT': ebit,
        'Margen EBIT (%)': ebit_margin,
        'Gastos Financieros': interest_exp,
        'Utilidad Neta': net_income,
        'Margen Neto (%)': net_margin,
        'Crecimiento Utilidad Neta (%)': net_income_growth,
        'Activo Corriente': total_ca,
        'Activo Total': total_assets,
        'Pasivo Corriente': total_cl,
        'Pasivo Total': total_liab,
        'Patrimonio': total_equity,
        'Efectivo': cash,
        'Cuentas por Cobrar': cxc,
        'Inventarios': inventories,
        'Proveedores': cxp_prov,
        'Deuda CP': st_debt,
        'Deuda LP': lt_debt,
        'Deuda Financiera Total': total_debt,
        'Deuda Neta': net_debt,
        'ROA (%)': roa,
        'ROE (%)': roe,
        'DSO (Días Cartera)': dso,
        'DIO (Días Inventario)': dio,
        'DPO (Días Proveedores)': dpo,
        'CCC (Ciclo Efectivo)': ccc,
        'KTNO': ktno,
        'PKT (%)': pkt,
        'Razón Corriente': current_ratio,
        'Prueba Ácida': quick_ratio,
        'Razón de Efectivo': cash_ratio,
        'Endeudamiento (%)': leverage_ratio,
        'Deuda / EBITDA': debt_to_ebitda,
        'Deuda Neta / EBITDA': net_debt_to_ebitda,
        'Cobertura de Intereses': interest_coverage,
        'CFO': cfo,
        'CAPEX': capex,
        'CFI': cfi,
        'CFF': cff,
        'Flujo de Caja Libre': free_cash_flow,
        'Conversión EBITDA a Caja (%)': ebitda_to_cash_conv,
        'Dividendos Pagados': abs(dividends),
        'Payout Ratio (%)': dividend_payout,
        'Rotación de Activos (x)': asset_turnover,
        'Multiplicador de Capital (x)': equity_multiplier
    })
    
    # Tablas contables formateadas
    er_table = pd.DataFrame({
        'Cuenta': [
            'Ingresos operacionales (ventas)',
            '(-) Costo de ventas',
            '(=) Utilidad bruta',
            '(-) Gastos de administración',
            '(-) Gastos de ventas',
            '(-) Depreciaciones y amortizaciones',
            '(=) Utilidad operacional (EBIT)',
            '(-) Gastos financieros (intereses)',
            '(=) Utilidad antes de impuestos',
            '(-) Impuesto de renta (30%)',
            '(=) Utilidad neta del ejercicio'
        ]
    })
    for i, y in enumerate(years):
        er_table[str(y)] = [
            rev[i], -cogs[i], gross_profit[i],
            -admin_exp[i], -sales_exp[i], -depr_amort[i],
            ebit[i], -interest_exp[i], ebt[i], -tax[i], net_income[i]
        ]
        
    bg_table = pd.DataFrame({
        'Cuenta': [
            'Efectivo y equivalentes',
            'Deudores (cuentas por cobrar)',
            'Inventarios',
            'Otros activos corrientes',
            'TOTAL ACTIVO CORRIENTE',
            'Propiedad, planta y equipo (neto)',
            'Intangibles (neto)',
            'TOTAL ACTIVOS',
            'Obligaciones financieras - corto plazo',
            'Proveedores',
            'Cuentas por pagar y otros pasivos',
            'Impuestos por pagar',
            'TOTAL PASIVO CORRIENTE',
            'Obligaciones financieras - largo plazo',
            'TOTAL PASIVOS',
            'Capital social',
            'Reservas',
            'Resultados acumulados',
            'TOTAL PATRIMONIO',
            'TOTAL PASIVO + PATRIMONIO'
        ]
    })
    for i, y in enumerate(years):
        bg_table[str(y)] = [
            cash[i], cxc[i], inventories[i], other_ca[i], total_ca[i],
            ppe_net[i], intangibles[i], total_assets[i],
            st_debt[i], cxp_prov[i], other_cl[i], tax_payable[i], total_cl[i],
            lt_debt[i], total_liab[i],
            capital[i], reserves[i], retained_earn[i], total_equity[i],
            total_liab[i] + total_equity[i]
        ]

    cfs_table = pd.DataFrame({
        'Concepto': [
            'Utilidad neta del ejercicio',
            '(+) Depreciación y amortización',
            '(-) Var. Cuentas por cobrar',
            '(-) Var. Inventarios',
            '(-) Var. Otros activos corrientes',
            '(+) Var. Proveedores',
            '(+) Var. Otros pasivos corrientes',
            '(+) Var. Impuestos por pagar',
            '(=) Flujo neto de efectivo de operación (CFO)',
            '(-) Compras de PPE (CAPEX)',
            '(=) Flujo neto de efectivo de inversión (CFI)',
            '(+) Var. Neta obligaciones financieras (CP+LP)',
            '(-) Dividendos pagados',
            '(=) Flujo neto de efectivo de financiación (CFF)',
            '(=) Incremento neto de efectivo',
            'Efectivo inicial',
            'Efectivo final'
        ]
    })
    for i, y in enumerate(years):
        cfs_table[str(y)] = [
            net_income[i], depr_amort[i],
            fe_df.iloc[3][y], fe_df.iloc[4][y], fe_df.iloc[5][y],
            fe_df.iloc[6][y], fe_df.iloc[7][y], fe_df.iloc[8][y],
            cfo[i],
            capex[i], cfi[i],
            debt_flow[i], dividends[i], cff[i],
            net_cash_change[i], cash_beg[i], cash_end[i]
        ]

    data = {
        'years': years,
        'summary': summary_df,
        'er_table': er_table,
        'bg_table': bg_table,
        'cfs_table': cfs_table,
        'arrays': {
            'rev': rev, 'cogs': cogs, 'gross_profit': gross_profit,
            'ebitda': ebitda, 'ebit': ebit, 'net_income': net_income,
            'cash': cash, 'cxc': cxc, 'inv': inventories, 'cxp': cxp_prov,
            'total_ca': total_ca, 'total_assets': total_assets,
            'total_cl': total_cl, 'total_liab': total_liab, 'total_equity': total_equity,
            'total_debt': total_debt, 'net_debt': net_debt,
            'cfo': cfo, 'capex': capex, 'cfi': cfi, 'cff': cff, 'fcf': free_cash_flow,
            'dso': dso, 'dio': dio, 'dpo': dpo, 'ccc': ccc,
            'ktno': ktno, 'pkt': pkt,
            'gross_margin': gross_margin, 'ebitda_margin': ebitda_margin,
            'ebit_margin': ebit_margin, 'net_margin': net_margin,
            'roa': roa, 'roe': roe,
            'current_ratio': current_ratio, 'quick_ratio': quick_ratio,
            'debt_to_ebitda': debt_to_ebitda, 'net_debt_to_ebitda': net_debt_to_ebitda,
            'interest_coverage': interest_coverage,
            'asset_turnover': asset_turnover, 'equity_multiplier': equity_multiplier,
            'dividends': dividends, 'payout': dividend_payout
        }
    }
    return data

if __name__ == '__main__':
    d = load_and_process_financial_data()
    print("Data loaded successfully! Columns in summary:", len(d['summary'].columns))
