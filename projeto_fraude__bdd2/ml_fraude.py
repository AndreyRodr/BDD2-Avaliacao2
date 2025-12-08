import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix, 
                            accuracy_score, roc_curve, auc, 
                            precision_recall_curve, average_precision_score)

# Conexão com a Camada Ouro (SQLite)
GOLD_DIR = os.path.expanduser("~/projeto_fraude__bdd2/data_lakehouse/gold")
db_path = f'{GOLD_DIR}/fraud_analysis.sqlite'
conn = sqlite3.connect(db_path)

print(f"Carregando dados do SQLite em: {db_path} ...")
try:
    df = pd.read_sql("SELECT * FROM final_transactions", conn)
    print("Dados carregados com sucesso!")
except Exception as e:
    print(f"Erro ao ler o banco: {e}")
    exit()
finally:
    conn.close()

# Separação de Features (X) e Target (y)
X = df.drop(['Class', 'Time'], axis=1)
y = df['Class']

# Divisão em Treino e Teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Treinamento com verbose=2 para mostrar o progresso
print("\n--- Iniciando Treinamento do Random Forest ---")
start_time = time.time()

clf = RandomForestClassifier(
    n_estimators=100, 
    random_state=42, 
    verbose=2,     # Mostra o log de construção das árvores
    n_jobs=-1      # Usa todos os núcleos do processador
)

clf.fit(X_train, y_train)

end_time = time.time()
print(f"\nTreinamento concluído em {end_time - start_time:.2f} segundos.")

# Predições
print("\nGerando predições e probabilidades...")
y_pred = clf.predict(X_test)

y_prob = clf.predict_proba(X_test)[:, 1] 

# Relatório textual
print("\n--- Relatório de Classificação ---")
print(classification_report(y_test, y_pred))

# Geração do Painel de Gráficos (Dashboard)
print("Gerando gráficos de performance...")

# Cria uma figura com 2 linhas e 2 colunas
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
plt.subplots_adjust(hspace=0.3, wspace=0.3)

# GRÁFICO 1: Matriz de Confusão (Canto Superior Esquerdo)
conf_matrix = confusion_matrix(y_test, y_pred)
nomes_classes = ['Não Fraude', 'Fraude']
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=nomes_classes, yticklabels=nomes_classes, ax=axes[0, 0])
axes[0, 0].set_title('1. Matriz de Confusão')
axes[0, 0].set_ylabel('Real')
axes[0, 0].set_xlabel('Previsto')

# GRÁFICO 2: Curva ROC (Canto Superior Direito)
fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

axes[0, 1].plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
axes[0, 1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
axes[0, 1].set_xlim([0.0, 1.0])
axes[0, 1].set_ylim([0.0, 1.05])
axes[0, 1].set_xlabel('Taxa de Falsos Positivos')
axes[0, 1].set_ylabel('Taxa de Verdadeiros Positivos (Recall)')
axes[0, 1].set_title('2. Curva ROC (Capacidade de Separação)')
axes[0, 1].legend(loc="lower right")
axes[0, 1].grid(alpha=0.3)

# GRÁFICO 3: Curva Precision-Recall (Canto Inferior Esquerdo)
precision, recall, _ = precision_recall_curve(y_test, y_prob)
avg_precision = average_precision_score(y_test, y_prob)

axes[1, 0].plot(recall, precision, color='green', lw=2, label=f'Avg Precision = {avg_precision:.2f}')
axes[1, 0].set_xlabel('Recall (Revocação)')
axes[1, 0].set_ylabel('Precision (Precisão)')
axes[1, 0].set_title('3. Curva Precision-Recall (Foco na Fraude)')
axes[1, 0].legend(loc="lower left")
axes[1, 0].grid(alpha=0.3)

# GRÁFICO 4: Importância das Features (Canto Inferior Direito)
# Pega as 10 variáveis mais importantes para o modelo
importances = pd.Series(clf.feature_importances_, index=X.columns)
top_features = importances.nlargest(10).sort_values()

top_features.plot(kind='barh', color='#4c72b0', ax=axes[1, 1])
axes[1, 1].set_title('4. Top 10 Features Mais Importantes')
axes[1, 1].set_xlabel('Importância Relativa')

# Salvar tudo em um arquivo só
output_img = "painel_metricas_completo.png"
plt.savefig(output_img, dpi=300, bbox_inches='tight')
print(f"\nPainel completo salvo com sucesso: {output_img}")