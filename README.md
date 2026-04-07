
```markdown
# European Bakery Sales Analysis — Data Visualisation Portfolio

## COM7021 - Data Visualisation
**Student:** Farid Negahbani
**Student ID:** 24154844

---

## Project Overview

This project analyses European bakery sales data across multiple cities and confectionery types. It includes static visualisations built with Matplotlib and Seaborn, and an interactive dashboard built with Plotly Dash.

---

## Repository Contents

| File | Description |
|------|-------------|
| `bakery_cleaned.csv` | Cleaned dataset used for all visualisations |
| `static_visualisations.py` | Python script generating 6 static charts (Matplotlib & Seaborn) |
| `dashboard_app.py` | Plotly Dash interactive dashboard application |
| `README.md` | This file — setup and usage instructions |
| `report.pdf` | Written report with analysis and design rationale |

---

## Dataset

The dataset contains European bakery sales records with the following columns:

- **Date** — Transaction date
- **City** — City where the sale occurred
- **Confectionary** — Type of bakery product sold
- **Units Sold** — Number of units sold
- **Revenue(£)** — Total revenue in GBP
- **Profit(£)** — Total profit in GBP
- **Profit_Margin(%)** — Profit as a percentage of revenue
- **Year** — Extracted year from the date

---

## Prerequisites

Make sure you have **Python 3.8 or higher** installed on your system.

### Required Libraries

```
pandas
matplotlib
seaborn
plotly
dash
```

---

## Installation

### Step 1 — Clone or Download the Project

Download all project files into a single folder on your computer.

### Step 2 — Open a Terminal or Command Prompt

Navigate to the project folder:

```
cd path/to/your/project/folder
```

### Step 3 — Install Required Libraries

Run the following command to install all dependencies at once:

```
pip install pandas matplotlib seaborn plotly dash
```

If you are using a virtual environment (recommended):

```
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux
pip install pandas matplotlib seaborn plotly dash
```

---

## How to Run

### Static Visualisations

This script generates 6 static charts and saves them as image files:

```
python static_visualisations.py
```

The following charts will be generated:

1. Profit by City (horizontal bar chart)
2. Profit by Confectionery (bar chart)
3. Yearly Profit Trends (line chart)
4. Revenue vs Profit (scatter plot)
5. Profit Margin Heatmap (City × Confectionery)
6. Profit Treemap (hierarchical breakdown)

### Interactive Dashboard

To launch the Plotly Dash dashboard:

```
python dashboard_app.py
```

Then open your web browser and go to:

```
http://127.0.0.1:8050
```

To stop the dashboard, press `Ctrl + C` in the terminal.

---

## Dashboard Features

### Filters

- **City Dropdown** — Filter data by a specific city or view all cities
- **Confectionery Dropdown** — Filter data by product type or view all types
- **Year Range Slider** — Select a range of years to analyse

### KPI Cards

- Total Revenue
- Total Profit
- Average Profit Margin
- Total Units Sold

### Interactive Charts

| Chart | Description |
|-------|-------------|
| Profit by City | Horizontal bar chart showing total profit per city |
| Profit by Confectionery | Bar chart comparing profit across product types |
| Yearly Profit Trends | Line chart showing profit trends over time by city |
| Revenue vs Profit | Scatter plot exploring the relationship between revenue and profit |
| Profit Margin Heatmap | Heatmap showing average margin for each city and product combination |
| Profit Treemap | Hierarchical treemap showing profit distribution across cities and products |

All charts update automatically when any filter is changed.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'dash'` | Run `pip install dash` |
| `ModuleNotFoundError: No module named 'plotly'` | Run `pip install plotly` |
| `FileNotFoundError: bakery_cleaned.csv` | Make sure the CSV file is in the same folder as the Python scripts |
| `TypeError: Dict key must be a type serializable` | Make sure you are using the latest fixed version of `dashboard_app.py` |
| Port 8050 already in use | Close other Dash apps or change the port: `app.run(debug=True, port=8060)` |
| Charts show no data | Adjust the filters — some City + Confectionery combinations may not exist |

---

## Technologies Used

- **Python 3** — Programming language
- **Pandas** — Data manipulation and analysis
- **Matplotlib** — Static chart generation
- **Seaborn** — Statistical visualisation styling
- **Plotly** — Interactive chart library
- **Dash** — Web-based dashboard framework

---

## License

This project is submitted as coursework for COM7021 Data Visualisation at the University of Sheffield. It is intended for academic purposes only.
```
