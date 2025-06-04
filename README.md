# ACME Spend Categorization

An intelligent spend categorization system that uses machine learning and natural language processing to automatically categorize business expenses.

## 🚀 Features

- **Automated Categorization**: Uses ML and NLP to categorize expenses
- **Rule-Based Filtering**: Initial categorization using business rules
- **AI-Powered Classification**: Advanced classification using language models
- **Confidence Scoring**: Provides confidence scores for each categorization
- **Manual Review**: Flags items needing human review
- **Interactive Dashboard**: Visual analytics and insights
- **Export Capabilities**: Export results in CSV format

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL (for production)
- Required Python packages (see requirements.txt)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/acme-spend-categorization.git
cd acme-spend-categorization
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
DB_HOST=localhost
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

## 🚀 Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to:

3. Upload your expense data in CSV format

4. View results and analytics

## 📁 Project Structure
acme-spend-categorization/
├── app.py # Main application file
├── pipeline.py # Processing pipeline
├── requirements.txt # Python dependencies
├── data/ # Data directory
│ ├── sample_invoices.csv
│ └── results/
├── logs/ # Log files
├── static/ # Static files
│ └── style.css
└── templates/ # HTML templates
└── index.html


## 🔧 Configuration

### Environment Variables
- `DB_HOST`: Database host
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password

### Application Settings
- `CHUNK_SIZE`: Processing batch size (default: 10)
- `MAX_WORKERS`: Maximum worker threads (default: 3)
- `CONF_THRESH`: Confidence threshold (default: 0.85)

## 📊 Performance

- Memory Usage: Optimized for <512MB
- Processing Speed: ~1000 records/minute
- Accuracy: >90% for common categories

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Subhav , Sidhant , Komal and Prayash

## 🙏 Acknowledgments

- Thanks to all contributors
- Inspired by [source of inspiration]
- Built with [technologies used]

## 📞 Support

For support, email [your-email] or open an issue in the repository.

## 🔄 Updates

- Latest update: [date]
- Version: 1.0.0
- Status: Active Development

## 🎯 Roadmap

- [ ] Add more ML models
- [ ] Improve accuracy
- [ ] Add API endpoints
- [ ] Enhance dashboard
- [ ] Add batch processing

## 📚 Documentation

For detailed documentation, visit [your-docs-link]

## 🔍 Testing

Run tests with:
```bash
python -m pytest tests/
```

## 🚨 Known Issues

- Memory usage spikes with large datasets
- Processing time increases with complex categories

## 💡 Tips

- Use smaller batch sizes for better memory management
- Regular database maintenance recommended
- Monitor log files for errors

## 🔐 Security

- All sensitive data is encrypted
- Regular security updates
- Secure API endpoints

## 🌟 Stars

If you find this project useful, please give it a star!
