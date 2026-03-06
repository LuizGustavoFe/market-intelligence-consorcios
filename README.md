# 📊 Market Intelligence: Panorama do Mercado de Consórcios (Bacen)

<img width="1118" height="626" alt="image" src="https://github.com/user-attachments/assets/b35bb123-0f41-4673-88cf-76dfb515da0d" />
<img width="1276" height="715" alt="image" src="https://github.com/user-attachments/assets/1403e63a-396b-474e-9612-24379a6711ac" />
<img width="1277" height="716" alt="image" src="https://github.com/user-attachments/assets/004a57f0-8213-4802-83e3-8fcf242e164d" />
<img width="1278" height="717" alt="image" src="https://github.com/user-attachments/assets/b234da74-37ad-44c6-89d0-976896979551" />
<img width="1277" height="716" alt="image" src="https://github.com/user-attachments/assets/8aeccd9d-379f-44a7-9f06-71e3160499f1" />
<img width="1278" height="716" alt="image" src="https://github.com/user-attachments/assets/e5b0d742-23e7-49ed-85e4-af79b9813d7d" />

## 🎯 Visão Geral do Projeto
Este projeto de **Business Intelligence e Análise de Mercado** foi desenvolvido para fornecer uma visão executiva e aprofundada sobre o mercado de Consórcios no Brasil. Utilizando dados públicos e abertos do Banco Central do Brasil (Bacen), o painel transforma milhares de registros brutos em inteligência competitiva, permitindo análises de *Market Share*, risco (inadimplência), tendências geográficas e sazonalidade das administradoras de consórcio.

A interface foi projetada com foco em **UX/UI (Dark Mode)**, garantindo uma navegação fluida, autoritária e focada na redução da carga cognitiva para a tomada de decisão.

## 📈 Perguntas de Negócio Respondidas
* **Benchmarking:** Quais são as administradoras líderes em volume de vendas e carteira ativa?
* **Risco vs. Retorno:** Quais empresas possuem a melhor relação entre crescimento de vendas e controle de inadimplência?
* **Geointeligência:** Onde o mercado está mais aquecido e qual a representatividade (% Share) de cada Estado?
* **Sazonalidade:** Quais são os meses de maior conversão histórica? Existe uma tendência clara de longo prazo?
* **Análise de Nicho:** Como a dominância de mercado se divide entre os segmentos de Veículos Leves, Imóveis, Pesados e Serviços?

## 🛠️ Arquitetura Técnica e Desafios Solucionados
Este relatório vai muito além de gráficos visuais, utilizando **DAX Avançado** e modelagem dimensional para garantir alta performance e escalabilidade.

### Destaques do DAX & Modelagem:
* **Parâmetros de Campo Dinâmicos (`Field Parameters`):** Criação de seletores dinâmicos que alteram completamente o contexto dos gráficos (eixos, tooltips e formatações numéricas) sem a necessidade de criar dezenas de visuais sobrepostos.
* **Lógica Inversa de Ranking (`RANKX` Condicional):** Desenvolvimento de algoritmo em DAX que identifica a métrica selecionada e inverte a lógica de ranqueamento automaticamente (ex: para Vendas, o maior é o 1º; para Inadimplência ou Taxa de ADM, o menor é o 1º).
* **Inteligência de Tempo (MoM, YoY e Média Móvel):** Cálculos de variação mensal e anual, incluindo o tratamento para ignorar "valores fantasmas" (empresas sem operação no período) e uma Média Móvel de 3 meses para suavizar a curva de tendência histórica.
* **Tratamento de Contexto em Matrizes:** Uso das funções `MAX`, `SWITCH` e `ALL`/`ALLSELECTED` para contornar erros de chave composta nativos do Power BI e travar a posição do *Market Share* mesmo quando filtros específicos são aplicados.

## 🗺️ Estrutura do Painel
O dashboard é composto por 6 visões estratégicas:
1. **Visão Executiva:** Panorama geral e termômetro do mercado.
2. **Market Share & Ranking Dinâmico:** Tabelas e gráficos detalhando o posicionamento dos players, com setas de variação percentual.
3. **Geointeligência:** Mapa de Formas (*Shape Map*) do Brasil, exibindo volume por UF com Tooltips personalizados contendo Share % e evolução Trimestral (QoQ).
4. **Evolução e Sazonalidade:** Gráfico de Área com Média Móvel e Heatmap (Mapa de Calor) evidenciando os piores e melhores meses históricos.
5. **Análise de Segmentos:** Treemap e Gráfico de Faixa demonstrando o fluxo de dominância dos nichos de mercado ao longo do tempo.
6. **Matriz de Benchmarking:** Gráfico de Dispersão mapeando o Risco (Inadimplência) *versus* Tração (Vendas/Cotas Ativas).

## ⚙️ Ferramentas Utilizadas
* **Power BI:** Extração, Limpeza (Power Query), Modelagem (Data Modeling), DAX e Visualização de Dados.
* **Figma:** Prototipação e design de interface (Backgrounds, wireframes e paleta de cores).
* **Banco de Dados:** Dados abertos governamentais estruturados para análise relacional.

---
**Desenvolvido por Luiz Gustavo Federici**
*Analista de Dados & Especialista em Business Intelligence*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/luiz-gustavo-federici/)
