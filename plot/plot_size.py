import pandas as pd
import matplotlib.pyplot as plt

def load_excel_data(file_path, sheet_name):
    try:
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

# Example usage
file_path = './certSSAT.xlsx'
low_name = 'low_size'
up_name = 'up_size'

# Load the dataset from Excel
low_dataset = load_excel_data(file_path, low_name)
up_dataset = load_excel_data(file_path, up_name)

# Display the loaded dataset
low_cnf  = low_dataset.iloc[:, 1]
low_nnf  = low_dataset.iloc[:, 2]
low_cpog = low_dataset.iloc[:, 3]
up_cnf  = up_dataset.iloc[:, 1]
up_nnf  = up_dataset.iloc[:, 2]
up_cpog = up_dataset.iloc[:, 3]

# Create scatter plot with log scales
#plt.scatter(overall_x, overall_y, color='orange', s=32, label="full proof")
#plt.scatter(low_x, low_y, color='blue', s=16, marker='^', label="lower bound proof")

plt.scatter(up_nnf, up_cpog, color='orange',  s=32, label=r"$(\phi \rightarrow \psi_{G_u})$ vs. $\psi_{G_u}$" )
plt.scatter(low_nnf, low_cpog, color='blue',  s=15, marker='^',label=r"$(\psi_{G_l} \rightarrow \phi)$ vs. $\psi_{G_l}$" )


# Set log scale for both axes
plt.xscale('log')
plt.yscale('log')

# Add labels and title
plt.xlabel('Dec-DNNF ($\#$clauses in CNF encoding)', fontsize=11)
plt.ylabel('CPOG ($\#$clauses)', fontsize=11)

# Add light grey grid lines
plt.grid(color='lightgrey', linestyle='--', linewidth=0.5, which='both', alpha=0.5)

# Add a reference line y=x
plt.plot([100, 1000000000], [100, 1000000000],  color='lightgray', linestyle='-', linewidth=1)
plt.plot([100, 100000000],  [1000, 1000000000], color='lightgray', linestyle='-', linewidth=1)
plt.plot([100, 10000000],   [10000, 1000000000], color='lightgray', linestyle='-', linewidth=1)
#plt.plot([100, 1000000],    [100000, 1000000000], color='lightgray', linestyle='-', linewidth=1)


# Add LaTeX formatted label at the midpoint of the reference line
plt.text(1000000000, 1000000000, r'$1 \times$',   color='black', fontsize=10, ha='center', va='center')
plt.text(100000000,  1000000000, r'$10 \times$', color='black', fontsize=10, ha='center', va='center')
plt.text(10000000,   1000000000, r'$100 \times$', color='black', fontsize=10, ha='center', va='center')
#plt.text(10, 10000, r'$1000 \times$', color='black', fontsize=10, ha='center', va='center')

# Show the plot with legend
plt.legend()

# Show the plot
plt.show()
