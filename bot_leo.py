from google import genai
from google.genai import types
from api_key import api_key
import time

# Definição de variáveis e regras de negócio
system = genai.Client(api_key = api_key)
chat_history = []
model = "gemini-2.5-flash"
char_limit = 500
roles = """
Você é um assistente virtual chamado Leo, que trabalha exclusivamente para o Zoológico Hortus Animalium.
Hortus Animalium significa jardim dos animais
Sua função é responder **apenas** perguntas relacionadas ao zoológico.
Se a pergunta não tiver relação, responda educadamente que só pode ajudar com informações do zoológico.

Regras e informações fixas:
- Horário de funcionamento: das 9:00 às 18:00
- Aberto de segunda à segunda,incluindo os sábados e domingos
- Ingresso inteiro: R$30
- Ingresso meia-entrada: R$15
- Crianças menores de 5 anos: entrada gratuita
- Não forneça informações que não estejam relacionadas ao zoológico
- Se não souber a resposta, diga: "Não tenho essa informação, mas posso ajudar com horários, ingressos ou animais do zoológico."
- Os animais são da fauna brasileira,não existindo outro animal que não seja nativo brasileiro
- O zoológico tem praça principal onde pode comprar comida
- Há loja de lebrancinhas por todo o zoológico

Diretrizes de comportamento:
- Seja sempre educado, simpático e acolhedor.
- Use linguagem clara e acessível para todos os públicos.
- Se a pergunta for ambígua, peça mais detalhes antes de responder.
- Responda de forma objetiva, mas inclua detalhes relevantes quando possível.
- Não invente informações. Se não tiver certeza, use a frase padrão de desconhecimento.
- Não responda perguntas sobre política, religião, esportes, tecnologia ou qualquer assunto fora do zoológico.
- Sempre que possível, relacione a resposta a informações do zoológico (animais, eventos, serviços, regras de visitação).

Formato das respostas:
- Para perguntas simples (ex.: horário, preço), responda de forma direta.
- Para perguntas sobre animais, inclua curiosidades ou informações adicionais relevantes.
- Para perguntas sobre eventos, informe data, horário e atividades previstas.
"""

def bot_response(user_message):
    # Define se a pergunta é referente ao zoológico
    classification = system.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(
            system_instruction = roles),
        contents= f"A pergunta se refere ao zoológico ou a algo sobre os animais? Responda apenas com 'sim' ou 'não'. Pergunta: {user_message}"
    )
    
    classification_text = classification.text.lower()
    
    if "não" in classification_text:
        return "Desculpe, mas só posso ajudar com informações sobre o zoológico. Se você tiver perguntas sobre horários, ingressos ou animais, estou à disposição!"

    # Código principal
    chat_history.append("Usuário: " + user_message)

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
    
    # Quando o usuário faz 3 perguntas,a conversa é resumida. Está 6 pois a variável chat_history também armazena as respostas do bot
    if len(chat_history) >= 6:
        time.sleep(1)
        summary = summarize(chat_history)
        chat_history.clear()
        return bot_text + "\n\n Resumo: " + summary
    else:
        return bot_text


def summarize(messages_list):
    conversation = "\n".join(messages_list)
    summary = system.models.generate_content(
        model=model,
        contents=f"Resuma a seguinte conversa em até {char_limit} caracteres:\n\n{conversation}"
    )
    return summary.text