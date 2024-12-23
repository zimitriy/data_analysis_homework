import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import re
from datetime import datetime

# Загрузка данных
data = pd.read_csv('data.csv')

print(data.head())

# Переходим к профилирование данных, проводим анализ форматов:
data.info()  # Все столбцы имеют тип данных - object

# Создаем новый файл для проведения анализа
data.to_csv('data_analysed.csv', index=False)

# Преобразовываем столбцы age и salary в числовой формат и заменяем некорректные данные на NaN
data['age'] = pd.to_numeric(data['age'], errors='coerce')
data['salary'] = pd.to_numeric(data['salary'], errors='coerce')

# Сохраняем данные после преобразования столбцов age и salary
data.to_csv('data_analysed.csv', index=False)


# Далее проводим анализ полноты данных, начинаем с даты - меняем местами день и месяц, если месяц больше 12
def fix_date_format(date_str):
    try:
        date_parts = str(date_str).split(" ")
        date = date_parts[0]
        time = date_parts[1] if len(date_parts) > 1 else "00:00:00"
        year, month, day = date.split("-")
        month, day = (day, month) if int(month) > 12 else (month, day)
        return f"{year}-{month}-{day} {time}"
    except ValueError:
        return date_str


# Применяем функцию к столбцу join_date для исправления формата
data['join_date'] = data['join_date'].apply(fix_date_format)

# Преобразуем столбец join_date в datetime
data['join_date'] = pd.to_datetime(data['join_date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Сохраняем данные после исправления столбца join_date
data.to_csv('data_analysed.csv', index=False)

# Указываем, что столбец join_date должен быть распознан как datetime
data_analysed = pd.read_csv('data_analysed.csv', parse_dates=['join_date'])

# Проверяем типы данных и выводим первые строки
print(data_analysed.head())
data_analysed.info()

# Затем выполняем анализ дубликатов по столбцам first_name, last_name и age - уникальным сотрудникам
duplicates = data_analysed[data_analysed.duplicated(subset=['first_name', 'last_name', 'age'], keep=False)]
print("\nДубликаты по столбцам first_name, last_name и age:")
print(duplicates)

# Теперь начинаем статистический анализ данных:
age_stats = {
   'mean': data_analysed['age'].mean(),
   'std': data_analysed['age'].std(),
   'min': data_analysed['age'].min(),
   'max': data_analysed['age'].max()
}

age_anomalies = data_analysed[
   (data_analysed['age'] < 18) |
   (data_analysed['age'] > 80) |
   (abs(data_analysed['age'] - age_stats['mean']) > 3 * age_stats['std'])
]

salary_stats = {
   'mean': data_analysed['salary'].mean(),
   'std': data_analysed['salary'].std(),
   'min': data_analysed['salary'].min(),
   'max': data_analysed['salary'].max()
}

salary_anomalies = data_analysed[
   (data_analysed['salary'] < 10000) |
   (abs(data_analysed['salary'] - salary_stats['mean']) > 3 * salary_stats['std'])
]

current_date = pd.Timestamp.now()
date_anomalies = data_analysed[
   (data_analysed['join_date'] > current_date) |
   (data_analysed['join_date'] < pd.Timestamp('2000-01-01'))
]

print("\nАномалии в возрасте:")
print(age_anomalies[['first_name', 'last_name', 'age']])

print("\nАномалии в зарплате:")
print(salary_anomalies[['first_name', 'last_name', 'salary']])

print("\nАномалии в датах:")
print(date_anomalies[['first_name', 'last_name', 'join_date']])

# Удаляем строки с нулевыми значениями
data_analysed = data_analysed.dropna()

# Удаляем аномалии в столбце salary (9999999 и отрицательные значения)
data_analysed = data_analysed[~data_analysed['salary'].isin([9999999]) & (data_analysed['salary'] >= 0)]

# Удаляем аномалии в столбце age (999 и отрицательные значения)
data_analysed = data_analysed[~data_analysed['age'].isin([999]) & (data_analysed['age'] >= 0)]

# Удаляем аномалии в столбце join_date (даты ранее 01.01.2020 и из будущего)
data_analysed = data_analysed[
    (data_analysed['join_date'] >= pd.Timestamp('2020-01-01')) &
    (data_analysed['join_date'] <= pd.Timestamp('2024-12-23'))
]

# Сохраняем данные после удаления аномалий
data_analysed.to_csv('data_cleaned.csv', index=False)
data_cleaned = pd.read_csv('data_cleaned.csv')

# Проверяем результат
print(data_cleaned.head())
data_cleaned.info()

# Предполагаем зависимость заработной платы от возраста
# Строим график для проверки гипотезы
plt.figure(figsize=(10, 6))
plt.scatter(data_cleaned['age'], data_cleaned['salary'], alpha=0.5, color='b')

# Добавляем заголовок и подписи осей
plt.title('Зависимость зарплаты от возраста', fontsize=14)
plt.xlabel('Возраст', fontsize=12)
plt.ylabel('Зарплата', fontsize=12)

# Сохраняем график в файл (например, в формате PNG)
plt.savefig('salary_vs_age.png')

# Предполагаем зависимость заработной платы от даты трудоустройства
# Строим график для проверки гипотезы
plt.figure(figsize=(10, 6))
plt.scatter(data_cleaned['join_date'], data_cleaned['salary'], alpha=0.5, color='g')

# Добавляем заголовок и подписи осей
plt.title('Зависимость зарплаты от даты вступления', fontsize=14)
plt.xlabel('Дата вступления', fontsize=12)
plt.ylabel('Зарплата', fontsize=12)

# Поворот подписей оси X для удобства чтения
plt.xticks(rotation=45)

# Сохраняем график в файл
plt.savefig('salary_vs_join_date.png')

# Строим график зависимости возраста от даты вступления
plt.figure(figsize=(10, 6))
plt.scatter(data_cleaned['join_date'], data_cleaned['age'], alpha=0.5, color='r')

# Добавляем заголовок и подписи осей
plt.title('Зависимость возраста от даты вступления', fontsize=14)
plt.xlabel('Дата вступления', fontsize=12)
plt.ylabel('Возраст', fontsize=12)

# Поворот подписей оси X для удобства чтения
plt.xticks(rotation=45)

# Сохраняем график в файл
plt.savefig('age_vs_join_date.png')

# Предполагаем зависимость возраста от даты вступления
# Строим график для проверки гипотезы
plt.figure(figsize=(10, 6))
plt.scatter(data_cleaned['join_date'], data_cleaned['age'], alpha=0.5, color='r')

# Добавляем заголовок и подписи осей
plt.title('Зависимость возраста от даты вступления', fontsize=14)
plt.xlabel('Дата вступления', fontsize=12)
plt.ylabel('Возраст', fontsize=12)

# Поворот подписей оси X для удобства чтения
plt.xticks(rotation=45)

# Сохраняем график в файл
plt.savefig('age_vs_join_date.png')

# Для начала строим график количества трудоустройств по датам
data_cleaned['join_date'] = pd.to_datetime(data_cleaned['join_date'], errors='coerce')

# Группируем данные по датам и считаем количество трудоустройств
join_date_counts = data_cleaned['join_date'].dt.date.value_counts().sort_index()

# Строим график
plt.figure(figsize=(12, 6))
join_date_counts.plot(kind='line', color='b', marker='o', linestyle='-', linewidth=2)

# Добавляем заголовок и подписи осей
plt.title('Количество трудоустройств по датам', fontsize=14)
plt.xlabel('Дата вступления', fontsize=12)
plt.ylabel('Количество трудоустройств', fontsize=12)

# Поворот подписей оси X для удобства чтения
plt.xticks(rotation=45)

# Сохраняем график в файл
plt.savefig('employment_counts_by_date.png')

# Рассчитываем статистику по количеству трудоустройств
mean_join_date_count = join_date_counts.mean()
std_join_date_count = join_date_counts.std()

# Определяем порог для аномальных дат (например, 3 стандартных отклонения выше среднего)
threshold = mean_join_date_count + 3 * std_join_date_count

# Убираем даты, у которых количество трудоустройств больше порога
filtered_join_date_counts = join_date_counts[join_date_counts <= threshold]

# Строим график после удаления аномальных дат
plt.figure(figsize=(12, 6))
filtered_join_date_counts.plot(kind='line', color='b', marker='o', linestyle='-', linewidth=2)

# Добавляем заголовок и подписи осей
plt.title('Количество трудоустройств по датам (без аномальных дат)', fontsize=14)
plt.xlabel('Дата вступления', fontsize=12)
plt.ylabel('Количество трудоустройств', fontsize=12)

# Поворот подписей оси X для удобства чтения
plt.xticks(rotation=45)

# Сохраняем график в файл
plt.savefig('filtered_employment_counts_by_date.png')

# Подсчитываем уникальные значения email
email_counts = data_cleaned['email'].value_counts()

# Строим график количества уникальных значений email
plt.figure(figsize=(14, 8))  # Увеличиваем размер графика

email_counts.plot(kind='bar', color='c')

# Добавляем заголовок и подписи осей
plt.title('Количество уникальных значений email', fontsize=16)
plt.xlabel('Email', fontsize=14)
plt.ylabel('Количество', fontsize=14)

# Поворот подписей оси X для удобства чтения
plt.xticks(rotation=90)

# Используем tight_layout для улучшения размещения элементов графика
plt.tight_layout()

# Сохраняем график в файл
plt.savefig('email_counts.png')


