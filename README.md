# Dashboard de Umidade do Solo - Flet

Este projeto cria um dashboard para monitoramento de umidade do solo usando a lib Flet para a interface gráfica, Plotly para visualização dos dados e uma conexão serial com um Arduino para ler os dados dos sensores de umidade.

## Requisitos

Antes de rodar o projeto, certifique-se de que você possui os seguintes itens instalados:

- Python 3.8 ou superior
- Bibliotecas Python necessárias:
  - Flet: `flet`
  - Plotly: `plotly`
  - PySerial: `pyserial`
 
- Você também precisa de um arduino e 3 sensores de umidade

## Instalação

1. Clone este repositório ou faça o download do código.
2. Crie um ambiente virtual e entre nele

   ```sh
   python -m venv venv
   # No Linux/macOS
   source venv/bin/activate
   
   # No Windows
   venv\Scripts\activate
   ```

3. Instale as bibliotecas necessárias:

   ```sh
   pip install flet plotly pyserial
   ```

## Conexão com Arduino

Certifique-se de que o Arduino esteja conectado à porta correta do computador. No código, a porta está configurada como `/dev/ttyUSB0`. Caso esteja utilizando Windows, você pode precisar mudar para algo como `COM3` ou `COM4`, dependendo da porta utilizada.

### Alterar a Porta Serial:

No arquivo principal, altere a linha a seguir, caso necessário:

```python
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
```

Substitua `/dev/ttyUSB0` pela porta serial correta do seu sistema.

## Executando o Projeto

Para rodar o dashboard, execute o arquivo principal do projeto:

```sh
python app.py
```

O dashboard será aberto no navegador padrão, apresentando as leituras de umidade em tempo real dos sensores conectados ao Arduino.

## Estrutura do Código

- **Flet**: Utilizado para criar a interface do dashboard.
- **Plotly**: Criação dos gráficos que mostram a umidade ao longo do tempo.
- **PySerial**: Utilizado para estabelecer a comunicação com o Arduino e coletar as leituras dos sensores.

O dashboard exibe os valores de umidade dos três tipos de solo: Arenoso, Argiloso e Orgânico. Cada tipo de solo possui um gráfico que é atualizado em tempo real com as últimas 30 leituras feitas pelos sensores.

## Problemas Comuns

1. **Erro na Conexão Serial**: Verifique se a porta correta está configurada e se o Arduino está conectado corretamente.
2. **Bibliotecas Não Instaladas**: Certifique-se de ter instalado todas as bibliotecas necessárias executando `pip install flet plotly pyserial`.
3. **Conexão do Arduino**: Se os valores lidos não estiverem corretos, verifique a ligação dos sensores ao Arduino e se estão corretamente calibrados.

