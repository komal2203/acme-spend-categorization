# 🧾 ACME Spend Categorization

An intelligent spend categorization system that automatically classifies invoice data using a hybrid of rule-based and AI-powered techniques, built for scalability, accuracy, and user-friendly oversight.

---

## 🚀 Overview

This system processes invoice-level data to categorize spend items according to the [UNSPSC](https://www.unspsc.org/) (United Nations Standard Products and Services Code) taxonomy. It uses a hybrid pipeline that combines:

- 🧠 **AI-Powered Categorization** using OpenAI GPT models  
- 🛠️ **Rule-Based Classification** for deterministic tagging  
- 👀 **Manual Review Interface** for edge cases and quality assurance  

---

## ✨ Key Features

- ✅ **Automatic Categorization**: Categorize thousands of line items at scale  
- ⚖️ **Hybrid Classification**: Leverages both deterministic rules and probabilistic AI  
- 📈 **Confidence Scoring**: Track classification certainty with every result  
- 🧑‍💼 **Manual Review**: Built-in UI for validating uncertain predictions  
- 📊 **Data Visualization**: Interactive spend analytics (coming soon)  
- 📤 **Export Capability**: Download categorized and reviewed data in CSV format  
- 🧠 **Taxonomy-Aware Embeddings**: Uses semantic similarity against the UNSPSC hierarchy  
- 🔁 **Daily Taxonomy Sync**: Refreshes UNSPSC data every 24 hours automatically  

---

## ⚙️ Prerequisites

   - Python 3.9+
   - [OpenAI API Key](https://platform.openai.com/account/api-keys)

---

<!--
## 📦 Installation


1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/acme-spend-categorization.git
   cd acme-spend-categorization
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # OR for Windows
   venv\Scripts\activate
   pip install -r requirements.txt
   python src/08_pipeline.py
   ```
   OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


---

## 🧪 Usage

1. **Run Full Pipeline** - Processes invoices and writes outputs

   ```bash
   python src/08_pipeline.py
   ```

   ---

2. **Outputs**

   - **data/categorized.csv**: High-confidence auto-tagged items  
   - **`data/manual_review.csv`**: Items requiring human validation  
   - **`logs/pipeline.log`**: Detailed logging of categorization events  


---
-->

## 📁 Data Format

Prepare your invoice CSV like this:

| invoice_id | sku   | description               | supplier       | amount |
|------------|-------|---------------------------|----------------|--------|
| INV-001    | 10001 | Black toner cartridge     | OfficeSupplyCo | 89.99  |
| INV-002    | 20003 | Fiber optic cables, 50ft  | NetGear Inc.   | 129.50 |

**Required columns**: `description`, `supplier`, `sku`, `invoice_id`

---

## 🌐 Web UI (Optional)
   - To run a lightweight Flask interface:

     ````bash
     python app.py
     ````
   - Then navigate to http://localhost:5000 (Flask).

---

## 🧠 How It Works
   - Sanitization: Cleans and normalizes invoice text
   - Rule Matching: Applies analyst-defined keyword rules
   - Semantic Retrieval: Finds top UNSPSC candidates via embedding similarity
   - AI Selection: GPT-4 picks the most likely UNSPSC code
   - Confidence Routing: Items below threshold are queued for manual review

---

## Performance & Monitoring
   - Multi-core parallel processing via multiprocessing
   - Confidence-based classification routing
   - Logs available in logs/pipeline.log

---


## 📅 Roadmap
   - More robust rule engine (regex, entity recognition)
   - Spend analytics dashboard
   - RESTful API endpoints for integration
   - Scheduled batch job manager
   - Mobile-friendly UI

---

## 🤝 Collaborators
   - Subhav Jain
   - Sidhant Budhiraja
   - Komal Meena
   - Prayash Pandey

---

## 📚 Acknowledgments
   - OpenAI for powerful AI APIs
   - UNSPSC.org for the classification taxonomy
   - Sentence-Transformers for semantic search


