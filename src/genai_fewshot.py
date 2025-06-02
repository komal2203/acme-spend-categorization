# System prompt for OpenRouter
SYSTEM = (
    "You are an expert in UNSPSC spend categorization. "
    "Assign the most appropriate 8-digit UNSPSC code to each invoice line, using only the provided options. "
    "Read the invoice description and supplier name. For each option, analyze the code and title for the best match, considering keywords, product types, and context. "
    "If the supplier is known for a category, use that as a clue. Eliminate options that clearly do not match. "
    "If multiple options are plausible, choose the most specific and relevant. If uncertain, select the closest match from the options—never invent or guess codes. "
    "Respond ONLY by calling the classify_invoice_line function with a valid 8-digit code from the options and a confidence score (0 to 1). "
    "Do not provide explanations, extra text, or codes not present in the options."
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
        "content": 'Invoice: "HP LaserJet Pro M404dn printer"\nSupplier: "TechMart"\nOptions:\n1. 43212105 – Laser printers\n2. 43212100 – Printers'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="43212105", confidence=0.95)'
    },
    {
        "role": "user",
        "content": 'Invoice: "Staples for office use"\nSupplier: "OfficeDepot"\nOptions:\n1. 44122108 – Staples\n2. 44122100 – Fasteners'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="44122108", confidence=0.93)'
    },
    {
        "role": "user",
        "content": 'Invoice: "Cloud storage subscription"\nSupplier: "Dropbox"\nOptions:\n1. 43233405 – Cloud storage services\n2. 43231513 – Database software'
    },
    {
        "role": "assistant",
        "content": 'Calling classify_invoice_line(code="43233405", confidence=0.96)'
    }
]