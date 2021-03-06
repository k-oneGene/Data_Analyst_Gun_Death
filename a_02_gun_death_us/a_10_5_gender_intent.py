import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gun_data = pd.read_csv('full_data.csv', index_col='Unnamed: 0')

education_replace = {
    'Less than HS': 1,
    'HS/GED': 2,
    'Some college': 3,
    'BA+': 4,
    np.NaN: 5
}

gun_data['education'] = gun_data['education'].map(education_replace)

gun_data['day'] = 1
gun_data['date'] = gun_data['year'].astype(str) + '-' + gun_data['month'].astype(str) + '-' + gun_data['day'].astype(str)
gun_data['date'] = pd.to_datetime(gun_data['date'], format='%Y-%m-%d')

# ==================================================================

"""
Further investigation into suicide and homicide by race and gender 
"""

race_mapping = {
    "Asian/Pacific Islander": 15159516 + 674625,
    "Native American/Native Alaskan": 3739506,
    "Black": 40250635,
    "Hispanic": 44618105,
    "White": 197318956
}

def race_per_fix(row):
    race = row['x_label']
    count = row['count']/race_mapping[race] * 100000
    return count


plt.style.use('seaborn')

# Makes per 100,000 from total number
def make_graph_data(df, col):
    count_by_col = df[col].value_counts(sort=False)
    count_by_col = count_by_col.to_frame('count')
    count_by_col['x_label'] = count_by_col.index
    count_by_col = count_by_col.sort_index(0)
    count_by_col_per = count_by_col.apply(race_per_fix, axis=1)

    print(df[col].value_counts())

    return count_by_col_per, count_by_col['x_label']


######
# Finding intent of gun, male vs female
######

gun_data_male_intent = gun_data[gun_data['sex'] == 'M']
gun_data_female_intent = gun_data[gun_data['sex'] == 'F']

gun_data_male_intent_factor = gun_data_male_intent['race'].value_counts() / gun_data_female_intent['race'].value_counts()
print('How many more times likely it\'s male with gun.')
print(gun_data_male_intent_factor)

g_data_race_male, g_x_race_male = make_graph_data(gun_data_male_intent, 'race')
g_data_race_female, g_x_race_female = make_graph_data(gun_data_female_intent, 'race')

#Drawing graph
fig, ax = plt.subplots()

ind = np.arange(len(g_data_race_male))
width = 0.35

rect1 = ax.bar(ind, g_data_race_male, width, color='royalblue')
rect2 = ax.bar(ind + width, g_data_race_female, width, color='violet')

ax.set_xticks(ind + width / 2)
ax.set_xticklabels(g_x_race_male)


ax.set_title('Gun Deaths')
ax.set_xlabel('Gender')
ax.set_ylabel('Gun death per 100000')

ax.legend((rect1[0], rect2[0]), ('Male', 'Female'))

plt.tight_layout()
plt.show()