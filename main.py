import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

filepaths = glob.glob("excelFiles/*.xlsx")

for filepath in filepaths:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    filename = Path(filepath).stem
    invoice_nr, date = filename.split("-")

    pdf.set_font(family="Times", style="B", size=16)
    pdf.cell(w=50, h= 8, txt=f"Invoice nr. {invoice_nr}", ln=1)

    pdf.set_font(family="Times", style="B", size=16)
    pdf.cell(w=50, h= 8, txt=f"Date: {date}", ln=1)

    df = pd.read_excel(filepath, sheet_name="Sheet 1")

    #add a header
    columns = df.columns
    columns = [item.replace("_", " ").title() for item in columns]
    pdf.set_font(family="Times", style="B", size=10)
    pdf.set_text_color(80, 80, 80)
    for column in columns:
        #pdf.cell(w=30, h=8, txt=column, border=1, ln=0)
        if column == "Product Name":
            pdf.cell(w=70, h=8, txt=column, border=1, ln=0)
        elif column == "Total Price":
            pdf.cell(w=30, h=8, txt=column, border=1, ln=1)
        else:
            pdf.cell(w=30, h=8, txt=column, border=1, ln=0)
            
    #pdf.cell(w=30, h=8, txt=columns[0], border=1, ln=0)
    #pdf.cell(w=70, h=8, txt=columns[1], border=1, ln=0)
    #pdf.cell(w=30, h=8, txt=columns[2], border=1, ln=0)
    #pdf.cell(w=30, h=8, txt=columns[3], border=1, ln=0)
    #pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

    #Add rows
    for index, row in df.iterrows():
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1, ln=0)
        pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1, ln=0)
        pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1, ln=0)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1, ln=0)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

    total_sum = df["total_price"].sum()
    pdf.set_font(family="Times", size=10)
    pdf.set_text_color(80, 80, 80)
    for i in range(4):
        if i == 1:
            pdf.cell(w=70, h=8, txt=" ", border=1, ln=0)
        else:
            pdf.cell(w=30, h=8, txt=" ", border=1, ln=0)
    pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

    #add total sum sentence
    pdf.set_font(family="Times", size=10, style="B")
    pdf.cell(w=30, h=8, txt=f"The total sum is {total_sum}", ln=1)

    #add company name and logo
    pdf.set_font(family="Times", size=14, style="B")
    pdf.cell(w=20, h=8, txt="Chill.Inc", ln=0)
    pdf.image("images/logo.png", w=10)


    pdf.output(f"pdfFiles/{filename}.pdf")