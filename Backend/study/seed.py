from study.models import Deck, Card

deck, _ = Deck.objects.get_or_create(name="PL-300 DAX")

cards_data = [
    {
        "question": "What does CALCULATE do in DAX?",
        "answer": "Evaluates an expression in a modified filter context.",
        "explanation": "It changes filter context before evaluating."
    },
    {
        "question": "What is a measure in Power BI?",
        "answer": "A calculation used in data analysis, created using DAX.",
        "explanation": "Measures are dynamic and respond to filters."
    },
    {
        "question": "Difference between calculated column and measure?",
        "answer": "Column is static, measure is dynamic.",
        "explanation": "Columns are computed row by row, measures at query time."
    },
    {
        "question": "What is filter context?",
        "answer": "The set of filters applied to data before evaluation.",
        "explanation": "Determines which data is visible to calculations."
    },
    {
        "question": "What does SUMX do?",
        "answer": "Iterates over a table and sums an expression.",
        "explanation": "Row-by-row evaluation."
    },
]

for card in cards_data:
    Card.objects.create(
        deck=deck,
        question=card["question"],
        answer=card["answer"],
        explanation=card["explanation"]
    )

print("Data loaded.")