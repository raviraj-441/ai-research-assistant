# AI Research Assistant

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Overview

AI Research Assistant is a powerful tool that leverages artificial intelligence to conduct thorough research, perform fact-checking, and generate professional reports. It streamlines the research process by automating information gathering, validation, and report generation, making it an invaluable tool for researchers, students, and professionals.

## 🖥️ Live Demo

Try the app live: [AI Research Assistant on Streamlit](https://ai-research-assistant-raviraj-441.streamlit.app/)

---

## ✨ Key Features

- 🔍 **Automated Research** with iterative refinement and deep analysis
- ✅ **Fact-checking and Validation** ensuring information accuracy
- 📊 **Professional Report Generation** with structured formatting
- 📁 **Multiple Export Options** (PDF and Markdown formats)
- 📈 **Interactive Progress Tracking** with real-time updates
- 🎯 **Customizable Research Depth** for tailored results

## 🛠️ Prerequisites

- Python 3.8 or higher
- [Tavily API key](https://tavily.com) for research capabilities
- [Groq API key](https://groq.com) for AI processing

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/raviraj-441/ai-research-assistant.git
   cd ai-research-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   TAVILY_API_KEY=your_tavily_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🚀 Getting Started

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**
   
   Open your browser and navigate to `http://localhost:8501`

## 📝 Usage Guide

1. **Enter Research Query**
   - Type your research topic or question in the sidebar
   - Be specific for better results

2. **Configure Research Parameters**
   - Set iterations (1-10) based on desired thoroughness
   - Adjust depth level to control search intensity

3. **Monitor Progress**
   - Track real-time research progress
   - View source validation and fact-checking status

4. **Export Results**
   - Download comprehensive reports in PDF or Markdown format
   - Access structured research findings with citations

## 📁 Project Structure

```
├── app.py           # Main Streamlit application
├── agents.py        # AI research agent implementations
├── config.py        # Configuration and settings
├── requirements.txt # Project dependencies
└── .env            # Environment variables
```

## 🔍 Advanced Usage Tips

- **Research Depth**: Higher depth levels perform more thorough but slower searches
- **Iterations**: More iterations improve fact-checking accuracy but increase processing time
- **Export Formats**: 
  - PDF: Best for formal presentations
  - Markdown: Ideal for further editing or integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Tavily API](https://tavily.com) for research capabilities
- [Groq](https://groq.com) for AI processing
- [Streamlit](https://streamlit.io) for the web interface

## 📧 Contact

For questions and support, please open an issue in the GitHub repository.
