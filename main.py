from input_management import read_input
from molecule import MonatomicGas
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

matplotlib.use('Agg')

# --- Basic Implementation --- #

input_data = read_input('input.txt')
gas = MonatomicGas('Monatomic', input_data, 'NVT')
print(gas.print_properties())

# ----------------------------- #
"""
# --- All Monatomic Gas Implementation --- #
# with plotting
fig, axs = plt.subplots(2, 4, figsize=(15, 10))

subplot_indices = {
    'A': (0, 0,), 'E': (0, 1,), 'H': (0, 2), 'G': (0, 3),
    'S': (1, 0), 'P': (1, 1), 'Cv': (1, 2), 'Cp': (1, 3),
}

gasses = ['He', 'Ne', 'Ar', 'Kr', 'Xe']
for gas_name in gasses:
    input_data = read_input(f'input_{gas_name}.txt')
    gas = MonatomicGas(gas_name, input_data, 'NVT')
    properties = gas.properties
    del properties['P_bar'] 
    for prop, values in properties.items():
        row, col = subplot_indices[prop]
        axs[row, col].bar(gas_name, values, label=f'{prop}')
        axs[row, col].set_title(prop)
        axs[row, col].set_ylabel(f'{prop} ({gas.units_dict[prop]})')
        axs[row, col].set_xlabel('Monatomic Gas')
        
plt.tight_layout()
plt.savefig('properties.jpg')

# ----------------------------- #

# --- Compare Entropy with Textbook --- #
text_exp = {
    'He': 30.13,
    'Ne': 34.95,
    'Ar': 36.98,
    'Kr': 39.19,
    'Xe': 40.53
}
text_calc = {
    'He': 30.11,
    'Ne': 34.94,
    'Ar': 36.97,
    'Kr': 39.18,
    'Xe': 40.52
}

# convert e.u. to J/mol.K
constant = 4.18
text_exp = {key: value * constant for key, value in text_exp.items()}
text_calc = {key: value * constant for key, value in text_calc.items()}

fig, axs = plt.subplots()
df = pd.DataFrame(columns=['Gas', 'Calculated', 'Text_Calc', 'Text_Exp'])
df['Gas'] = gasses
df['Text_Exp'] = text_exp.values()
df['Text_Calc'] = text_calc.values()
S_array = []
for gas_name in gasses:
    input_data = read_input(f'input_{gas_name}.txt')
    gas = MonatomicGas(gas_name, input_data, 'NVT')
    S = gas.properties['S']
    # plot
    axs.scatter(gas_name, S, label=f'{gas_name} Calculated', color='blue')
    axs.scatter(gas_name, text_exp[gas_name], label=f'Text_Experimental', color='red')
    axs.scatter(gas_name, text_calc[gas_name], label=f'Text_Calculated', color='green')
    # add to array
    S_array.append(S)

# manipulate dataframe
df['Calculated'] = S_array
df['%Diff_EXP'] = 100 * (df['Calculated'] - df['Text_Exp']) / df['Text_Exp']
df = df.round(1)
# Create custom legend
custom_lines = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='My Calculation'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Textbook Experimental'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Textbook Calculated')
]
axs.legend(handles=custom_lines, loc='upper left')
axs.set_title('Entropy of Monatomic Gases')
axs.set_ylabel('Entropy (J/mol.K)')
axs.set_xlabel('Monatomic Gas')

plt.savefig('entropy.jpg')
df.to_csv('entropy.csv')
print(df)