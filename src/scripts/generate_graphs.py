import pandas as pd
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns  # type: ignore

# Lire les données du fichier CSV
df = pd.read_csv('./Report/comparison_results.csv')

# Convertir les colonnes en types appropriés
df['MongoDB_time'] = df['MongoDB_time'].replace('N/A', 0).astype(float)
df['MONGO_JSON_time'] = df['MONGO_JSON_time'].replace('N/A', 0).astype(float)
df['REDIS_JSON_time'] = df['REDIS_JSON_time'].replace('N/A', 0).astype(float)
df['Difference_MONGO_JSON'] = df['Difference_MONGO_JSON'].replace('N/A', 0).astype(float)
df['Difference_REDIS_JSON'] = df['Difference_REDIS_JSON'].replace('N/A', 0).astype(float)
df['Percentage_Diff_MONGO_JSON'] = df['Percentage_Diff_MONGO_JSON'].replace('N/A', '0%').str.rstrip('%').astype(float)
df['Percentage_Diff_REDIS_JSON'] = df['Percentage_Diff_REDIS_JSON'].replace('N/A', '0%').str.rstrip('%').astype(float)

# Configurer le style de Seaborn
sns.set(style='whitegrid')

# Exclure la ligne 'Total' pour les graphiques des fonctions individuelles
df_functions = df[df['function_name'] != 'Total']

# --- Graphique des Temps d'Exécution des Fonctions Individuelles ---
plt.figure(figsize=(14, 8))

# Positions des barres
bar_width = 0.25
index = pd.Index(range(len(df_functions['function_name'])))

# Création du DataFrame pour faciliter le plotting avec Seaborn
plot_data = pd.DataFrame({
  'Fonction': df_functions['function_name'],
  'MongoDB': df_functions['MongoDB_time'],
  'MONGO_JSON': df_functions['MONGO_JSON_time'],
  'REDIS_JSON': df_functions['REDIS_JSON_time']
})

# Conversion du DataFrame en format long pour Seaborn
plot_data_melted = plot_data.melt(id_vars='Fonction', var_name='Méthode', value_name='Temps')

# Création du graphique
ax = sns.barplot(
  x='Fonction',
  y='Temps',
  hue='Méthode',
  data=plot_data_melted,
  palette={'MongoDB': 'steelblue', 'MONGO_JSON': 'seagreen', 'REDIS_JSON': 'darkorange'}
)

# Ajouter les valeurs numériques sur les barres
for p in ax.patches:
  height = p.get_height()
  if height > 0:
    ax.annotate(f'{height:.4f}',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom',
                fontsize=8,
                rotation=90,
                xytext=(0, 5),
                textcoords='offset points')

# Ajuster les étiquettes et le titre
ax.set_xlabel('Fonctions', fontsize=12)
ax.set_ylabel('Temps d\'exécution (secondes)', fontsize=12)
ax.set_title('Comparaison des Temps d\'Exécution par Fonction', fontsize=16)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.legend(title='Méthode', fontsize=10, title_fontsize=12)

plt.tight_layout()
plt.savefig('Report/img/execution_times_comparison_functions.png', dpi=300)
plt.show()

# --- Graphique des Temps Totaux ---
plt.figure(figsize=(10, 6))

total_times = df[df['function_name'] == 'Total'][['MongoDB_time', 'MONGO_JSON_time', 'REDIS_JSON_time']].iloc[0]
methods = ['MongoDB', 'MONGO_JSON', 'REDIS_JSON']
times = [total_times['MongoDB_time'], total_times['MONGO_JSON_time'], total_times['REDIS_JSON_time']]

# Création du DataFrame pour le graphique
total_plot_data = pd.DataFrame({
  'Méthode': methods,
  'Temps Total': times
})

ax = sns.barplot(
  x='Méthode',
  y='Temps Total',
  data=total_plot_data,
  palette=['steelblue', 'seagreen', 'darkorange']
)

# Ajouter les valeurs numériques sur les barres
for p in ax.patches:
  height = p.get_height()
  ax.annotate(f'{height:.4f}',
              (p.get_x() + p.get_width() / 2., height),
              ha='center', va='bottom',
              fontsize=12,
              xytext=(0, 8),
              textcoords='offset points')

# Ajuster les étiquettes et le titre
ax.set_xlabel('Méthodes', fontsize=12)
ax.set_ylabel('Temps d\'exécution total (secondes)', fontsize=12)
ax.set_title('Comparaison des Temps d\'Exécution Totaux', fontsize=16)

plt.tight_layout()
plt.savefig('Report/img/execution_times_comparison_total.png', dpi=300)
plt.show()
