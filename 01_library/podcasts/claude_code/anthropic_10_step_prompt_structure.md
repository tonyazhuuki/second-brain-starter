# 🏗️ 10-шаговая структура промпта от Anthropic

> Источник: [Prompting 101 | Code w/ Claude](prompting_101.md)

## 📋 **Обзор структуры**

Anthropic рекомендует следующую последовательность для построения эффективных промптов:

1. **Task Context** — контекст задачи
2. **Tone Context** — тональный контекст  
3. **Background Detail** — фоновая информация
4. **Examples** — примеры (few-shot)
5. **Conversation History** — история диалога
6. **Content** — динамический контент
7. **Detailed Instructions** — детальные инструкции
8. **Task Reminder** — напоминание о задаче
9. **Output Formatting** — форматирование вывода
10. **Guidelines/Reinforcement** — финальные принципы

---

## 🔍 **Подробная разбивка каждого шага**

### **1. Task Context (Контекст задачи)**
**Что делает:** Четко определяет роль Claude и основную задачу

**Пример:**
```
You are an AI assistant helping a claims adjuster review car accident report forms in Swedish.
```

**Почему важно:** 
- Без контекста Claude может неправильно интерпретировать данные
- В демо без контекста Claude решил, что это "лыжная авария"
- Задает рамки для всего последующего анализа

---

### **2. Tone Context (Тональный контекст)**
**Что делает:** Устанавливает стиль общения и требования к уверенности

**Пример:**
```
Stay factual and confident. If you can't understand something clearly, don't guess or mislead us.
```

**Почему важно:**
- Предотвращает галлюцинации
- Контролирует уровень уверенности в ответах
- Устанавливает профессиональный тон для бизнес-задач

---

### **3. Background Detail/Documents/Images (Фоновая информация)**
**Что делает:** Предоставляет статическую информацию, не меняющуюся между запросами

**Пример:**
```xml
<form_structure>
This is a Swedish car accident form with:
- Title: "Skadeanmälan"
- Two columns representing Vehicle A and Vehicle B
- 17 numbered rows, each representing different actions:
  1. Parked/stopped
  2. Leaving parking space
  3. Entering parking space
  [... etc for all 17 rows]
</form_structure>
```

**Где размещать:** В system prompt для переиспользования

**Преимущества:**
- Claude тратит меньше времени на понимание структуры
- Идеально для prompt caching
- Повышает точность анализа

---

### **4. Examples (Примеры)**
**Что делает:** Few-shot примеры сложных случаев с правильными решениями

**Формат:**
```xml
<example>
<input>
[Изображение формы с конкретными отметками]
</input>
<output>
Based on the form analysis:
- Vehicle A: Box 7 checked (turning left)  
- Vehicle B: Box 12 checked (going straight)
- Verdict: Vehicle A at fault for improper left turn
</output>
</example>
```

**Когда использовать:**
- Для граничных случаев
- Когда нужна человеческая экспертиза
- Для консистентности в сложных решениях

---

### **5. Conversation History (История диалога)**
**Что делает:** Включает релевантный контекст из предыдущих взаимодействий

**Когда нужно:**
- User-facing приложения с длинными диалогами
- Когда контекст предыдущих сообщений влияет на текущий анализ

**В кейсе со страховой:** Не использовался, так как это background-система

---

### **6. Content (Контент)**
**Что делает:** Динамические данные для анализа

**Особенности:**
- Единственная часть, которая меняется между запросами
- В примере: изображения формы ДТП и эскиза аварии
- Может включать файлы, изображения, тексты

---

### **7. Detailed Instructions (Детальные инструкции)**
**Что делает:** Пошаговый алгоритм выполнения задачи

**Ключевой принцип:** Порядок анализа критичен

**Пример структуры:**
```
1. First, carefully examine the accident report form
   - Look at each checkbox methodically
   - Note which boxes are clearly marked for Vehicle A and Vehicle B
   - Create a list of what you observe

2. Then, analyze the hand-drawn sketch
   - Use your understanding from the form to interpret the drawing
   - Look for consistency between form data and sketch
   - Note any additional details the sketch provides

3. Make your final assessment
   - Only if you're confident in your analysis
   - Reference specific form data to support your conclusion
```

**Почему порядок важен:**
- Человек тоже не стал бы сначала смотреть непонятный эскиз
- Сначала факты (форма), потом интерпретация (эскиз)
- Логическое построение рассуждений

---

### **8. Task Reminder (Напоминание о задаче)**
**Что делает:** Повторяет ключевые требования и ограничения

**Цель:** Предотвращение дрейфа от задачи и галлюцинаций

**Пример:**
```
Remember:
- Answer only if very confident
- Refer back to specific form data when making factual claims
- If the sketch is unintelligible, say so rather than guess
```

---

### **9. Output Formatting (Форматирование вывода)**
**Что делает:** Структурирует результат для легкой интеграции

**Инструменты:**
- **XML-теги:** `<final_verdict>Vehicle B at fault</final_verdict>`
- **JSON:** Для программной обработки
- **Prefill:** Подсказка начала ответа

**Цель:** 
- Легкое извлечение ключевых данных
- Интеграция с базами данных
- Автоматизация процессов

---

### **10. Guidelines/Reinforcement (Финальные принципы)**
**Что делает:** Последнее усиление важных правил

**Пример:**
```
Important guidelines:
- Keep summary clear, concise, and accurate
- Don't invent details not found in the provided data
- Wrap your final determination in the specified XML tags
```

**Цель:** Финальная "подстраховка" от нежелательного поведения

---

## 🎯 **Ключевые принципы применения**

### **Итеративность**
- Тестируй промпт → анализируй ошибки → улучшай → повторяй
- В демо: от "лыжной аварии" к точному определению вины через итерации

### **Структурированность** 
- Claude "любит структуру и организацию"
- XML-теги помогают понимать назначение каждой части
- Markdown тоже работает, но XML точнее

### **Логический порядок**
- Как человек анализирует информацию пошагово
- От простого к сложному, от фактов к интерпретации

---

## 🚀 **Продвинутые техники**

### **Prefill (Предзаполнение)**
```
Human: [ваш промпт]
```


