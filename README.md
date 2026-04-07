# European Bakery Sales Analysis
### Data Visualisation Portfolio Project

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-Academic-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-success?style=flat-square)

A comprehensive data visualisation project analysing European bakery sales across multiple cities and confectionery types. Features both static visualisations and an interactive web-based dashboard.

**Module:** COM7021 - Data Visualisation  
**Student:** Farid Negahbani  
**Student ID:** 24154844  
**Institution:** Arden University  
**Professor:** Dr. Ahmed Hassan

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard Features](#dashboard-features)
- [Technologies](#technologies)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

This project demonstrates advanced data visualisation techniques through analysing European bakery sales data. It combines exploratory static visualisations with an interactive dashboard, providing insights into sales performance, profitability, and market trends across different cities and product categories.

### Key Insights
- Sales performance analysis across European cities
- Profitability trends and margin analysis
- Product category performance comparison
- Revenue-to-profit relationship exploration
- Temporal trends and seasonality patterns

---

## ✨ Features

### Static Visualisations
- **Profit by City** — Horizontal bar chart for easy comparison
- **Profit by Confectionery** — Product category performance analysis
- **Yearly Profit Trends** — Temporal analysis with line charts
- **Revenue vs Profit** — Scatter plot showing relationships
- **Profit Margin Heatmap** — City × Product cross-tabulation
- **Profit Treemap** — Hierarchical breakdown of sales data

### Interactive Dashboard
- 🎨 Real-time filtering and dynamic chart updates
- 📊 Responsive design with multiple visualisation types
- 📈 KPI cards for quick metrics overview
- 🔍 Multi-level filtering capabilities

---

## 📁 Repository Structure

```
.
├── README.md                    # This file
├── bakery_cleaned.csv           # Cleaned dataset
├── bakery_analysis.py           # Static chart generation script
├── dashboard_app.py             # Interactive Dash application
├── report.pdf                   # Detailed analysis report
└── requirements.txt             # Python dependencies
```

---

## 📊 Dataset

The dataset contains European bakery sales records with the following attributes:

| Column | Type | Description |
|--------|------|-------------|
| `Date` | datetime | Transaction date |
| `City` | string | Sale location |
| `Confectionary` | string | Bakery product type |
| `Units Sold` | integer | Number of units sold |
| `Revenue(£)` | float | Total revenue in GBP |
| `Profit(£)` | float | Total profit in GBP |
| `Profit_Margin(%)` | float | Profit as percentage of revenue |
| `Year` | integer | Extracted from date |

---

## 🚀 Installation

### Prerequisites

- **Python 3.8** or higher
- **pip** (Python package manager)

### Quick Start

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd european-bakery-sales-analysis
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS / Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install pandas matplotlib seaborn plotly dash
   ```

---

## 📖 Usage

### Running Static Visualisations

Generate 6 static charts and save them as image files:

```bash
python bakery_analysis.py
```

**Output:** PNG files saved in the project directory for the following visualisations:
- Profit by City
- Profit by Confectionery
- Yearly Profit Trends
- Revenue vs Profit Scatter Plot
- Profit Margin Heatmap
- Profit Treemap

### Running the Interactive Dashboard

Launch the Plotly Dash web application:

```bash
python dashboard_app.py
```

Then open your web browser and navigate to:

```
http://127.0.0.1:8050
```

**To stop the dashboard:** Press `Ctrl + C` in the terminal.

---

## 📊 Dashboard Features

### Filtering Controls

| Filter | Purpose |
|--------|---------|
| **City Dropdown** | Filter by specific city or view all cities |
| **Confectionery Dropdown** | Filter by product type or view all types |
| **Year Range Slider** | Select analysis period |

### Key Performance Indicators (KPIs)

The dashboard displays four KPI cards:
- 💰 **Total Revenue** — Aggregate revenue in GBP
- 📈 **Total Profit** — Total profit across selected filters
- 📊 **Average Profit Margin** — Mean profit margin percentage
- 📦 **Total Units Sold** — Sum of all units

### Interactive Charts

| Chart Type | Description |
|-----------|-------------|
| **Profit by City** | Horizontal bar chart for city-level comparison |
| **Profit by Confectionery** | Product category performance analysis |
| **Yearly Profit Trends** | Line chart showing temporal patterns by city |
| **Revenue vs Profit** | Scatter plot with correlation insights |
| **Profit Margin Heatmap** | City × Product combination analysis |
| **Profit Treemap** | Hierarchical profit distribution |

**Dynamic Updates:** All charts update automatically when filters are changed.

---

## 🛠️ Technologies

| Technology | Purpose |
|-----------|---------|
| **Python 3** | Core programming language |
| **Pandas** | Data manipulation and analysis |
| **Matplotlib** | Static visualisation generation |
| **Seaborn** | Statistical visualisation styling |
| **Plotly** | Interactive charting library |
| **Dash** | Web application framework |

---

## 🔧 Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'dash'` | Run `pip install dash` |
| `ModuleNotFoundError: No module named 'plotly'` | Run `pip install plotly` |
| `FileNotFoundError: bakery_cleaned.csv` | Ensure CSV file is in the project root directory |
| `TypeError: Dict key must be a type serializable` | Update `dashboard_app.py` to the latest version |
| Port 8050 already in use | Change port in code: `app.run(debug=True, port=8060)` |
| Dash dashboard won't start | Check Python version is 3.8+ and all dependencies are installed |
| Charts display no data | Adjust filters—some City × Confectionery combinations may not exist |

### Getting Help

If you encounter issues:
1. Verify all files are in the correct directory
2. Check Python version: `python --version`
3. Reinstall dependencies: `pip install --upgrade -r requirements.txt`
4. Review error messages for specific module issues

---

## 📝 Project Structure Explanation

### `static_visualisations.py`
Generates six static visualisations using Matplotlib and Seaborn. Outputs PNG files for presentations and reports.

### `dashboard_app.py`
Plotly Dash application providing interactive exploration of the data. Includes filtering controls and responsive charts.

### `bakery_cleaned.csv`
Pre-processed dataset ready for analysis. No data cleaning steps required.

---

## 📄 Documentation

- **Report** — See `report.pdf` for detailed analysis, design rationale, and findings
- **Code Comments** — Both Python scripts include inline documentation
- **Visualisation Descriptions** — Each chart includes a title and axis labels for clarity

---

## ✅ Quality Assurance

- ✓ All dependencies pinned to stable versions
- ✓ Error handling for common issues
- ✓ Cross-platform compatibility (Windows, macOS, Linux)
- ✓ Code follows PEP 8 style guidelines
- ✓ Comprehensive documentation included

---

## 📜 License

This project is submitted as coursework for **COM7021 Data Visualisation** at **Arden University** under the supervision of **Dr. Ahmed Hassan**. It is intended for **academic purposes only**.

---

## 👨‍💻 Author

**Farid Negahbani**  
Student ID: 24154844  
Arden University  
Module: COM7021 - Data Visualisation  
Supervisor: Dr. Ahmed Hassan

---

## 📚 Additional Resources

- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Plotly Dash Documentation](https://dash.plotly.com/)
- [Seaborn Documentation](https://seaborn.pydata.org/)

---

**Last Updated:** April 2026  
**Project Status:** Complete ✓
