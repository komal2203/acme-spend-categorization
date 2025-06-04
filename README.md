# ACME Spend Categorization

An intelligent invoice categorization system that automatically categorizes spend data using a combination of rule-based and AI-powered classification.

## Overview

This system processes invoice data to automatically categorize spend items according to the UNSPSC (United Nations Standard Products and Services Code) taxonomy. It uses a hybrid approach combining:
- Rule-based classification
- AI-powered categorization using OpenAI's models
- Manual review interface for low-confidence classifications

## Features

- **Automated Categorization**: Process large volumes of invoice data automatically
- **Hybrid Classification**: Combines rule-based and AI-powered approaches
- **Confidence Scoring**: Each categorization comes with a confidence score
- **Manual Review Interface**: Easy review and correction of low-confidence categorizations
- **Data Visualization**: Interactive charts and analytics
- **Export Capabilities**: Download categorized data in CSV format

## Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/acme-spend-categorization.git
cd acme-spend-categorization
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:



## Usage

1. **Web Interface**:
```bash
python app.py
```
Access the web interface at `http://localhost:5000`

2. **Upload Data**:
- Prepare your invoice data in CSV format
- Required columns: Description, Supplier, Amount, Invoice Id
- Upload through the web interface

3. **Process Data**:
- The system will automatically:
  - Apply rule-based classification
  - Use AI for unclassified items
  - Generate confidence scores
  - Create manual review queue for low-confidence items

4. **Review and Export**:
- Review low-confidence categorizations
- Make corrections if needed
- Export final categorized data

## Memory Management

The system is optimized for memory efficiency:
- Processes API Calls in Parallel
- Implements garbage collection
- Uses CPU-optimized versions of ML libraries
- Monitors memory usage during processing

## Deployment

### Local Deployment
1. Install dependencies
2. Set up environment variables
3. Run `python app.py`

### Render Deployment
1. Create a new Web Service on Render
2. Connect your repository
3. Set environment variables
4. Deploy

## Performance Considerations

- **Memory Usage**: Monitor through logs/pipeline.log
- **Processing Speed**: Varies based on data volume and complexity
- **API Usage**: OpenAI API calls are optimized for cost efficiency

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request



## Support

For support, please:
1. Check the documentation
2. Review existing issues
3. Create a new issue if needed

## Acknowledgments

- OpenAI for AI models
- UNSPSC for taxonomy

##Collaborators 
- Subhav Jain
- Sidhant Budhiraja
- Komal Meena
- Prayash Pandey

## Roadmap

- [ ] Enhanced rule engine
- [ ] Additional visualization options
- [ ] Batch processing improvements
- [ ] API endpoint development
- [ ] Mobile interface

## Changelog

### Version 1.0.0
- Initial release
- Basic categorization functionality
- Web interface
- Manual review system

