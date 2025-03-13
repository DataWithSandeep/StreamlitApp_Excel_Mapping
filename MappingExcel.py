import streamlit as st
from io import BytesIO
import pandas as pd


# Function to map hierarchy values
def map_hierarchy(unit_no, mapping_dict):
    units = unit_no.split(',')  # Split multiple units
    hierarchies = [mapping_dict.get(unit.strip(), 'Unknown') for unit in units]  # Map hierarchy
    return ', '.join(hierarchies)  # Join multiple hierarchy values

# Function to process data
def mapping_fun(file1, file2, custom_filename, file_format):
    df1 = pd.read_excel(file1)
    df_H = df1.iloc[7:]
    df_H.columns = list(df_H.iloc[0])
    df_H1 = df_H.iloc[1:].reset_index(drop=True)

    invoice = pd.read_excel(file2)
    invoice1 = invoice.iloc[8:]
    invoice1.columns = list(invoice1.iloc[0])
    invoice2 = invoice1.iloc[1:].reset_index(drop=True)

    # Creating a mapping dictionary
    mapping_dict = df_H1.set_index('Plot Number')['Project Hierarchy'].to_dict()

    # Apply mapping function
    invoice2['Hierarchy'] = invoice2['Unit No'].apply(lambda x: map_hierarchy(x, mapping_dict))
    
    df = invoice2.copy()
    df['Hierarchy'] = df['Hierarchy'].apply(lambda x: x.split(',')[0])
    df[['Parent Hierarchy', 'Child Hierarchy']]  = df['Hierarchy'].str.split('>>', expand=True)
    desired_columns = ['Company GSTIN', 'Company CIN', 'Business Unit', 
                    'Parent Hierarchy', 'Child Hierarchy', 'Document No',
                    'Document Date', 'Booking No', 'Application No', 
                    'Generation Date', 'Validation Date', 'Customer Code', 
                    'Customer Name', 'Customer Name Arabic', 'Customer Email Id', 
                    'Finance Ledger Name', 'Unit No', 'DM Plot No', 'Related Party', 
                    'Grace Period', 'Period From', 'Period To', 'Invoice Type', 
                    'Invoice Month', 'Due Date', 'GSTIN', 'Place of Supply', 
                    'Area (Sq Feet)', 'Billing Rate', 'RevenueHead Description', 
                    'GST Amount', 'Previous Dues', 'Total Payable', 'Interest Charges', 
                    'GST On Interest', 'Total Payable with Interest', 'Amount', 'Tax', 
                    'Net Amount', 'Discount', 'Narration', 'Hijri From', 'Hijri To', 'Hierarchy']
    # print(df.columns)
    df = df[desired_columns]
    df_modified = df.drop('Hierarchy', axis=1)

    # Ensure the filename has the correct extension
    if file_format == "Excel (.xlsx)":
        if not custom_filename.endswith(".xlsx"):
            custom_filename += ".xlsx"
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_modified.to_excel(writer, index=False, sheet_name='Sheet1')
            worksheet = writer.sheets['Sheet1']

            # Set column widths
            for col_num, col_name in enumerate(df_modified.columns):
                max_length = max(df_modified[col_name].astype(str).apply(len).max(), len(col_name))
                worksheet.set_column(col_num, col_num, max(max_length + 2, 20))

            # Apply table format
            num_rows, num_cols = df_modified.shape
            worksheet.add_table(0, 0, num_rows, num_cols - 1, {
                'columns': [{'header': col} for col in df_modified.columns],
                'header_row': True,
                'autofilter': True,
                'style': 'Table Style Medium 2'
            })

            # Apply autofilter
            # worksheet.autofilter(0, 0, num_rows, num_cols - 1)

        output.seek(0)
        return output, custom_filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    elif file_format == "CSV (.csv)":
        if not custom_filename.endswith(".csv"):
            custom_filename += ".csv"

        output = BytesIO()
        df_modified.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)
        return output, custom_filename, "text/csv"


# Streamlit UI
st.title("Excel & CSV Processing App")

file1 = st.file_uploader("Upload Unit Register Excel file", type=['xlsx'])
file2 = st.file_uploader("Upload Invoice Register Excel file", type=['xlsx'])

# Custom file name input (only name, not extension)
custom_filename = st.text_input("Enter custom output file name (without extension)", "invoice_register_detail")

# File format selection
file_format = st.radio("Select output file format", ["Excel (.xlsx)", "CSV (.csv)"], index=0)  # Default is Excel

if st.button("Process Data"):
    if file1 and file2:
        output_file, filename, mime_type = mapping_fun(file1, file2, custom_filename, file_format)
        st.success(f"File processed successfully: {filename}")

        # Provide download button
        st.download_button(label="Download Processed File", data=output_file, file_name=filename, mime=mime_type)
    else:
        st.error("Please upload both Excel files to proceed.")
