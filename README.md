# 🧾 ACME Spend Categorization

An advanced, intelligent spend categorization system designed to automatically classify invoice-level procurement data using a hybrid approach that combines both rule-based logic and AI-driven semantic understanding. The system is architected to be scalable, accurate, and human-in-the-loop friendly, enabling organizations to process large volumes of invoice descriptions while maintaining control, auditability, and transparency over categorization decisions.

---

## 🚀 Overview

This system processes invoice-level data to categorize spend items according to the [UNSPSC](https://www.unspsc.org/) (United Nations Standard Products and Services Code) taxonomy. It uses a hybrid pipeline that combines:

- **AI-Powered Categorization** using OpenAI GPT models  
- **Rule-Based Classification** for deterministic tagging  
- **Manual Review Interface** for edge cases and quality assurance  

---

## ✨ Key Features

- **Automatic Categorization**: Categorize thousands of line items at scale  
- **Hybrid Classification**: Leverages both deterministic rules and probabilistic AI  
- **Confidence Scoring**: Track classification certainty with every result  
- **Manual Review**: Built-in UI for validating uncertain predictions.  
- **Data Visualization**: Interactive spend analytics and can be downloaded as well for detailed analysis. 
- **Export Capability**: Download categorized and reviewed data in CSV format  
- **Taxonomy-Aware Embeddings**: Uses semantic similarity against the UNSPSC hierarchy  
- **Daily Taxonomy Sync**: Refreshes UNSPSC data every 3 months automatically
- **Real-time Search**: Instant search across categorized items
- **Learning System**: Use feedback to improve future classifications
- **Feedback History**: Maintain audit trail of all corrections
- **Continuous Improvement**: Regular prompt updates based on feedback

---

### 📊 Enhanced Performance Metrics
- **Detailed Analytics Dashboard**:
  - Confidence distribution analysis
  - Category-wise performance metrics
  - Source distribution (Rule-based vs AI-based)
- **Downloadable Reports**:
  - Export metrics as CSV

---

### 🎯 Prompt Optimization
- **Dynamic Prompt Engineering**: Automatically optimize prompts based on performance
- **Context-Aware Prompts**: Adapt prompts based on item category
- **Continuous Improvement**: Regular prompt updates based on feedback

---

### 📈 Performance Visualization
- **Interactive Charts**:
  - Category distribution bar graphs
  - Supplier amount distribution
  - Confidence score pie charts
  - Source distribution analysis
- **Downloadable Visualizations**:
  - Export charts as PNG
  - Save metrics as CSV
  - Generate comprehensive reports
 
---

## 📁 Data Format

Prepare your invoice CSV like this:

| Invoice ID | SKU   | Description               | Supplier       | Amount |
|------------|-------|---------------------------|----------------|--------|
|     001    | 10001 | Black toner cartridge     | OfficeSupplyCo | 89.99  |
|     002    | 20003 | Fiber optic cables, 50ft  | NetGear Inc.   | 129.50 |

**Required columns**: `description`, `supplier`, `sku`, `invoice_id`

---

## 🌐 Web UI
   - To run a lightweight Flask interface:

     ````bash
     python app.py
     ````
   - Then navigate to http://localhost:5000 (Flask).
   
   - **Main Dashboard**<br><br>![Main Dashboard](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/main_dashboard1.png)
   - **After Running the Model**<br><br>![After Running the model](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/main_dashboard2.png)
   - **Categorised Table**<br><br>![Categorised table](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/categorised_table.png)
   - **Category Distribution Bar Graph**<br><br>![Category Distribution Bar Graph](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/category_distribution_bar_graph.png)
   - **Supplier By Amount Distribution Bar Graph**<br><br>![ Supplier By Amount Distribution Bar Graph](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/supplier_amount_distribution.png)
   - **Supplier Distribution Pie Chart**<br><br>![Supplier Distribution Pie Chart](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/supplier_distribution_pie_chart.png)
   - **Confidence Distribution Pie Chart**<br><br>![Confidence Distribution Pie Chart](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/confidence_distribution_pie_chart.png)
   - **Manual Review UI**<br><br>![Manual Review UI](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/manual_review_dashboard.png)
   - **Manual Review Dropdown and Seachbar**<br><br>![Manual Review Dropdown](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/manual_review_searchbar.png)
   - **Model Performance Metrics**<br><br>![Model Performance Metrics](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/model_performance_metrics.png)
   - **Category Wise Performance**<br><br>![Category Wise Performance](https://github.com/komal2203/acme-spend-categorization/blob/main/ui_images_for_readme/category_wise_performance.png)



---

## 💻 How It Works
   - **Sanitization**: Cleans and normalizes invoice text
   - **Rule Matching**: Applies analyst-defined keyword rules
   - **Semantic Retrieval**: Finds top UNSPSC candidates via embedding similarity
   - **AI Selection**: GPT-4 picks the most likely UNSPSC code
   - **Confidence Routing**: Items below threshold are queued for manual review

---

## 📊 Performance & Monitoring
   - Multi-core parallel processing via multiprocessing
   - Confidence-based classification routing
   - Logs available in logs/pipeline.log

---


## 📅 Roadmap
   - More robust rule engine (regex, entity recognition)
   - Spend analytics dashboard
   - RESTful API endpoints for integration
   - Scheduled batch job manager
   - User-friendly UI

---

## 🤝 Collaborators
   - Komal Meena
   - Subhav Jain
   - Sidhant Budhiraja
   - Prayash Pandey

---



## ⚙️ Prerequisites

   - Python 3.9+
   - [OpenAI API Key](https://platform.openai.com/account/api-keys)

---


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

## 🖥️ Usage

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

## 📚 Acknowledgments
   - OpenAI for powerful AI APIs
   - UNSPSC.org for the classification taxonomy
   - Sentence-Transformers for semantic search


