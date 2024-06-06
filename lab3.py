
import pandas as pd
import matplotlib.pyplot as plt

# Загрузка файла с населением
population_df = pd.read_csv('https://gist.githubusercontent.com/SharmaAshwini/404b6dd361b234d7fecae78ff9deb80a/raw/1c3b0c82f6e48a93a2ba2f690c838753196b43e9/world_population.csv')
population_df = population_df[['country name', 'current population']]
population_df.columns = ['Country', 'Population']
population_df['Population'] = population_df['Population'].str.replace(',', '').astype(int)
population_df['Country'] = population_df['Country'].str.lower().str.strip()
population_df.set_index('Country', inplace=True)

# Загрузка данных о COVID-19
df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
df['Country'] = df['Country'].str.strip()

# Пользовательский ввод для выбора количества и названий стран
num_countries = int(input("Введите количество стран для сравнения: "))

selected_countries = []
for i in range(num_countries):
    country = input("Введите название страны: ").strip()  # Приведение к нижнему регистру и удаление пробелов по краям
    selected_countries.append(country)

# Пользовательский ввод для выбора формата данных
print("Выберите формат данных:")
print("1. Абсолютные значения")
print("2. На 100,000 человек")
print("3. Прирост (заболевшие, выздоровевшие, умершие)")
data_format = int(input("Введите число: "))

# Функция для пересчета данных на 100 000 человек
def per_capita_data(df):
    percapita_df = df.copy()
    for country in selected_countries:
        if country in population_df.index:
            percapita_df[country] = percapita_df[country] / population_df.loc[country, 'Population'] * 100000
        else:
            print(f"Данные о населении для страны {country} отсутствуют.")
    return percapita_df

# Функция для расчета прироста
def calculate_growth(df):
    growth_df = df.copy()
    for country in selected_countries:
        growth_df[f'Daily Confirmed {country}'] = growth_df[growth_df['Country'] == country]['Confirmed'].diff().fillna(0)
    return growth_df

# Если выбран формат данных "на 100 000 человек", выполняем пересчет
if data_format == 2:
    df = per_capita_data(df)
elif data_format == 3:
    df = calculate_growth(df)

# Пользовательский ввод для выбора категории статистики
if data_format != 3:
    category = input("Введите категорию статистики (Confirmed/Recovered/Deaths) или цифру (1/2/3): ").strip()

    # Расшифровка введенных чисел
    if category == '1':
        category = 'Confirmed'
    elif category == '2':
        category = 'Recovered'
    elif category == '3':
        category = 'Deaths'

    # Фильтрация данных по выбранным странам
    df = df[df['Country'].isin(selected_countries)]

    # Отображение графика для выбранной категории
    plt.figure(figsize=(12,8))

    for country in selected_countries:
        country_data = df[df['Country'] == country]
        plt.plot(country_data['Date'], country_data[category], label=country)

    plt.xlabel('Date')
    plt.ylabel(f'# of {category.capitalize()}')
    plt.title(f'COVID-19 {category.capitalize()} by Country')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    plt.figure(figsize=(12,8))
    for country in selected_countries:
        country_data = df[df['Country'] == country]
        plt.plot(country_data['Date'], country_data[f'Daily Confirmed {country}'], label=f'{country} Daily Confirmed')

    plt.xlabel('Date')
    plt.ylabel('Daily Confirmed Cases')
    plt.title('COVID-19 Daily Confirmed Cases by Country')
    plt.legend()
    plt.grid(True)
    plt.show()
