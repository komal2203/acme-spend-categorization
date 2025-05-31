# System prompt for OpenRouter
SYSTEM = (
    "You are a spend-categorization expert. "
    "Given an invoice line and supplier, your task is to assign the most appropriate 8-digit UNSPSC code "
    "from the provided options. Respond ONLY by calling the classify_invoice_line function, "
    "with a valid 8-digit code and a confidence score between 0 and 1. "
    "Do not invent codes. If unsure, pick the closest match from the options."
)

# Few-shot examples using natural language to simulate function calls
FEW_SHOT = [
    {
        "role": "user",
        "content": 'Invoice: "Printer toner, black"\nSupplier: "OfficeSupplyCo"\nOptions:\n1. 14101500 – Toner cartridges\n2. 14101600 – Ink cartridges'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="14101500", confidence=0.97)'
    },
    {
        "role": "user",
        "content": 'Invoice: "Catering service for staff meeting"\nSupplier: "DeliciousCatering"\nOptions:\n1. 90101600 – Food catering services\n2. 90101700 – Beverage catering services'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="90101600", confidence=0.93)'
    },
    {
        "role": "user",
        "content": 'Invoice: "MacBook Pro 14 inch, 16GB RAM"\nSupplier: "TechWorld"\nOptions:\n1. 43211503 – Laptop computers\n2. 43211700 – Computer monitors'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="43211503", confidence=0.95)'
    },
    {
        "role": "user",
        "content": 'Invoice: "Travel reimbursement for business trip"\nSupplier: "CompanyX"\nOptions:\n1. 90101609 – Travel management services\n2. 93141500 – Expense reimbursement services'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="90101609", confidence=0.92)'
    },
    {
        "role": "user",
        "content": 'Invoice: "Monthly subscription to Adobe Creative Cloud"\nSupplier: "Adobe"\nOptions:\n1. 43232100 – Software subscriptions\n2. 43232400 – Graphic software'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="43232100", confidence=0.96)'
    }
]