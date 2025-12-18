# 🎧 Microserviço de Acessibilidade e Conversão de Mídia (OCR & TTS)

> **Disciplina:** Reuso de Software  
> **Trabalho:** 2 - Desenvolvimento de Serviço Reutilizável  
> **Opção Escolhida:** A (Serviço Reutilizável com Resiliência)

## 📄 Descrição do Projeto

Este projeto consiste em um **Microserviço de Acessibilidade** projetado para ser reutilizado por diversas aplicações (chatbots, apps mobile, sites educacionais). Ele atua como um *Gateway* de conversão de mídia, oferecendo duas capacidades principais:

1.  **OCR (Optical Character Recognition):** Extração de texto a partir de imagens.
2.  **TTS (Text-to-Speech):** Conversão de texto em áudio falado (MP3).

O diferencial deste serviço é a implementação manual de **Padrões Arquiteturais de Resiliência**, garantindo que o sistema suporte falhas de dependências externas e picos de acesso sem degradar completamente.

---

## 🛡️ Padrões de Resiliência Aplicados

Para garantir robustez e alta disponibilidade, foram implementados os seguintes padrões (sem uso de bibliotecas externas de circuit breaker):

* **Circuit Breaker (Disjuntor):** Protege o serviço contra falhas na API de voz (Google TTS). Se o serviço externo falhar 3 vezes consecutivas, o circuito abre e rejeita novas requisições imediatamente por 30 segundos, evitando efeito cascata.
* **Retry Pattern (Tentativa):** Em caso de falha de conexão, o sistema tenta reconectar até 3 vezes antes de desistir.
* **Bulkhead (Antepara):** Limita o número de processamentos de imagem simultâneos (OCR) usando um Semáforo. Isso impede que o processamento pesado de imagens consuma 100% da CPU e trave as rotas de áudio.

---

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Framework API:** FastAPI (Alta performance e assíncrono)
* **Servidor:** Uvicorn (ASGI)
* **OCR Engine:** Tesseract OCR (via `pytesseract`)
* **TTS Engine:** Google Text-to-Speech (`gTTS`)
* **Processamento de Imagem:** Pillow (PIL)

