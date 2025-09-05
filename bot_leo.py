from google import genai
from google.genai import types
from api_key import api_key
import time
import re

# Definição de variáveis e regras de negócio
system = genai.Client(api_key = api_key)
chat_history = []
model = "gemini-2.5-flash"
char_limit = 800
roles = """
Você é o GuardaDigital, um assistente virtual especializado em segurança digital para idosos.
Sua missão é detectar, explicar e prevenir golpes, fraudes e tentativas de phishing.

PRINCIPAIS FUNÇÕES:
1. Analisar mensagens suspeitas enviadas pelos usuários
2. Identificar sinais de golpes, fraudes e phishing
3. Educar sobre segurança digital de forma simples e clara
4. Dar dicas preventivas personalizadas para idosos

TIPOS DE GOLPES MAIS COMUNS:
- Phishing: solicitação de dados pessoais via email/mensagem
- Golpe do WhatsApp: falsos parentes pedindo dinheiro
- Falsos investimentos e pirâmides financeiras
- Golpe do boleto falso
- Golpe do cartão clonado
- Falsos técnicos de banco/operadoras
- Golpes em sites de compras falsas
- Golpe do amor (relacionamento falso online)
- Falsos prêmios e promoções

SINAIS DE ALERTA PARA IDENTIFICAR:
- Urgência excessiva ("faça agora ou perderá")
- Solicitação de dados pessoais, senhas ou códigos
- Links suspeitos ou URLs estranhas
- Erros de português ou formatação ruim
- Ofertas impossíveis ("ganhe muito dinheiro fácil")
- Pressão emocional ou ameaças
- Pedidos de transferência de dinheiro para desconhecidos
- Mensagens de pessoas se passando por conhecidos

DIRETRIZES DE RESPOSTA:
- Use linguagem simples, carinhosa e respeitosa
- Explique de forma didática, como se estivesse conversando com seus avós
- Sempre forneça o nível de risco: BAIXO, MÉDIO, ALTO ou CRÍTICO
- Dê dicas práticas de como proceder
- Inclua orientações preventivas
- Se não for relacionado à segurança digital, responda: "Sou especialista em segurança digital. Como posso ajudar com golpes, fraudes ou mensagens suspeitas?"

FORMATO DA ANÁLISE:
🚨 NÍVEL DE RISCO: [BAIXO/MÉDIO/ALTO/CRÍTICO]
📝 ANÁLISE: [explicação detalhada]
⚠️ SINAIS DE ALERTA: [pontos específicos identificados]
✅ RECOMENDAÇÕES: [o que fazer]
🛡️ PREVENÇÃO: [dicas para evitar golpes similares]
"""

# Palavras-chave que indicam possíveis golpes
FRAUD_KEYWORDS = [
    # Phishing e dados pessoais
    'cpf', 'senha', 'cartão', 'dados pessoais', 'confirme seus dados', 'atualize cadastro',
    'código de segurança', 'token', 'chave pix', 'número do cartão', 'cvv',
    
    # Urgência e pressão
    'urgente', 'imediatamente', 'prazo', 'expire', 'suspenso', 'bloqueado', 'cancelado',
    'últimas horas', 'oferta limitada', 'apenas hoje',
    
    # Golpes financeiros
    'transferir dinheiro', 'depósito', 'investimento garantido', 'lucro fácil', 'ganhe dinheiro',
    'empréstimo aprovado', 'prêmio', 'você ganhou', 'sortudo', 'milionário',
    
    # Golpes comuns
    'whatsapp clonado', 'novo número', 'celular quebrou', 'preciso de ajuda', 'emergência',
    'clique no link', 'baixe o aplicativo', 'instale agora', 'acesse o site'
]

def detect_fraud_keywords(message):
    """Detecta palavras-chave suspeitas na mensagem"""
    message_lower = message.lower()
    found_keywords = []
    
    for keyword in FRAUD_KEYWORDS:
        if keyword in message_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def analyze_message_structure(message):
    """Analisa a estrutura da mensagem para sinais suspeitos"""
    suspicious_patterns = []
    
    # URLs suspeitas
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    if re.search(url_pattern, message):
        suspicious_patterns.append("Contém links/URLs")
    
    # Muitos números (possível tentativa de obter dados)
    if len(re.findall(r'\d+', message)) > 3:
        suspicious_patterns.append("Muitos números mencionados")
    
    # Excesso de maiúsculas (pressão)
    if len(re.findall(r'[A-Z]', message)) > len(message) * 0.3:
        suspicious_patterns.append("Excesso de letras maiúsculas")
    
    # Múltiplos pontos de exclamação
    if message.count('!') > 2:
        suspicious_patterns.append("Excesso de pontos de exclamação")
    
    return suspicious_patterns

def bot_response(user_message):
    # Verifica se é uma pergunta sobre segurança digital
    classification = system.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(
            system_instruction = roles),
        contents= f"A pergunta se refere a segurança digital, golpes, fraudes, mensagens suspeitas ou análise de possível golpe? Responda apenas com 'sim' ou 'não'. Pergunta: {user_message}"
    )
    
    classification_text = classification.text.lower()
    
    if "não" in classification_text:
        return "Olá! Sou o GuardaDigital, especialista em segurança digital para idosos. Como posso ajudar com golpes, fraudes ou análise de mensagens suspeitas? 🛡️"

    # Análise prévia da mensagem
    fraud_keywords = detect_fraud_keywords(user_message)
    suspicious_patterns = analyze_message_structure(user_message)
    
    # Prepara contexto adicional para a IA
    analysis_context = ""
    if fraud_keywords:
        analysis_context += f"\nPalavras-chave suspeitas encontradas: {', '.join(fraud_keywords)}"
    if suspicious_patterns:
        analysis_context += f"\nPadrões suspeitos identificados: {', '.join(suspicious_patterns)}"

    # Código principal com contexto de análise
    chat_history.append("Usuário: " + user_message + analysis_context)

    response = system.models.generate_content(
        model= model,
        config = types.GenerateContentConfig(
            system_instruction = roles,
            thinking_config = types.ThinkingConfig(thinking_budget=0),
            max_output_tokens = char_limit
        ),
        contents = chat_history
    )

    bot_text = response.text
    chat_history.append("Assistente: " + bot_text)
    
    # Quando o usuário faz 3 perguntas, a conversa é resumida
    if len(chat_history) >= 6:
        time.sleep(1)
        summary = summarize(chat_history)
        chat_history.clear()
        return bot_text + "\n\n📋 Resumo da conversa: " + summary
    else:
        return bot_text


def summarize(messages_list):
    conversation = "\n".join(messages_list)
    summary = system.models.generate_content(
        model=model,
        contents=f"Resuma esta conversa sobre segurança digital e detecção de golpes em até {char_limit} caracteres, destacando os principais riscos identificados e dicas dadas:\n\n{conversation}"
    )
    return summary.text

# Função adicional para análise rápida de mensagens suspeitas
def quick_fraud_check(message):
    """Análise rápida para mensagens muito suspeitas"""
    high_risk_phrases = [
        'confirme seus dados', 'atualize seu cadastro', 'clique no link', 
        'sua conta será bloqueada', 'você ganhou', 'transferir dinheiro',
        'código de verificação', 'novo whatsapp', 'celular quebrou'
    ]
    
    message_lower = message.lower()
    for phrase in high_risk_phrases:
        if phrase in message_lower:
            return True
    return False