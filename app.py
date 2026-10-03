import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Data Cleaning & Reporting Automation",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Cleaning & Reporting Automation")
st.write(
    "Automatically clean data, analyze it, and generate reports."
)

# -------------------------------
# File Upload
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # -------------------------------
    # Read File
    # -------------------------------

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # -------------------------------
    # Raw Data
    # -------------------------------

    st.subheader("📋 Raw Data")

    st.dataframe(
        df,
        use_container_width=True
    )

    # -------------------------------
    # Original Data Statistics
    # -------------------------------

    original_rows = len(df)

    original_duplicates = df.duplicated().sum()

    original_missing = int(
        df.isnull().sum().sum()
    )

    # -------------------------------
    # Data Quality Check
    # -------------------------------

    st.subheader("🔍 Data Quality Check")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Rows",
            original_rows
        )

    with col2:
        st.metric(
            "Duplicate Rows",
            original_duplicates
        )

    with col3:
        st.metric(
            "Missing Values",
            original_missing
        )

    # -------------------------------
    # Create Cleaned Data
    # -------------------------------

    cleaned_df = df.copy()

    # -------------------------------
    # Convert Numeric Columns
    # -------------------------------

    numeric_columns = [
        "Customer_ID",
        "Quantity",
        "Price"
    ]

    for column in numeric_columns:

        if column in cleaned_df.columns:

            cleaned_df[column] = pd.to_numeric(
                cleaned_df[column],
                errors="coerce"
            )

    # -------------------------------
    # Fill Missing Values
    # -------------------------------

    for column in cleaned_df.columns:

        if pd.api.types.is_numeric_dtype(
            cleaned_df[column]
        ):

            median_value = cleaned_df[
                column
            ].median()

            cleaned_df[column] = cleaned_df[
                column
            ].fillna(median_value)

        else:

            cleaned_df[column] = cleaned_df[
                column
            ].fillna("Unknown")

    # -------------------------------
    # Remove Duplicates
    # -------------------------------

    cleaned_df = cleaned_df.drop_duplicates()

    # -------------------------------
    # Standardize Text
    # -------------------------------

    text_columns = cleaned_df.select_dtypes(
        include=["object"]
    ).columns

    for column in text_columns:

        cleaned_df[column] = (
            cleaned_df[column]
            .astype(str)
            .str.strip()
        )

    # -------------------------------
    # Standardize Customer Names
    # -------------------------------

    if "Customer_Name" in cleaned_df.columns:

        cleaned_df["Customer_Name"] = (
            cleaned_df["Customer_Name"]
            .str.title()
        )

    # -------------------------------
    # Standardize Cities
    # -------------------------------

    if "City" in cleaned_df.columns:

        cleaned_df["City"] = (
            cleaned_df["City"]
            .str.title()
        )

    # -------------------------------
    # Calculate Total Sales
    # -------------------------------

    if (
        "Quantity" in cleaned_df.columns
        and
        "Price" in cleaned_df.columns
    ):

        cleaned_df["Total_Sales"] = (
            cleaned_df["Quantity"]
            * cleaned_df["Price"]
        )

    # -------------------------------
    # Cleaning Summary
    # -------------------------------

    cleaned_rows = len(cleaned_df)

    st.subheader("🧹 Cleaning Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Original Rows",
            original_rows
        )

    with col2:
        st.metric(
            "Duplicates Removed",
            original_duplicates
        )

    with col3:
        st.metric(
            "Missing Values Found",
            original_missing
        )

    with col4:
        st.metric(
            "Rows After Cleaning",
            cleaned_rows
        )

    # -------------------------------
    # Cleaned Data
    # -------------------------------

    st.subheader("✨ Cleaned Data")

    st.dataframe(
        cleaned_df,
        use_container_width=True
    )

    # -------------------------------
    # Automated Report
    # -------------------------------

    st.subheader("📈 Automated Report")

    if "Total_Sales" in cleaned_df.columns:

        total_sales = cleaned_df[
            "Total_Sales"
        ].sum()

        average_sales = cleaned_df[
            "Total_Sales"
        ].mean()

        total_transactions = len(
            cleaned_df
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Sales",
                f"₹{total_sales:,.2f}"
            )

        with col2:
            st.metric(
                "Average Sale",
                f"₹{average_sales:,.2f}"
            )

        with col3:
            st.metric(
                "Total Transactions",
                total_transactions
            )

        # -------------------------------
        # Sales by City
        # -------------------------------

        if "City" in cleaned_df.columns:

            st.subheader("🏙️ Sales by City")

            city_sales = (
                cleaned_df
                .groupby("City")[
                    "Total_Sales"
                ]
                .sum()
            )

            fig, ax = plt.subplots()

            city_sales.plot(
                kind="bar",
                ax=ax
            )

            ax.set_xlabel("City")
            ax.set_ylabel("Total Sales")
            ax.set_title("Sales by City")

            plt.xticks(rotation=45)

            st.pyplot(fig)

            plt.close(fig)

        # -------------------------------
        # Sales by Product
        # -------------------------------

        if "Product" in cleaned_df.columns:

            st.subheader("🛍️ Sales by Product")

            product_sales = (
                cleaned_df
                .groupby("Product")[
                    "Total_Sales"
                ]
                .sum()
            )

            fig, ax = plt.subplots()

            product_sales.plot(
                kind="bar",
                ax=ax
            )

            ax.set_xlabel("Product")
            ax.set_ylabel("Total Sales")
            ax.set_title("Sales by Product")

            plt.xticks(rotation=45)

            st.pyplot(fig)

            plt.close(fig)

    # -------------------------------
    # Download CSV
    # -------------------------------

    st.subheader("⬇️ Download Reports")

    csv_data = cleaned_df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    # -------------------------------
    # Download Excel
    # -------------------------------

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        cleaned_df.to_excel(
            writer,
            index=False,
            sheet_name="Cleaned Data"
        )

    excel_buffer.seek(0)

    st.download_button(
        label="📊 Download Excel Report",
        data=excel_buffer,
        file_name="cleaned_data_report.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument"
            ".spreadsheetml.sheet"
        )
    )

    # -------------------------------
    # Success Message
    # -------------------------------

    st.success(
        "✅ Data cleaning and automated reporting completed!"
    )