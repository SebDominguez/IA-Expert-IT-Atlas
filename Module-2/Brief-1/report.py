import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt

# original
#df = pd.read_csv("./resources/fichier-de-donnees-numeriques.csv")

# cleaned
df = pd.read_csv("./resources/cleaned_data.csv")



# on prend tout (illisible)
# msno.matrix(df)

# on prend 500 au pif
msno.matrix(df.sample(500))

plt.show()
