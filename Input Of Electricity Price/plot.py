import pandas as pd
import matplotlib.pyplot as plt

importing_name_plot= input('Import the name of your CSV-file: ')
df = pd.read_csv(f"{importing_name_plot}.csv")

# Plot specific area given by the user 
# plot a line graph of the data
df.plot(x='Timestamp', y='SpotPriceEUR', kind='line')

# add a title to the plot
plt.title('Line graph of data')

# show the plot
plt.show()