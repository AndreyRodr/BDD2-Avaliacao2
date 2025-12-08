## Avaliação 2 Banco de Dados

# 🛡️ Credit Card Fraud Detection Pipeline & Data Lakehouse

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-Orchestration-red?style=for-the-badge&logo=apacheairflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Relational-orange?style=for-the-badge&logo=mysql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Machine_Learning-yellow?style=for-the-badge&logo=scikitlearn&logoColor=black)

> **Projeto Acadêmico - IFSP Jacareí (2025)** > **Disciplina:** Banco de Dados 2

---

## 📋 Sobre o Projeto

Este projeto consiste em uma solução de **Engenharia de Dados ponta a ponta** para detecção de fraudes em cartões de crédito. O objetivo principal foi simular um ambiente corporativo real, implementando um **Data Lakehouse** automatizado que ingere dados de fontes heterogêneas (Relacional e NoSQL), processa-os através de uma Arquitetura Medalhão e alimenta um modelo de Machine Learning.

O sistema foi desenvolvido em um ambiente virtualizado (Ubuntu Server 25), utilizando **Docker** para serviços de banco de dados e **Apache Airflow** para orquestração do pipeline de ETL.

## 🏗️ Arquitetura e Pipeline de Dados

O projeto adota a **Arquitetura Medalhão**, garantindo a evolução da qualidade dos dados em três camadas lógicas.

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

O desenvolvimento foi realizado remotamente via **VS Code ** conectado a uma Máquina Virtual, garantindo paridade entre os ambientes de desenvolvimento e produção.

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
1.  **Robustez ao Desbalanceamento:** O dataset possui apenas 136 fraudes contra 85.307 transações normais.
2.  **Generalização (Bagging):** Redução de variância e prevenção de overfitting.
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

## 👥 Autores

| Nome | Função / Responsabilidade |
| :--- | :--- |
| **Andrey Rodrigues** | Preparação de dados, ETL, Data Lakehouse |
| **Guilherme Augusto Frazão** | Documentação (README) |
| **João Pedro de Andrade** | Relatório Técnico |
| **Lucas Nascimento** | Desenvolvimento de Machine Learning |

---
*Instituto Federal de Educação, Ciência e Tecnologia de São Paulo - Campus Jacareí*

## ⚠️ Disclaimer

Este projeto foi desenvolvido estritamente para fins acadêmicos como parte da disciplina de Banco de Dados 2 do IFSP - Jacareí.
* **Fins Educacionais:** O objetivo principal é o aprendizado de arquiteturas de Data Lakehouse e Pipelines de ETL.
* **Dados Fictícios:** Todos os dados de transações e cartões de crédito utilizados são simulados e não correspondem a dados reais de usuários.
* **Uso:** Este projeto não possui fins lucrativos e não deve ser utilizado como uma solução financeira real em produção.
