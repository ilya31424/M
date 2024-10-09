﻿import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

pd.set_option("display.precision", 2)

data = pd.read_csv('titanic_train.csv',
                  index_col='PassengerId')

data.head(5)

data.describe()

data[(data['Embarked'] == 'C') & (data.Fare > 200)].head()

data[(data['Embarked'] == 'C') & (data['Fare'] > 200)].sort_values(by='Fare', ascending=False).head()

def age_category(age):
    '''
    < 30 -> 1
    >= 30, <55 -> 2
    >= 55 -> 3
    '''
    if age < 30:
        return 1
    elif age < 55:
        return 2
    elif age >= 55:
        return 3

    age_categories = [age_category(age) for age in data.Age]
data['Age_category'] = age_categories

#1 Сколько мудчин и женщин было на боррту?
male_count = data[data['Sex'] == 'male'].shape[0]
female_count = data[data['Sex'] == 'female'].shape[0]
print("1. Сколько мужчин / женщин было на борту?")
print(f"{male_count} мужчин и {female_count} женщин")

#2. Определите распределение функции Pclass. Теперь Для мужчин и женщин отдельно. Сколько людей из второго класса было на борту?
pclass_distribution = data['Pclass'].value_counts()
pclass_2_count = pclass_distribution[2]
print("2. Сколько людей из второго класса было на борту?")
print(f"{pclass_2_count}")

#3. Каковы медиана и стандартное отклонениеFare?. Округлите до 2-х знаков после запятой.
fare_median = round(data['Fare'].median(), 2)
fare_std = round(data['Fare'].std(), 2)
print("3. Каковы медиана и стандартное отклонение Fare?. Округлите до 2-х знаков после запятой.")
print(f"Медиана: {fare_median}, Стандартное отклонение: {fare_std}")

#4. Правда ли, что средний возраст выживших людей выше, чем у пассажиров, которые в конечном итоге умерли?
survived_avg_age = data[data['Survived'] == 1]['Age'].mean()
not_survived_avg_age = data[data['Survived'] == 0]['Age'].mean()
print("4. Правда ли, что средний возраст выживших людей выше, чем у пассажиров, которые в конечном итоге умерли?")
print(f"Средний возраст выживших: {survived_avg_age}, умерших: {not_survived_avg_age}")
if survived_avg_age > not_survived_avg_age:
    print("Да")
else:
    print("Нет")

#5. Это правда, что пассажиры моложе 30 лет. выжили чаще, чем те, кому больше 60 лет. Каковы доли выживших людей среди молодых и пожилых людей?
young_survival_rate = data[(data['Age'] < 30) & (data['Survived'] == 1)].shape[0] / data[data['Age'] < 30].shape[0] * 100
old_survival_rate = data[(data['Age'] > 60) & (data['Survived'] == 1)].shape[0] / data[data['Age'] > 60].shape[0] * 100
print("5. Это правда, что пассажиры моложе 30 лет выжили чаще, чем те, кому больше 60 лет. Каковы доли выживших людей среди молодых и пожилых людей?")
print(f"Доля выживших среди молодежи: {young_survival_rate:.1f}%, среди пожилых: {old_survival_rate:.1f}%")

#6. Правда ли, что женщины выживали чаще мужчин? Каковы доли выживших людей среди мужчин и женщин?
male_survival_rate = data[(data['Sex'] == 'male') & (data['Survived'] == 1)].shape[0] / data[data['Sex'] == 'male'].shape[0] * 100
female_survival_rate = data[(data['Sex'] == 'female') & (data['Survived'] == 1)].shape[0] / data[data['Sex'] == 'female'].shape[0] * 100
print("6. Правда ли, что женщины выживали чаще мужчин? Каковы доли выживших людей среди мужчин и женщин?")
print(f"Доля выживших среди мужчин: {male_survival_rate:.1f}%, среди женщин: {female_survival_rate:.1f}%")

#7. Какое имя наиболее популярно среди пассажиров мужского пола?
def get_first_name(full_name):
    if '(' in full_name:  # для имен, включающих девичью фамилию
        name = full_name.split('(')[1].split(' ')[0]
    else:
        name = full_name.split(',')[1].split('.')[1].split(' ')[1]
    return name

male_names = data[data['Sex'] == 'male']['Name'].apply(get_first_name)
most_common_male_name = male_names.value_counts().idxmax()
print("7. Какое имя наиболее популярно среди пассажиров мужского пола?")
print(f"{most_common_male_name}")

#8. Как средний возраст мужчин / женщин зависит от Pclass? Выберите все правильные утверждения:
avg_age_by_class_and_sex = data.groupby(['Pclass', 'Sex'])['Age'].mean().unstack()

statements = []

if avg_age_by_class_and_sex.loc[1, 'male'] > 40:
    statements.append("В среднем мужчины 1 класса старше 40 лет")

if avg_age_by_class_and_sex.loc[1, 'female'] > 40:
    statements.append("В среднем женщины 1 класса старше 40 лет")

if (avg_age_by_class_and_sex['male'] > avg_age_by_class_and_sex['female']).all():
    statements.append("Мужчины всех классов в среднем старше, чем женщины того же класса")

if (avg_age_by_class_and_sex.loc[1].mean() > avg_age_by_class_and_sex.loc[2].mean() and
    avg_age_by_class_and_sex.loc[2].mean() > avg_age_by_class_and_sex.loc[3].mean()):
    statements.append("В среднем, пассажиры первого класса старше, чем пассажиры 2-го класса, которые старше, чем пассажиры 3-го класса.")

#Вывод
print("8. Как средний возраст мужчин / женщин зависит от Pclass?")
for statement in statements:
    print(statement) 
