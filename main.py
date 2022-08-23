import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt

pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)


def add(df):
    ultimo_valor = df['Numero'].iat[-1]
    ultima_fecha = df['Fecha'].iat[-1]

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

    df = pd.concat([df, new_data], ignore_index=True)
    data.reset_index()

    df.to_csv('wordle_stats.csv', encoding='latin1')

    return df


def plot(df):
    average_pablo = df['Pablo'].mean()
    std_dev_pablo = df['Pablo'].std()
    average_jorge = df['Jorge'].mean()
    std_dev_jorge = df['Jorge'].std()
    average_andres = df['Andres'].mean()
    std_dev_andres = df['Andres'].std()

    average_total = (average_pablo + average_andres + average_jorge) / 3

    poly_order = 1

    coef_pablo = np.polyfit(df['Numero'], df['Pablo'], poly_order)
    reg_pablo = np.poly1d(coef_pablo)

    coef_jorge = np.polyfit(df['Numero'], df['Jorge'], poly_order)
    reg_jorge = np.poly1d(coef_jorge)

    coef_andres = np.polyfit(df['Numero'], df['Andres'], poly_order)
    reg_andres = np.poly1d(coef_andres)

    # ----------------------------------------- MATPLOTLIB ----------------------------------------- #

    plt.figure(dpi=120, facecolor='#52616B')
    plt.title("Cantidad de intentos hasta averiguar la palabra correcta", fontsize=18)

    plt.xticks(fontsize=14, rotation=45)
    plt.yticks(fontsize=14)

    plt.xlabel("Número de Wordle", fontsize=14)
    plt.ylabel("Intentos", fontsize=14)

    plt.xlim(left=df['Numero'].min(), right=df['Numero'].max())
    plt.ylim(1, 8)

    plt.grid(color='gray', linestyle='--', linewidth=0.3)

    plt.plot(df['Numero'], reg_pablo(df['Numero']), color="#F08A5D", linewidth=3, label='Pablo')
    plt.plot(df['Numero'], reg_jorge(df['Numero']), color="#393E46", linewidth=3, label='Jorge')
    plt.plot(df['Numero'], reg_andres(df['Numero']), color="#3FC1C9", linewidth=3, label='Andres')
    plt.plot(df['Numero'], df['Pablo'], color="#F08A5D", linewidth=1)
    plt.plot(df['Numero'], df['Jorge'], color="#393E46", linewidth=1)
    plt.plot(df['Numero'], df['Andres'], color="#3FC1C9", linewidth=1)

    plt.legend(loc='upper right')

    plt.text(
        x=(df['Numero'].max() - df['Numero'].min()) / 2,
        y=7.7,
        s=f'Promedio Pablo: {average_pablo:.4}   Promedio Jorge: {average_jorge:.4}   Promedio Andrés: {average_andres:.4}'
    )
    plt.text(
        x=(df['Numero'].max() - df['Numero'].min()) / 2 + df['Numero'].min(),
        y=7.4,
        s=f'Promedio total: {average_total:.4}'
    )
    plt.text(
        x=(df['Numero'].max() - df['Numero'].min()) / 2,
        y=7.1,
        s=f'Desv Std Pablo: {std_dev_pablo:.4}   Desv Std Jorge: {std_dev_jorge:.4}   Desv Std Andres: {std_dev_andres:.4}'
    )

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()


def edit(df, num):

    print(df.loc[df['Numero'] == num])

    value = int(input('\nIngrese el dato que desea editar: Numero (1) / Fecha (2) / Pablo (3) / Jorge (4) / Andres (5)\n'))

    if value == 1:
        to_replace = df.loc[df['Numero'] == num, 'Numero'].values[0]
        new_value = int(input('\nIngrese el nuevo valor:\n'))
        df.replace(to_replace=to_replace, value=new_value, inplace=True)
        print(df.tail())

    elif value == 2:
        to_replace = df.loc[df['Numero'] == num, 'Fecha'].values[0]
        new_value = input('\nIngrese la nueva fecha:\n')
        df.replace(to_replace=to_replace, value=new_value, inplace=True)
        print(df.tail())

    df.to_csv('wordle_stats.csv', encoding='latin1')
    return


data = pd.read_csv('wordle_stats.csv', encoding='latin1', parse_dates=['Fecha'], index_col=[0])

print(data.tail())

is_on = True

while is_on:

    user_input = int(input('\nIngrese la opción deseada: AGREGAR (1) / MOSTRAR GRÁFICO (2) / EDITAR (3) / BUSCAR (4) / SALIR (5)\n'))

    if user_input == 1:

        data = add(data)

        print(data.tail())

    elif user_input == 2:

        plot(data)

    elif user_input == 3:

        wordle_num = input("\nIngrese el numero de wordle que desea editar:\n")

        if data['Numero'].astype(str).str.contains(wordle_num).any():
            edit(data, int(wordle_num))
        else:
            print(f'Ese numero de wordle no existe')

    elif user_input == 4:

        palabra = input("\nIngrese la palabra que desea buscar:\n")

        if data['Palabra'].str.contains(palabra, case=False).any():
            print(f'La palabra {palabra.upper()} ya fue utilizada')
        else:
            print(f'La palabra {palabra.upper()} no fue utilizada')

    elif user_input == 5:

        print('\nChaucito!')

        is_on = False

    else:
        print('\nEsa no es una opción posible. Intente de nuevo.')

# TODO 1: Incluir alguna manera de editar filas
