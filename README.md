# Xboard - Automated Excel Dashboard Generator

📌 **Project Overview**  
Xboard is an intelligent Flask-based web platform that enables users to instantly convert raw Excel or CSV datasets into fully formatted, insightful Excel dashboards. It’s designed to simplify data analysis for non-technical users by automating data cleaning, summary statistics, and visual chart generation – all embedded in a downloadable Excel file.

---

🎯 **Features**

- 📂 **Data Upload Interface** → User-friendly web UI built with TailwindCSS.
- 🧠 **Smart Dataset Type Detection** → Identifies whether the dataset is Sales, HR, Marketing, or General.
- 🧹 **Data Cleaning** → Removes nulls, handles infinities, and prepares clean data for reporting.
- 📊 **Automated Visualizations** → Creates charts like histograms and bar graphs using Matplotlib & Seaborn.
- 📈 **Statistical Summaries** → Calculates mean, median, and standard deviation for numerical columns.
- 📥 **Downloadable Excel Dashboard** → Generates polished dashboards with embedded visuals and stats using OpenPyXL.
- ⚡ **Real-Time Processing** → Generates insights within seconds after upload.

---

🛠️ **Technologies Used**

- **Frontend:** HTML, Tailwind CSS, JavaScript  
- **Backend:** Flask (Python)  
- **Data Handling:** Pandas, NumPy  
- **Visualizations:** Matplotlib, Seaborn  
- **Excel Integration:** OpenPyXL  
- **File Upload Handling:** Werkzeug + Flask file management

---

🚀 **How to Run the Project**

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/xboard.git
   cd xboard
