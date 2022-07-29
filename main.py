import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt

pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

# USAR EN CASO DE HACER CAGADAS CON EL CSV #
# data = pd.read_csv('wordle_stats.csv', delimiter=';', encoding='latin1', parse_dates=['Fecha'])
# data.to_csv('wordle_stats.csv')

data = pd.read_csv('wordle_stats.csv', encoding='latin1', parse_dates=['Fecha'], index_col=[0])

print(data.tail(5))

data_to_add = True

while data_to_add:
    info = input('Hay información nueva para agregar (y/n)? \n')
    ultimo_valor = data['Numero'].iat[-1]
    ultima_fecha = data['Fecha'].iat[-1]
    if info == 'y':
        numero = int(input(f'Ingrese el número de Wordle correspondiente. El último es el {ultimo_valor}\n'))
        fecha = ultima_fecha + datetime.timedelta(days=1)
        pablo = int(input('Ingrese los intentos de Pablo\n'))
        jorge = int(input('Ingrese los intentos de Jorge\n'))
        andres = int(input('Ingrese los intentos de Andrés\n'))
        palabra = input('Ingrese la palabra\n').upper()

        new_data = pd.DataFrame({
            'Numero': numero,
            'Fecha': fecha,
            'Pablo': pablo,
            'Jorge': jorge,
            'Andres': andres,
            'Palabra': palabra
        }, index=[0])

        data = pd.concat([data, new_data], ignore_index=True)
        data.reset_index()

        print(data.tail())

        data.to_csv('wordle_stats.csv', encoding='latin1')
    else:
        data_to_add = False

average_pablo = data['Pablo'].mean()
std_dev_pablo = data['Pablo'].std()
average_jorge = data['Jorge'].mean()
std_dev_jorge = data['Jorge'].std()
average_andres = data['Andres'].mean()
std_dev_andres = data['Andres'].std()

average_total = (average_pablo + average_andres + average_jorge) / 3

poly_order = 1

coef_pablo = np.polyfit(data['Numero'], data['Pablo'], poly_order)
reg_pablo = np.poly1d(coef_pablo)

coef_jorge = np.polyfit(data['Numero'], data['Jorge'], poly_order)
reg_jorge = np.poly1d(coef_jorge)

coef_andres = np.polyfit(data['Numero'], data['Andres'], poly_order)
reg_andres = np.poly1d(coef_andres)

# ----------------------------------------- MATPLOTLIB ----------------------------------------- #

plt.figure(dpi=120, facecolor='#52616B')
plt.title("Cantidad de intentos hasta averiguar la palabra correcta", fontsize=18)

plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)

plt.xlabel("Número de Wordle", fontsize=14)
plt.ylabel("Intentos", fontsize=14)

plt.xlim(left=data['Numero'].min(), right=data['Numero'].max())
plt.ylim(1, 8)

plt.grid(color='gray', linestyle='--', linewidth=0.3)

plt.plot(data['Numero'], reg_pablo(data['Numero']), color="#F08A5D", linewidth=3, label='Pablo')
plt.plot(data['Numero'], reg_jorge(data['Numero']), color="#393E46", linewidth=3, label='Jorge')
plt.plot(data['Numero'], reg_andres(data['Numero']), color="#3FC1C9", linewidth=3, label='Andres')
plt.plot(data['Numero'], data['Pablo'], color="#F08A5D", linewidth=1)
plt.plot(data['Numero'], data['Jorge'], color="#393E46", linewidth=1)
plt.plot(data['Numero'], data['Andres'], color="#3FC1C9", linewidth=1)

plt.legend(loc='upper right')

plt.text(
    x=(data['Numero'].max() - data['Numero'].min()) / 2,
    y=7.7,
    s=f'Promedio Pablo: {average_pablo:.4}   Promedio Jorge: {average_jorge:.4}   Promedio Andrés: {average_andres:.4}'
)
plt.text(
    x=(data['Numero'].max() - data['Numero'].min()) / 2 + data['Numero'].min(),
    y=7.4,
    s=f'Promedio total: {average_total:.4}'
)
plt.text(
    x=(data['Numero'].max() - data['Numero'].min()) / 2,
    y=7.1,
    s=f'Desv Std Pablo: {std_dev_pablo:.4}   Desv Std Jorge: {std_dev_jorge:.4}   Desv Std Andres: {std_dev_andres:.4}'
)

mng = plt.get_current_fig_manager()
mng.window.state('zoomed')

plt.show()

# TODO 1: Incluir alguna manera de buscar palabras existentes
# TODO 2: Incluir alguna manera de editar filas
