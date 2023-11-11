import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sql

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#данные вписываемые в таблицу
data = [
    (months[0], 200000, 33), (months[1], 250000, 37), (months[2], 400000, 72),
    (months[3], 500000, 65), (months[4], 900000, 78), (months[5], 1100000, 85),
    (months[6], 1500000, 88), (months[7], 1300000, 91), (months[8], 800000, 82),
    (months[9], 600000, 73), (months[10], 300000, 45), (months[11], 500000, 36)
]

database = sql.connect("service_ice_db")
cursor = database.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS serviceIce (
months TEXT,
cost NUMBER,
temp NUMBER
)""")

for month in months:
    cursor.execute("DELETE FROM serviceIce WHERE months=?", (month.lower(),))

#вписывание данных в таблицу
cursor.executemany("INSERT INTO serviceIce (months, cost, temp) VALUES (?, ?, ?)", data)
database.commit()

#создаем массивы, в которые будем пушить данные
cost_ice = []
temp_air = []

#перебираем массив месяцев, чтобы по каждому месяцу найти значения из столбцов таблицы. Если находим соответствующие то
# пушим в нужный массив значения из подходящего столбца
for month in months:
    cursor.execute("SELECT cost FROM serviceIce WHERE months=?", (month,))
    cost = cursor.fetchone()
    if cost:
        cost_ice.append(cost[0])

    cursor.execute("SELECT temp FROM serviceIce WHERE months=?", (month,))
    temp = cursor.fetchone()
    if temp:
        temp_air.append(temp[0])



width = 0.4
x_list = list(range(0, 12))
x_indexes = np.arange(len(months)) #создание индексов для оси х, их количество равно # кол-ву значений из оси х
# np.arange - это массив-нампай, точнее матрица

plt.figure()

plt.subplot(2, 1, 1)
plt.title('Зависимость продажи мороженого от температуры по ℉')
plt.xticks(x_indexes, months)
plt.ylabel('Сумма в рублях')
plt.plot(months, cost_ice, label="Выручка", marker="o")
plt.plot(months, temp_air, label="Температура по ℉", marker="^")
plt.legend()

plt.subplot(2, 1, 2)
plt.title(' ')
plt.xticks(np.arange(len(months)), months)
plt.ylabel('Сумма в рублях')
plt.bar(x_indexes - (width / 2), cost_ice, label="Выручка", width=width)
plt.bar(x_indexes + (width / 2), temp_air, label="Температура по ℉", width=width)
plt.legend()

x = np.array(cost_ice)
y = np.array(temp_air)

correlation_matrix = np.corrcoef(x, y)
correlation_coefficient = correlation_matrix[0, 1]

plt.xlabel(f'Коэффициент корреляции: {correlation_coefficient}')
print(correlation_coefficient)

plt.show()

database.close()
