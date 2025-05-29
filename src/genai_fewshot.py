# System prompt for OpenRouter
SYSTEM = "You are a spend-categorization expert."

# Few-shot examples using natural language to simulate function calls
FEW_SHOT = [
    {
        "role": "user",
        "content": 'Invoice line: "Printer toner, black" supplier:"OfficeSupplyCo"'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="14101500", confidence=0.97)'
    },
    {
        "role": "user",
        "content": 'Invoice line: "Catering service for staff meeting" supplier:"DeliciousCatering"'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="90101600", confidence=0.93)'
    },
    {
        "role": "user",
        "content": 'Invoice line: "MacBook Pro 14 inch, 16GB RAM" supplier:"TechWorld"'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="43211503", confidence=0.95)'
    },
    {
        "role": "user",
        "content": 'Invoice line: "Travel reimbursement for business trip" supplier:"CompanyX"'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="90101609", confidence=0.92)'
    },
    {
        "role": "user",
        "content": 'Invoice line: "Monthly subscription to Adobe Creative Cloud" supplier:"Adobe"'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="43232100", confidence=0.96)'
    }
]
