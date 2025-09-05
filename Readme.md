# 🛡️ GuardaDigital - Detector de Golpes e Fraudes
## Sistema de Segurança Digital para Idosos: Prevenção de Golpes e Fraudes

Este projeto cria um chatbot especializado em detectar e prevenir golpes digitais, com foco na proteção de idosos contra fraudes online. Integrado com a IA do Gemini, oferece análise inteligente de mensagens suspeitas e educação sobre segurança digital.

## 🎯 Principais Funcionalidades

### 🔍 Detecção Inteligente
- **Análise de Phishing**: Identifica tentativas de roubo de dados pessoais
- **Detecção de Palavras-chave**: Reconhece termos suspeitos automaticamente
- **Análise de Padrões**: Avalia estrutura de mensagens para sinais de alerta
- **Classificação de Risco**: Níveis BAIXO, MÉDIO, ALTO e CRÍTICO

### � Tipos de Golpes Detectados
- Phishing (solicitação de dados pessoais)
- Golpe do WhatsApp (falsos parentes)
- Investimentos fraudulentos
- Boletos falsos
- Cartão clonado
- Falsos técnicos de banco
- Sites de compras falsas
- Golpe do amor
- Prêmios falsos

### 📱 Interface Amigável
- Design pensado para idosos
- Cores diferenciadas para mensagens de risco
- Instruções claras e didáticas
- Análise em tempo real

## 🛠️ Como Usar

### Exemplos Práticos:
```
"Isso é golpe? Me passe seu e-mail para confirmar a compra"
"É seguro? Seu cartão foi clonado, confirme seus dados no link"
"Recebo uma mensagem: Olá mãe, quebrei o celular, esse é meu novo número"
```

### Tipos de Pergunta:
- **Análise**: "Isso é golpe? [cola a mensagem]"
- **Educação**: "Como identificar phishing?"
- **Prevenção**: "Como me proteger de golpes no WhatsApp?"
- **Dúvidas**: "O que fazer se cair em um golpe?"

## 📋 Resposta Estruturada
O GuardaDigital sempre responde no formato:
- 🚨 **NÍVEL DE RISCO**: Classificação do perigo
- 📝 **ANÁLISE**: Explicação detalhada
- ⚠️ **SINAIS DE ALERTA**: Pontos específicos identificados
- ✅ **RECOMENDAÇÕES**: O que fazer
- 🛡️ **PREVENÇÃO**: Dicas para evitar golpes similares

## 📜 Regras de Uso
- O sistema usa a versão gratuita da API do Gemini
- Pode haver inconsistências se o serviço estiver fora do ar
- A API tem limite de requisições por minuto
- Aguarde alguns segundos entre perguntas se necessário
- Após 3 perguntas, será gerado um resumo automático

## 💻 Instalação

1. **Baixe o projeto**
2. **Verifique o Python**:
   ```bash
   python --version
   ```
3. **Instale a biblioteca**:
   ```bash
   pip install google-genai
   ```
4. **Configure a API**:
   - Obtenha uma chave no [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Insira a chave no arquivo `api_key.py`

5. **Execute o programa**:
   ```bash
   python user_screen.py
   ```

## 🎥 Demonstração
[▶️ Vídeo mostrando detecção de golpes em ação]()

## 🔒 Segurança e Privacidade
- Não armazena dados pessoais permanentemente
- Análise local das mensagens
- Educação focada na prevenção
- Respostas didáticas e respeitosas

---


**Missão**: Proteger idosos contra golpes digitais através de tecnologia acessível e educação preventiva. 🛡️
