# NetPulse

Monitor leve de disponibilidade e latência para pequenos ambientes de rede. O projeto executa verificações TCP em hosts configurados, registra o histórico em CSV e gera um painel HTML com indicadores de disponibilidade, latência média e incidentes recentes.

> Projeto de portfólio desenvolvido para praticar automação, fundamentos de redes, observabilidade e tratamento de incidentes.

## O que o projeto demonstra

- Verificação de conectividade TCP em portas configuráveis
- Medição de latência e classificação dos resultados
- Registro de histórico em CSV
- Geração de relatório HTML sem dependências externas
- Modo de demonstração para testar o fluxo sem depender de uma rede específica
- Testes automatizados para as regras de classificação e agregação

## Demonstração

O diretório `docs` contém um painel gerado com dados fictícios. Ele pode ser publicado no GitHub Pages sem executar verificações reais contra serviços externos.

## Arquitetura

```text
hosts.json -> checker -> CSV histórico -> agregador -> dashboard HTML
```

## Como executar

Requisitos: Python 3.10 ou superior.

```bash
python netpulse.py --config hosts.example.json --output data/checks.csv --report dashboard.html
```

Para executar com dados simulados:

```bash
python netpulse.py --config hosts.example.json --output data/demo.csv --report dashboard.html --demo
```

Abra `dashboard.html` no navegador após a execução.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Conceitos aplicados

TCP/IP, portas, disponibilidade, latência, timeout, registro de eventos, indicadores operacionais e automação com Python.

## Próximos passos

- Execução periódica por agendador
- Alertas por e-mail ou webhook
- Persistência em banco de dados
- Exportação de métricas para Grafana ou Prometheus

## Uso responsável

Execute verificações apenas em equipamentos e serviços para os quais você tenha autorização.
