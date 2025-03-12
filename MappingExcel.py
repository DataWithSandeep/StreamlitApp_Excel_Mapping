import streamlit as st
import pandas as pd
from io import BytesIO

# Function to map hierarchy values
def map_hierarchy(unit_no, mapping_dict):
    units = unit_no.split(',')  # Split multiple units
    hierarchies = [mapping_dict.get(unit.strip(), 'Unknown') for unit in units]  # Map hierarchy
    return ', '.join(hierarchies)  # Join multiple hierarchy values

# Function to process data
def mapping_fun(file1, file2, output_filename="invoice_register_detail.xlsx"):
    df1 = pd.read_excel(file1)
    df_H = df1.iloc[7:]
    col_h = list(df_H.iloc[0])
    df_H.columns = col_h
    df_H1 = df_H.iloc[1:].reset_index(drop=True)

    invoice = pd.read_excel(file2)
    invoice1 = invoice.iloc[8:]
    col_1 = list(invoice1.iloc[0])
    invoice1.columns = col_1
    invoice2 = invoice1.iloc[1:].reset_index(drop=True)

    # Creating a mapping dictionary
    mapping_dict = df_H1.set_index('Plot Number')['Project Hierarchy'].to_dict()

    # Apply mapping function
    invoice2['Hierarchy'] = invoice2['Unit No'].apply(lambda x: map_hierarchy(x, mapping_dict))

    # Process the hierarchy column
    df = invoice2.copy()
    df['Hierarchy'] = df['Hierarchy'].apply(lambda x: x.split(',')[0])
    df[['Hierarchy1', 'Hierarchy2']] = df['Hierarchy'].str.split('>>', expand=True)
    df = df.drop('Hierarchy', axis=1)

    # Save to Excel in-memory
    output = BytesIO()
    df.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)

    return output, output_filename

# Streamlit UI
st.title("Excel File Processor - Hierarchy Mapping")

# Upload files
file1 = st.file_uploader("Upload Unit Register Excel file", type=['xlsx'])
file2 = st.file_uploader("Upload Invoice Register Excel file", type=['xlsx'])

# Custom file name
custom_filename = st.text_input("Enter custom output file name (default: invoice_register_detail.xlsx)", "invoice_register_detail.xlsx")

if st.button("Process Data"):
    if file1 and file2:
        output_file, filename = mapping_fun(file1, file2, custom_filename)
        st.success(f"File processed successfully: {filename}")

        # Provide download button
        st.download_button(label="Download Processed Excel File", data=output_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error("Please upload both Excel files to proceed.")
