# data_analysis_homework
Домашнее задание по: Лекция 6. Качество данных

**I. Профилирование**

~БД сотрудников организации **без указания должностей**, (возможно) за исключением ранее уволенных. (без дат увольнения)

**1) Анализ форматов и типов данных:**

~Все столбцы имеют тип "object" (строка)

1) Преобразовываем **age** и **salary** в числовые значения (float64)
2) Преобразовываем **join_date** в формат даты (datetime)

**2) Анализ полноты данных:**

~ **age**: 51 NaN
  **email**: 1 NaN
  **salary**: 31 NaN
  **join_date**: 50 NaT

1) Приводим даты к корректному формату (меняем местами месяц и день, если месяц больше 12)

**3) Анализ уникальности/дубликатов:**

~ email указаны случайно, с малым уникальным количеством, соответственно они повторяются, также выявлены некорректные форматы (без указания домена)
  дубликатов не выявлено, полное совпадение имени, фамилии и возраста сотрудника зафиксировано один раз (случайное совпадение в виду различий по **salary** и **join_date**)

  **4) Статистический анализ**

~ Проведенный статистический выявил аномалии:
1) **join_date** - x2: дата из будущего, и дата из далекого прошлого
2) **age** - x2: отрицательное значение и значение 999
3) **salary** - x16: одно отрицательное значение и пятнадцать значений 999999

**II. Очистка данных**

~Для очистки данных был выполнен поиск строк с пустыми значениями, вместе со строками с аномальными значениями они были удалены.
Из изначальных 1000 строк было получено 897 очищенных, потеря составила ~10%

**III. Коррелляционный анализ**

~На основе полученных очищенных данных был проведен коррелляционный анализ, значительных зависимостей не выявлено.
Выявлена дата с аномально высоким количеством трудоустройств.

**ВЫВОД:** ~10% данных потеряно в виду их некорректности, по оставшимся очищенным данным значительных коррелляций не выявлено.
