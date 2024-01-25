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
overall_name = 'overall_plot'
eval_name = 'eval_plot'
low_name = 'low_plot'
up_name = 'up_plot'
gen_check_name = 'gen_check_plot'

# Load the dataset from Excel
overall_dataset = load_excel_data(file_path, overall_name)
eval_dataset = load_excel_data(file_path, eval_name)
low_dataset = load_excel_data(file_path, low_name)
gen_check_dataset = load_excel_data(file_path, gen_check_name)

# Display the loaded dataset
overall_x = overall_dataset.iloc[:, 1]
overall_y = overall_dataset.iloc[:, 2]
eval_x = eval_dataset.iloc[:, 1]
eval_y = eval_dataset.iloc[:, 2]
low_x = low_dataset.iloc[:, 1]
low_y = low_dataset.iloc[:, 5]
check_x = gen_check_dataset.iloc[:,1]
check_y = gen_check_dataset.iloc[:,8]
gen_x = gen_check_dataset.iloc[:,1 ]
gen_y = gen_check_dataset.iloc[:,5 ]

# Create scatter plot with log scales
plt.scatter(overall_x, overall_y, color='orange', s=32, label="complete (tight bound) verification")
plt.scatter(low_x, low_y, color='blue', s=16, marker='^', label="partial (lower bound) verification")

#plt.scatter(gen_x, gen_y, color='darkblue',  s=32, marker='s',label="cpog-gen" )
#plt.scatter(check_x, check_y, color='dodgerblue', s=16, marker='^', label="cpog-check")
#plt.scatter(eval_x, eval_y,   color='cyan',   s=8, label="EvalSSAT")


# Set log scale for both axes
plt.xscale('log')
plt.yscale('log')

# Add labels and title
plt.xlabel('SharpSSAT  (seconds)', fontsize=11)
#plt.ylabel('cert-SSAT subprocess (seconds)', fontsize=11)
plt.ylabel('cert-SSAT run (seconds)', fontsize=11)

# Add light grey grid lines
plt.grid(color='lightgrey', linestyle='--', linewidth=0.5, which='both', alpha=0.5)

# Add a reference line y=x
plt.plot([0.1, 1000], [0.001, 10],  color='lightgray', linestyle='-', linewidth=1)
plt.plot([0.01, 1000], [0.001, 100],  color='lightgray', linestyle='-', linewidth=1)
plt.plot([0.002, 1000], [0.002, 1000],  color='lightgray', linestyle='-', linewidth=1)
plt.plot([0.002, 1000],  [0.02, 10000], color='lightgray', linestyle='-', linewidth=1)
plt.plot([0.002, 100],    [0.2, 10000], color='lightgray', linestyle='-', linewidth=1)
plt.plot([0.002, 10],       [2, 10000], color='lightgray', linestyle='-', linewidth=1)


# Add LaTeX formatted label at the midpoint of the reference line
plt.text(800, 10, r'$0.01 \times$',   color='black', fontsize=10, ha='center', va='center')
plt.text(900, 100, r'$0.1 \times$',   color='black', fontsize=10, ha='center', va='center')
plt.text(1000, 1000, r'$1 \times$',   color='black', fontsize=10, ha='center', va='center')
plt.text(1000, 10000, r'$10 \times$', color='black', fontsize=10, ha='center', va='center')
plt.text(100, 10000, r'$100 \times$', color='black', fontsize=10, ha='center', va='center')
plt.text(10, 10000, r'$1000 \times$', color='black', fontsize=10, ha='center', va='center')

# Show the plot with legend
plt.legend(fontsize=10, loc='lower right')

# Show the plot
plt.show()
