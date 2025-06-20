import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend for matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils.dataframe import dataframe_to_rows

def generate_dashboard(input_path, output_path):
    try:
        # Load dataset
        if input_path.endswith(".csv"):
            df = pd.read_csv(input_path)
        else:
            df = pd.read_excel(input_path)

        # Basic cleaning
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(how='all', axis=1, inplace=True)
        df.dropna(how='all', axis=0, inplace=True)

        # Detect column types
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # Setup workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Dashboard"

        # Basic info
        ws.append(["Xboard Auto Dashboard"])
        ws.append(["Total Rows", df.shape[0]])
        ws.append(["Total Columns", df.shape[1]])
        ws.append([])
        ws.append(["Numeric Summary"])

        for col in numeric_cols:
            ws.append([col, "Mean", df[col].mean()])
            ws.append([col, "Median", df[col].median()])
            ws.append([col, "Std Dev", df[col].std()])

        # Chart folder
        img_dir = "temp_charts"
        os.makedirs(img_dir, exist_ok=True)
        chart_paths = []

        # Bar charts for categorical
        for col in categorical_cols[:2]:
            top_values = df[col].value_counts().head(10)
            if not top_values.empty:
                plt.figure(figsize=(6, 4))
                top_values.plot(kind='bar', color='skyblue')
                plt.title(f"Top {col}")
                chart_file = os.path.join(img_dir, f"{col}_bar.png")
                plt.tight_layout()
                plt.savefig(chart_file)
                chart_paths.append(chart_file)
                plt.close()

        # Histograms for numeric
        for col in numeric_cols[:2]:
            if df[col].dropna().nunique() > 1:
                plt.figure(figsize=(6, 4))
                sns.histplot(df[col].dropna(), kde=True, color='lightgreen')
                plt.title(f"Distribution of {col}")
                chart_file = os.path.join(img_dir, f"{col}_hist.png")
                plt.tight_layout()
                plt.savefig(chart_file)
                chart_paths.append(chart_file)
                plt.close()

        # Add charts to Excel
        ws.append([])
        ws.append(["Charts"])
        row_cursor = ws.max_row + 1
        for chart in chart_paths:
            img = XLImage(chart)
            img.width = 400
            img.height = 250
            ws.add_image(img, f"A{row_cursor}")
            row_cursor += 16

        # Save Excel
        wb.save(output_path)

        # Clean up chart images
        for chart in chart_paths:
            if os.path.exists(chart):
                os.remove(chart)
        if os.path.exists(img_dir) and not os.listdir(img_dir):
            os.rmdir(img_dir)

        return output_path

    except Exception as e:
        print(f"Error generating dashboard: {e}")
        return None
