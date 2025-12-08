 # **Projeto Acadêmico - IFSP Jacareí (2025)** - **Disciplina:** Banco de Dados 2

## Credit Card Fraud Detection Pipeline & Data Lakehouse

### 🛠️ Tecnologias e Ferramentas

 - Python;
	 - Pandas;
	 - Scikit Learn;
	 - Seaborn;
	 - PyMongo;
 - Apache Airflow;
 - Docker;
 - MongoDB;
 - MySQL;
 - SQLite


## 📋 Sobre o Projeto

Este projeto consiste em uma solução de engenharia de dados ponta a ponta para detecção de fraudes em cartões de crédito. O objetivo principal foi simular um ambiente corporativo real, implementando um **Data Lakehouse** automatizado que ingere dados de fontes heterogêneas (Relacional e NoSQL), processa-os através de uma arquitetura medalhão e alimenta um modelo de Machine Learning.

O sistema foi desenvolvido em um ambiente virtualizado (Ubuntu Server 25), utilizando **Docker** para serviços de banco de dados e **Apache Airflow** para orquestração do pipeline de ETL.

## 📐 Arquitetura e Pipeline de Dados

O projeto adota a Arquitetura Medalhão, garantindo a evolução da qualidade dos dados em três camadas lógicas.

### 1. Fontes de Dados (Data Sources)
Para simular a complexidade real, o dataset original foi particionado em dois fluxos:
* **MySQL (Docker):** Armazena 50% dos dados (Transacional/On-premise).
* **MongoDB Atlas (Cloud):** Armazena 50% dos dados em formato JSON (NoSQL/Cloud).

### 2. Pipeline ETL (Orquestrado via Airflow)

| Camada | Descrição | Formato |
| :--- | :--- | :--- |
| **🥉 Bronze (Raw)** | Ingestão bruta dos dados do MySQL e MongoDB, preservando integridade original. | `.txt` |
| **🥈 Silver (Refined)** | Limpeza, padronização, feature engineering e transformação (Pandas). | `DataFrame` |
| **🥇 Gold (Curated)** | Consolidação final em tabelas relacionais prontas para consumo analítico. | `SQLite` |

## 🛠️ Tech Stack & Infraestrutura

O desenvolvimento foi realizado remotamente via **VS Code** conectado a uma Máquina Virtual, garantindo paridade entre os ambientes de desenvolvimento e produção.

* **Sistema Operacional:** Ubuntu Server v25 (VM)
* **Linguagem:** Python 3 (venv)
* **Containerização:** Docker
* **Orquestração:** Apache Airflow
* **Databases:** MySQL (Docker), MongoDB Atlas, SQLite
* **Machine Learning:** Scikit-Learn

## 🤖 Modelo de Machine Learning

Com os dados consolidados na camada Gold, foi desenvolvido um modelo classificador para identificar transações fraudulentas.

### Escolha do Algoritmo: Random Forest Classifier
Optou-se pelo método de *Ensemble* (Floresta Aleatória) que trás:
1.  **Robustez ao Desbalanceamento:** O *dataset* possui apenas 136 fraudes contra 85.307 transações normais.
2.  **Generalização (Bagging):** Redução de variância e prevenção de *overfitting*.
3.  **Features Brutas:** Capacidade de lidar com variáveis numéricas sem necessidade de normalização excessiva.

## 📊 Resultados e Métricas

O modelo foi treinado com 70% dos dados e testado com 30% (85.443 transações).

### Desempenho no Teste

| Métrica | Valor | Interpretação |
| :--- | :--- | :--- |
| **Precision (Fraude)** | **95%** | Quando o modelo alerta fraude, ele está quase sempre correto. |
| **Recall (Fraude)** | **82%** | O modelo recuperou 82% de todas as fraudes reais. |
| **Falsos Positivos** | **6** | Apenas 6 clientes legítimos seriam bloqueados indevidamente (excelente UX). |
| **Acurácia Global** | 99.96% | Alta, porém métrica secundária devido ao desbalanceamento. |

> **Conclusão:** A arquitetura técnica (Docker + Cloud + Python) provou-se robusta, e o modelo alcançou um equilíbrio ideal entre segurança e experiência do usuário, minimizando falsos positivos.


## 🏗️ Guia de Configuração do Ambiente

Este guia descreve os passos necessários para configurar o ambiente de desenvolvimento, incluindo a preparação do editor local e as dependências da Máquina Virtual (VM).

#### 1. Configuração Local (VS Code)

Para permitir o desenvolvimento remoto, é necessário instalar a extensão de conexão SSH no Visual Studio Code.

1. Abra o VS Code.
2. Acesse a aba de extensões (ou pressione `Ctrl+Shift+X`).
3. Pesquise e instale a seguinte extensão:
   - **Nome:** Remote - SSH
   - **ID:** `ms-vscode-remote.remote-ssh`

#### 2. Configuração da Máquina Virtual (VM)

Acesse o terminal da sua VM e execute os comandos abaixo. Isso garantirá que o sistema esteja atualizado e possua as ferramentas de compilação, controle de versão e o servidor SSH instalados.

```bash
# a. Atualizar a lista de pacotes do sistema
sudo apt update

# b. Instalar dependências essenciais (Build tools, Git, Curl, SSH Server)
sudo apt install -y build-essential tar wget curl git openssh-server 
```
Após a instalação na VM, verifique se o serviço SSH está ativo com o comando:
```bash
# c. Verificar status do serviço SSH
sudo systemctl status ssh
```

#### 3. Conexão via SSH no VS Code

Antes de iniciar, descubra o IP da sua Máquina Virtual (VM) executando `ip addr` ou verificando a configuração de rede.
> **Nota:** O IP aparecerá no formato `inet: 192.168.X.X`.

1. No VS Code, abra a paleta de comandos: `Ctrl + Shift + P`.
2. Digite e selecione: **Remote-SSH: Connect to Host...**.
3. Insira a string de conexão:
```
   aluno@<ip da vm>
```
>_(Substitua `<ip da vm>` pelo IP anotado anteriormente)_.
4. Pressione `ENTER`. 
5. Selecione o sistema operacional **Linux**. 
6. Digite a senha da VM quando solicitado. 
7. Após conectar, abra a pasta raiz do projeto no VS Code (**File > Open Folder**).

#### 4. Configuração do Ambiente Virtual (Python)

No terminal integrado do VS Code (conectado à VM), execute os passos abaixo:

1.  **Criar o ambiente virtual:**
``` bash
python3 -m venv <nome_venv>
```
1. **Ativar o ambiente:**
``` bash
source <nome_venv>/bin/activate]
```
> Se o nome do ambiente virtual aparecer entre parênteses no começo da linha do terminal, ele foi ativado com sucesso.

1.  **Instalar dependências:**
``` bash
pip install -r requirements.txt
```

#### 5. Preparação dos Dados e Infraestrutura

Navegue até a pasta do projeto e prepare os dados iniciais com os comandos:
``` bash
# Acessar diretório com o script
cd ./projeto_fraude__bdd2/

# Executar script de preparação
python3 ./preparar_dados.py
```
Posteriormente, inicie o container MySQL necessário para o projeto:
``` bash
docker run --name <nome-do-container> \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=fraud_detection \
  -p 3306:3306 \
  -d mysql:5.7
```
Por fim, popule os bancos de dados com os scripts de ingestão:
``` bash
# Ingestão para banco de dados relacional
python3 ingestao_mysql.py

# Ingestão para banco de dados NoSQL
python3 ingestao_mongodb.py
```
#### 6. Execução do Pipeline (Apache Airflow)
 
 1. **Inicializar o Airflow:** Defina a variável de ambiente e prepare o banco de dados (SQLite) do Airflow:
 ``` bash
 export AIRFLOW_HOME=~/airflow
airflow db migrate
airflow standalone
 ```

2.  **Acessar a Interface:**
-  O VS Code exibirá um pop-up com a opção **"Open in Browser"** (ou Forward Port 8080). Clique nele.
-   Faça login com as credenciais fornecidas no terminal pelo comando `airflow standalone`.

  3. **Executar a DAG:**

-   Na página inicial de **DAGs**, procure por: `fraud_detection_etl_pipeline`.
    
-   Clique no botão **Trigger** (ícone de "play") na coluna de ações.
    
-   Confirme clicando em **Trigger** novamente.
 
 Com as DAGs prontas, é possível prosseguir a para a etapa de Machine Learning.

#### 7. Execução do Machine Learning

Após o processamento dos dados pelo Airflow, siga os passos abaixo para gerar as análises do modelo:

1. **Parar o Airflow:**
Vá até o terminal onde o comando `airflow standalone` está rodando e pressione `Ctrl + C` para interromper a execução.

3. **Executar o script de ML:**
   Execute o script responsável pelo treinamento e avaliação do modelo de detecção de fraudes:

   ```bash
   python3 ml_fraude.py
   ````
   
## 👥 Autores

| Nome | Função / Responsabilidade |
| :--- | :--- |
| **Andrey Rodrigues** | Preparação de dados, ETL, Data Lakehouse |
| **Guilherme Augusto Frazão** | Documentação (README) |
| **João Pedro de Andrade** | Relatório Técnico |
| **Lucas Nascimento** | Desenvolvimento de Machine Learning |

---
*Instituto Federal de Educação, Ciência e Tecnologia de São Paulo - Campus Jacareí - 2025.2*
