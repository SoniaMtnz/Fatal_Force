# -*- coding: utf-8 -*-
"""Fatal_Force_(start).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zPzwLwqEfFDc8RCjnl7uBjES2CROnF1A

# Introduction

Since Jan. 1, 2015, [The Washington Post](https://www.washingtonpost.com/) has been compiling a database of every fatal shooting in the US by a police officer in the line of duty.

<center><img src=https://i.imgur.com/sX3K62b.png></center>

While there are many challenges regarding data collection and reporting, The Washington Post has been tracking more than a dozen details about each killing. This includes the race, age and gender of the deceased, whether the person was armed, and whether the victim was experiencing a mental-health crisis. The Washington Post has gathered this supplemental information from law enforcement websites, local new reports, social media, and by monitoring independent databases such as "Killed by police" and "Fatal Encounters". The Post has also conducted additional reporting in many cases.

There are 4 additional datasets: US census data on poverty rate, high school graduation rate, median household income, and racial demographics. [Source of census data](https://factfinder.census.gov/faces/nav/jsf/pages/community_facts.xhtml).

### Upgrade Plotly

Run the cell below if you are working with Google Colab
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install --upgrade plotly

"""## Import Statements"""

import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# This might be helpful:
from collections import Counter

"""## Notebook Presentation"""

pd.options.display.float_format = '{:,.2f}'.format

"""## Load the Data"""

df_hh_income = pd.read_csv('Median_Household_Income_2015.csv', encoding="windows-1252")
df_pct_poverty = pd.read_csv('Pct_People_Below_Poverty_Level.csv', encoding="windows-1252")
df_pct_completed_hs = pd.read_csv('Pct_Over_25_Completed_High_School.csv', encoding="windows-1252")
df_share_race_city = pd.read_csv('Share_of_Race_By_City.csv', encoding="windows-1252")
df_fatalities = pd.read_csv('Deaths_by_Police_US.csv', encoding="windows-1252")

"""# Preliminary Data Exploration

* What is the shape of the DataFrames?
* How many rows and columns do they have?
* What are the column names?
* Are there any NaN values or duplicates?

Media Household income
1 y 2. 29322 rows, 3 columns
3. Geographic Area', 'City', 'Median Income'
4. Not NaN, not duplicated

Deaths by Police
1 y 2. 2535 rows, 14 columns
3. 'id', 'name', 'date', 'manner_of_death', 'armed', 'age', 'gender',
       'race', 'city', 'state', 'signs_of_mental_illness', 'threat_level',
       'flee', 'body_camera'
4. NaN, not duplicated

Pct over 25
1 y 2. 29322 rows, 3 columns
3. Geographic Area', 'City', 'percent_completed_hs'
4. Not NaN, not duplicated

pct people below poverty
1 y 2. 29329 rows, 3 columns
3. Geographic Area', 'City', 'poverty_rate
4. Not NaN, not duplicated

share of Race by City
1 y 2. 29268 rows, 7 columns
3. 'Geographic area', 'City', 'share_white', 'share_black',
       'share_native_american', 'share_asian', 'share_hispanic'
4. Not NaN, not duplicated
"""

df_hh_income.shape
df_hh_income.head()
df_hh_income.columns
df_hh_income.isna()
df_hh_income.duplicated()

df_pct_poverty.shape
df_pct_poverty.head()
df_pct_poverty.columns
df_pct_poverty.isna()
df_pct_poverty.duplicated()

df_share_race_city.shape
df_share_race_city.head()
df_share_race_city.columns
df_share_race_city.isna()
df_share_race_city.duplicated()

df_pct_poverty.shape
df_pct_poverty.head()
df_pct_poverty.columns
df_pct_poverty.isna()
df_pct_poverty.duplicated()

df_fatalities.shape
df_fatalities.head()
df_fatalities.columns
df_fatalities.isna()
# df_fatalities.duplicated()

"""## Data Cleaning - Check for Missing Values and Duplicates

Consider how to deal with the NaN values. Perhaps substituting 0 is appropriate.
"""

# clean_df_fatalities = df_fatalities.isna().values.any()
# Check if there are any missing values in the DataFrame
if df_fatalities.isna().values.any():
    # Replace missing values with 0 for 'age' and 'race' columns
    df_fatalities['age'].fillna(0, inplace=True)
    df_fatalities['race'].fillna(0, inplace=True)

df_fatalities.isna()

"""# Chart the Poverty Rate in each US State

Create a bar chart that ranks the poverty rate from highest to lowest by US state. Which state has the highest poverty rate? Which state has the lowest poverty rate?  Bar Plot
"""

df_pct_poverty.columns

df_pct_poverty.describe()
df_pct_poverty.head()

# df_pct_poverty.poverty_rate.nunique()
# Reemplazar los guiones '-' con NaN
df_pct_poverty['poverty_rate'] = df_pct_poverty['poverty_rate'].replace('-', np.nan)
# Convertir la columna 'poverty_rate' a float
df_pct_poverty['poverty_rate'] = df_pct_poverty['poverty_rate'].astype(float)
df_pct_poverty['poverty_rate'].head()

# Hacer la media de cada area geografica
df_mean_poverty_rate = df_pct_poverty.groupby('Geographic Area')['poverty_rate'].mean().reset_index()
# Valores de mayor a menor
df_sorted_poverty = df_mean_poverty_rate.sort_values(by='poverty_rate', ascending=False)

bar = px.bar(df_sorted_poverty, x='Geographic Area', y='poverty_rate',
             title='Poverty Rate by Geographic Area', color='Geographic Area', color_discrete_map={'Geographic Area': 'lightblue'},
             )
# rotar valores x
bar.update_xaxes(tickangle=45)
bar.update_layout(width=800, height=600)
# quitar fondo azul
bar.update_layout(plot_bgcolor='rgba(0,0,0,0)')


bar.show()

# from google.colab import drive
# drive.mount('/content/drive')

# %cd /content/drive/MyDrive/Fatal+Force+(start)





"""# Chart the High School Graduation Rate by US State

Show the High School Graduation Rate in ascending order of US States. Which state has the lowest high school graduation rate? Which state has the highest?
"""

df_pct_completed_hs.columns

df_pct_completed_hs.head()
df_pct_completed_hs.isna()

# Reemplazar los guiones '-' con NaN
df_pct_completed_hs['percent_completed_hs'] = df_pct_completed_hs['percent_completed_hs'].replace('-', np.nan)
df_pct_completed_hs['percent_completed_hs'] = df_pct_completed_hs['percent_completed_hs'].astype(float)

# Hacer la media de cada area geografica
df_mean_high_school = df_pct_completed_hs.groupby('Geographic Area')['percent_completed_hs'].mean().reset_index()
# Valores de mayor a menor
df_sorted_HS = df_mean_high_school.sort_values(by='percent_completed_hs', ascending=True)

bar = px.bar(df_sorted_HS, x='Geographic Area', y='percent_completed_hs',
             title='High School Graduation Rate by Geographic Area', color='Geographic Area', color_discrete_map={'Geographic Area': 'lightblue'},
             )
# rotar valores x
bar.update_xaxes(tickangle=45)
bar.update_layout(width=800, height=600)
# quitar fondo azul
bar.update_layout(plot_bgcolor='rgba(0,0,0,0)')


bar.show()

"""# Visualise the Relationship between Poverty Rates and High School Graduation Rates

#### Create a line chart with two y-axes to show if the rations of poverty and high school graduation move together.  
"""



# Crear la figura y los ejes
fig, ax1 = plt.subplots(figsize=(10, 6))

# Graficar la tasa de graduación de la escuela secundaria en el primer eje y
ax1.plot(df_sorted_HS['Geographic Area'], df_sorted_HS['percent_completed_hs'], color='b', marker='o', label='High School Graduation Rate')
ax1.set_xlabel('Geographic Area')
ax1.set_ylabel('High School Graduation Rate (%)', color='b')
ax1.tick_params('y', colors='b')

# Crear el segundo eje y y graficar la tasa de pobreza
ax2 = ax1.twinx()
ax2.plot(df_sorted_HS['Geographic Area'], df_sorted_poverty['poverty_rate'], color='r', marker='s', label='Poverty Rate')
ax2.set_ylabel('Poverty Rate (%)', color='r')
ax2.tick_params('y', colors='r')

# Cambiar la orientación de los valores en el eje x
ax1.set_xticklabels(df_sorted_HS['Geographic Area'], rotation=45, ha='right')
ax2.set_xticklabels(df_sorted_poverty['Geographic Area'], rotation=45, ha='right')


# Añadir título y leyendas
plt.title('Poverty Rate vs High School Graduation Rate')
fig.tight_layout()

# Mostrar la gráfica
plt.show()

"""#### Now use a Seaborn .jointplot() with a Kernel Density Estimate (KDE) and/or scatter plot to visualise the same relationship"""

sns.set(style="whitegrid")
sns.jointplot(x=df_sorted_HS['percent_completed_hs'], y=df_sorted_poverty['poverty_rate'], kind="scatter", color="skyblue", height=7)
plt.xlabel('High School Graduation Rate (%)')
plt.ylabel('Poverty Rate (%)')
plt.show()



"""#### Seaborn's `.lmplot()` or `.regplot()` to show a linear regression between the poverty ratio and the high school graduation ratio."""

# Merge the two DataFrames based on a common column
merged_df = pd.merge(df_pct_completed_hs, df_pct_poverty, on='Geographic Area')
merged_df.head()

# Eliminar una columna específica
merged_df_clean = merged_df.drop(columns=['City_y'])
merged_df_clean.head()

merged_df_clean['percent_completed_hs'] = pd.to_numeric(merged_df_clean['percent_completed_hs'], errors='coerce')
merged_df_clean['poverty_rate'] = pd.to_numeric(merged_df_clean['poverty_rate'], errors='coerce')

# merged_df_clean.isna().values.any()
merged_df_clean.fillna(0)
merged_df_clean.isna().values.any()

merged_df_clean_mean = merged_df_clean.groupby('Geographic Area')[['percent_completed_hs', 'poverty_rate']].mean().reset_index()

merged_df_clean_sample = merged_df_clean_mean.sample(frac=0.5, random_state=42)

merged_df_clean_sample.head()

# lmplot
sns.set(style="whitegrid")
sns.lmplot(x='percent_completed_hs', y='poverty_rate', data=merged_df_clean_sample, height=4)
plt.xlabel('High School Graduation Rate (%)')
plt.ylabel('Poverty Rate (%)')
plt.show()

plt.figure(figsize=(6,3), dpi=150)
with sns.axes_style('darkgrid'):
  ax = sns.regplot(data=merged_df_clean_sample,
                   x='percent_completed_hs',
                   y='poverty_rate',
                   color='#2f4b7c',
                   scatter_kws = {'alpha': 0.3},
                   line_kws = {'color': '#ff7c43'})

  ax.set(ylim=(0, 100),
         xlim=(0, 100),
         ylabel='Poverty Rate',
         xlabel='Percent Completed High School')

"""# Create a Bar Chart with Subsections Showing the Racial Makeup of Each US State

Visualise the share of the white, black, hispanic, asian and native american population in each US State using a bar chart with sub sections.
"""

# df_share_race_city.describe()
# df_share_race_city.isna().values.any()
# df_share_race_city.columns
# df_share_race_city.head()
columns_to_convert = ["share_white", "share_black", "share_native_american", "share_asian", "share_hispanic"]
df_share_race_city[columns_to_convert] = df_share_race_city[columns_to_convert].apply(pd.to_numeric, errors='coerce')

df_share_race_city.fillna(0, inplace=True)
df_share_race_city[columns_to_convert]=df_share_race_city[columns_to_convert].astype(float)
df_share_race_city_sample = df_share_race_city.sample(frac=0.02, random_state=42)
df_share_race_city_sample.head()

# Configurar el gráfico de barras apiladas
fig, ax = plt.subplots(figsize=(14, 12))

# Configurar las categorías y colores
categories = ['share_white', 'share_black', 'share_hispanic', 'share_asian', 'share_native_american']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Crear el gráfico de barras apiladas
df_share_race_city_sample.set_index('Geographic area')[categories].plot(kind='bar', stacked=True, color=colors, ax=ax)

# Añadir título y etiquetas
ax.set_title('Racial Makeup of Each US State.')
ax.set_xlabel('State')
ax.set_ylabel('Subjects')

# Rotar etiquetas del eje x para mejor legibilidad
plt.xticks(fontsize=5, rotation=90)

# Añadir leyenda
plt.legend(title='Race')

# Mostrar gráfico
plt.show()

"""# Create Donut Chart by of People Killed by Race

Hint: Use `.value_counts()`
"""

df_fatalities.describe()
df_fatalities.columns
df_fatalities.isna().values.any()
df_fatalities.head()
# df_fatalities["age"].isna().values.any()

race_counts = df_fatalities["race"].value_counts()

races = race_counts.index
killed = race_counts.values

fig, ax = plt.subplots(figsize=(10, 6))

wedges, texts, autotexts = ax.pie(killed, labels=races, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.3))

# Add a center circle for the donut chart
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

ax.axis('equal')

# Add title
plt.title('People Killed by Race')

# Show the plot
plt.show()

"""# Create a Chart Comparing the Total Number of Deaths of Men and Women

Use `df_fatalities` to illustrate how many more men are killed compared to women.
"""



gender_counts = df_fatalities['gender'].value_counts()

# Plotting
genders = gender_counts.index
counts = gender_counts.values

# Create a bar chart
fig, ax = plt.subplots(figsize=(10, 6))

# Plot bars
ax.bar(genders, counts, color=['blue', 'pink'])

# Add labels and title
ax.set_xlabel('Gender')
ax.set_ylabel('Number of Deaths')
ax.set_title('Total Number of Deaths by Gender')

# Add value labels on top of bars
for i, v in enumerate(counts):
    ax.text(i, v + 0.2, str(v), ha='center', va='bottom')

# Show the plot
plt.show()

"""# Create a Box Plot Showing the Age and Manner of Death

Break out the data by gender using `df_fatalities`. Is there a difference between men and women in the manner of death?
"""

plt.figure(figsize=(12, 6))
sns.boxplot(x='manner_of_death', y='age', hue='gender', data=df_fatalities, palette='Set2')

# Add labels and title
plt.xlabel('Manner of Death')
plt.ylabel('Age')
plt.title('Age Distribution by Manner of Death and Gender')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.show()





"""# Were People Armed?

In what percentage of police killings were people armed? Create chart that show what kind of weapon (if any) the deceased was carrying. How many of the people killed by police were armed with guns versus unarmed?
"""

# Calculate the percentage of armed versus unarmed people
total_individuals = len(df_fatalities)
armed = df_fatalities[df_fatalities['armed'] != 'unarmed']
pct_armed = len(armed) / total_individuals * 100
unarmed = df_fatalities[df_fatalities['armed'] == 'unarmed']
pct_unarmed = len(unarmed) / total_individuals*100

# Calculate the count of each weapon type
weapon_count = df_fatalities['armed'].value_counts()


# Create a bar chart for types of weapons
plt.figure(figsize=(12, 6))
sns.barplot(x=weapon_count.index, y=weapon_count.values, palette='viridis')
plt.xticks(rotation=45)
plt.xlabel('Type of Weapon')
plt.ylabel('Count')
plt.title('Count of Each Weapon Type Carried by Deceased in Police Killings')
plt.show()


plt.figure(figsize=(8, 6))
plt.pie([pct_armed, pct_unarmed], labels=['Armed', 'Unarmed'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=90)
plt.title('Percentage of Armed vs Unarmed People in Police Killings')
plt.show()





"""# How Old Were the People Killed?

Work out what percentage of people killed were under 25 years old.
"""

under_25 = df_fatalities[df_fatalities["age"] < 25]
pct_under_25 = (len(under_25) / len(df_fatalities)) * 100

"""Create a histogram and KDE plot that shows the distribution of ages of the people killed by police."""

df_fatalities['age'] = pd.to_numeric(df_fatalities['age'], errors='coerce')

# Drop rows where 'age' could not be converted to a number (if any)
df_fatalities = df_fatalities.dropna(subset=['age'])

# Plot the histogram and KDE
plt.figure(figsize=(10, 6))
sns.histplot(df_fatalities['age'], kde=True, bins=10, color='blue')

# Add labels and title
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Distribution of Ages of People Killed by Police')

# Show the plot
plt.show()

"""Create a seperate KDE plot for each race. Is there a difference between the distributions?"""

races = df_fatalities['race'].unique()

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Create a KDE plot for each race
for race in races:
    subset = df_fatalities[df_fatalities['race'] == race]
    sns.kdeplot(subset['age'], label=race)

# Add labels and title
plt.xlabel('Age')
plt.ylabel('Density')
plt.title('KDE Plot of Ages of People Killed by Police, Separated by Race')
plt.legend(title='Race')

# Show the plot
plt.show()

"""# Race of People Killed

Create a chart that shows the total number of people killed by race.
"""

sns.set_style("whitegrid")

# Create the countplot
plt.figure(figsize=(10, 6))
sns.countplot(x='race', data=df_fatalities, order=df_fatalities['race'].value_counts().index, palette='viridis')

# Add labels and title
plt.xlabel('Race')
plt.ylabel('Number of People Killed')
plt.title('Total Number of People Killed by Race')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.show()



"""# Mental Illness and Police Killings

What percentage of people killed by police have been diagnosed with a mental illness?
"""

mental_illness_count = df_fatalities[df_fatalities['signs_of_mental_illness'] == True]['id'].count()

# Calculate the total number of people killed by police
total_count = df_fatalities['id'].count()

# Calculate the percentage
percentage_mental_illness = (mental_illness_count / total_count) * 100
print(percentage_mental_illness)



"""# In Which Cities Do the Most Police Killings Take Place?

Create a chart ranking the top 10 cities with the most police killings. Which cities are the most dangerous?  
"""

# Get the top 10 cities with the most police killings
top_10_cities = df_fatalities['city'].value_counts().head(10)

# Create a bar plot
plt.figure(figsize=(10, 6))
top_10_cities.plot(kind='bar', color='skyblue')
plt.title('Top 10 Cities with the Most Police Killings')
plt.xlabel('City')
plt.ylabel('Number of Police Killings')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

df_fatalities.columns

"""# Rate of Death by Race

Find the share of each race in the top 10 cities. Contrast this with the top 10 cities of police killings to work out the rate at which people are killed by race for each city.
"""

# Get the top 10 cities with the most police killings
top_10_cities = df_fatalities['city'].value_counts().head(10).index.tolist()

# Create an empty DataFrame to store the results
city_race_share = pd.DataFrame()

# Iterate over the top 10 cities
for city in top_10_cities:
    # Filter the DataFrame for the current city
    city_data = df_fatalities[df_fatalities['city'] == city]

    # Calculate the total number of police killings in the city
    total_killings = city_data.shape[0]

    # Calculate the share of each race in the city
    race_share = (city_data['race'].value_counts() / total_killings).reset_index()
    race_share.columns = ["Race", city]
    # Append the results to the DataFrame
    if city_race_share.empty:
        city_race_share = race_share
    else:
        city_race_share = city_race_share.merge(race_share, on="Race", how="outer")

# Fill NaN values with 0
city_race_share.fillna(0, inplace=True)

# Set 'Race' as the index
city_race_share.set_index('Race', inplace=True)

# Plot the results
plt.figure(figsize=(12, 6))
city_race_share.plot(kind='bar', stacked=True)
plt.title('Share of Police Killings by Race in Top 10 Cities')
plt.xlabel('Race')
plt.ylabel('Share of Police Killings')
plt.legend(title='City', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



"""# Create a Choropleth Map of Police Killings by US State

Which states are the most dangerous? Compare your map with your previous chart. Are these the same states with high degrees of poverty?
"""

# Agrupar los datos por estado y contar los asesinatos policiales
state_killings = df_fatalities['state'].value_counts().reset_index()
state_killings.columns = ['state', 'killings']

# Crear el mapa de coropletas
fig = px.choropleth(
    state_killings,
    locations='state',
    locationmode='USA-states',
    color='killings',
    color_continuous_scale='Reds',
    scope='usa',
    labels={'killings': 'Number of Killings'},
    title='Police Killings by US State'
)

# Mostrar el mapa
fig.show()

df_fatalities.columns

df_pct_poverty.columns

state_poverty = df_pct_poverty['Geographic Area'].value_counts().reset_index()
state_poverty.columns = ['Geographic Area', 'poverty_rate']


fig_poverty = px.choropleth(
    state_poverty,
    locations='Geographic Area',
    locationmode='USA-states',
    color='poverty_rate',
    color_continuous_scale='Blues',
    scope='usa',
    labels={'poverty_rate': 'Poverty Rate (%)'},
    title='Poverty Rate by US State'
)

# Mostrar el mapa de pobreza
fig_poverty.show()

"""# Number of Police Killings Over Time

Analyse the Number of Police Killings over Time. Is there a trend in the data?
"""

# Asegurarse de que la columna 'date' está en formato de fecha y hora
df_fatalities['date'] = pd.to_datetime(df_fatalities['date'])

# Agrupar los datos por año y mes
df_fatalities['year_month'] = df_fatalities['date'].dt.to_period('M')
killings_over_time = df_fatalities['year_month'].value_counts().sort_index()

# Convertir el PeriodIndex a un índice de fecha para la visualización
killings_over_time.index = killings_over_time.index.to_timestamp()

# Crear el gráfico de líneas
plt.figure(figsize=(12, 6))
plt.plot(killings_over_time.index, killings_over_time.values, marker='o')
plt.title('Number of Police Killings Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Killings')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()







"""# Epilogue

Now that you have analysed the data yourself, read [The Washington Post's analysis here](https://www.washingtonpost.com/graphics/investigations/police-shootings-database/).
"""

