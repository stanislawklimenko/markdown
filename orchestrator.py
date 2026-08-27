def process_ticket(raw_text):
    # 1. Анонимизация
    text_clean = pii_anonymizer.anonymize(raw_text)
    
    # 2. Классификация
    intent, entities = classifier.predict(text_clean)
    
    # 3. RAG
    docs = rag_retriever.retrieve(intent, entities, text_clean)
    
    # 4. Генерация (если интент разрешён для авто)
    if intent in AUTO_ALLOWED:
        draft = llm_generator.generate(text_clean, intent, entities, docs)
    else:
        draft = None
    
    # 5. Шлюз уверенности
    confidence = confidence_gate.evaluate(draft, docs) if draft else 0.0
    
    # 6. Решение
    if confidence > 0.92 and intent in AUTO_ALLOWED:
        status = "AUTO_CLOSED"
        final_response = draft
    else:
        status = "ESCALATED"
        final_response = None  # для агента
    
    log_ticket(raw_text, intent, confidence, status)
    return status, final_response

# Пример вызова
result = process_ticket("Не могу войти, забыл пароль. email: user@example.com")
print(result)  # ('AUTO_CLOSED', 'Инструкция по сбросу пароля...')
