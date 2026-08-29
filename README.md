# Factory-to-Customer-Shipping-Route-Efficiency-Analysis-for-Nassau-Candy-Distributor
## Project objective 
The objective of this project is to analyze shipping efficiency and lead-time performance using Excel data and Microsoft Power BI. The project evaluates route-level, regional, and ship-mode performance, identifies potential bottlenecks, and provides an interactive dashboard with filters and drill-down capabilities to support data-driven decision-making.

## Dataset 
-<a href="https://github.com/jyotismoy04/Factory-to-Customer-Shipping-Route-Efficiency-Analysis-for-Nassau-Candy-Distributor/blob/main/Nassau.xlsx">Dataset</a>

## 🛠️ Tech Stack
Data Analysis
Python
NumPy
Microsoft Excel / XLSX

Business Intelligence
Microsoft Power BI
DAX
Power BI Slicers
KPI Cards
Interactive Visualizations
Geographic Maps

Python Dashboard
Streamlit
Plotly
Pandas
OpenPyXL

Development & Version Control
Git
GitHub


# 🚚 Shipping Efficiency & Lead-Time Analytics

An interactive logistics analytics project designed to evaluate shipping efficiency, delivery lead times, route performance, regional bottlenecks, and shipping-mode performance using Power BI and Python.

The project combines business intelligence and interactive Python analytics to provide operational insights into shipping performance and support data-driven decision-making.

---

## 📌 Project Overview

Efficient shipment management is critical for reducing delivery delays, improving customer satisfaction, controlling operational costs, and optimizing logistics performance.

This project analyzes shipment-level data to identify:

- Shipping lead-time patterns
- High- and low-performing routes
- Regional bottlenecks
- Shipping-mode performance
- State-level performance differences
- Delayed shipment frequency
- Route efficiency
- Order-level shipment timelines

---

## 🎯 Project Objective

The primary objective of this project is to develop an interactive shipping analytics solution that enables business stakeholders to monitor logistics performance and identify operational inefficiencies.

The project focuses on:

- Measuring shipment lead time
- Comparing route performance
- Identifying regional bottlenecks
- Evaluating shipping methods
- Monitoring delayed shipments
- Measuring route efficiency
- Providing interactive filtering capabilities
- Supporting data-driven logistics decisions

---

## 📊 Key Performance Indicators

The dashboard contains the following KPIs:

| KPI | Description |
|---|---|
| Shipping Lead Time | Difference between Ship Date and Order Date |
| Average Lead Time | Average shipment duration |
| Route Volume | Number of unique orders handled by a route |
| Delay Frequency | Percentage of shipments exceeding the selected lead-time threshold |
| Route Efficiency Score | Normalized score representing route performance |

---

## 📈 Dashboard Modules

### 1. Route Efficiency Overview

Provides:

- Average lead time by State/Province
- Route performance leaderboard
- Route ranking based on average lead time

Lower lead time represents better operational performance.

---

### 2. Geographic Shipping Analysis

Provides:

- US shipping efficiency heatmap
- Regional bottleneck visualization
- Geographic comparison of average shipment lead time

The geographic analysis helps identify areas where shipping performance may require operational attention.

---

### 3. Ship Mode Comparison

Compares average lead time across different shipping methods.

This allows stakeholders to evaluate the relative performance of shipping modes and identify opportunities for optimization.

---

### 4. State-Level Performance Insights

Provides detailed state-level metrics including:

- Average lead time
- Median lead time
- Order volume
- Sales
- Gross profit

---

### 5. Order-Level Shipment Timeline

Provides shipment-level information including:

- Order ID
- Order Date
- Ship Date
- Lead Time
- Ship Mode
- Region
- State/Province
- Sales
- Gross Profit

An Order ID search feature is also provided.

---

## 🎛️ Interactive Dashboard Features

The dashboard supports:

- Date range filtering
- Region filtering
- State/Province filtering
- Ship Mode filtering
- Lead-time threshold filtering
- Order ID search
- Interactive charts
- Dynamic KPI calculations
- Filtered data exploration

---

## 🧮 Lead-Time Calculation

Shipping lead time is calculated as:
```text
Lead Time = Ship Date - Order Date
