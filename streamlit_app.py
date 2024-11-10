import streamlit as st
import pandas as pd
from io import BytesIO

# Load your customer data
data_path = './CapitalOneSampleData.xlsx'
df = pd.read_excel(data_path)


# Function to download the recommendations as Excel
def download_recommendations(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Recommendations')
    writer.save()
    output.seek(0)
    return output


# Function to get customer details
def get_customer_details(customer_id):
    customer_row = df[df['Customer ID'] == customer_id]
    if customer_row.empty:
        return None
    return customer_row.iloc[0]


# Streamlit App
def main():
    # Set page config and background color
    st.set_page_config(page_title="Capital Match", layout="centered")
    st.markdown(
        """
        <style>
            .stButton>button {
                width: 100%;
                padding: 10px;
                font-size: 16px;
            }
            .main-title {
                font-size: 42px;
                color: #2A9D8F;
                text-align: center;
            }
            .sub-title {
                font-size: 24px;
                color: #264653;
                text-align: center;
            }
            .footer {
                font-size: 14px;
                color: #A8DADC;
                text-align: center;
            }
            .customer-details, .products {
                background-color: #F1FAEE;
                padding: 15px;
                border-radius: 8px;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Page 1: Main Page with Search and Download Options
    if "page" not in st.session_state:
        st.session_state.page = 1

    if st.session_state.page == 1:
        st.markdown("<div class='main-title'>Capital Match</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Personalized Product Recommendations for Customers</div>",
                    unsafe_allow_html=True)
        st.markdown("####")

        # Search button
        if st.button("🔍 Search by Customer"):
            st.session_state.page = 2

        st.markdown("---")

        # Download button
        st.write("Get a comprehensive list of all recommendations:")
        if st.button("⬇️ Download Recommendation List for All Customers"):
            recommendations = download_recommendations(df)
            st.download_button(
                label="Download Recommendations",
                data=recommendations,
                file_name="recommendations.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Footer
        st.markdown("<div class='footer'>© 2023 Capital One | Empowered by AI-Driven Insights</div>",
                    unsafe_allow_html=True)

    # Page 2: Customer Search Page
    elif st.session_state.page == 2:
        st.markdown("<div class='main-title'>Capital Match</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Customer Product Recommendations</div>", unsafe_allow_html=True)

        # Search input for Customer ID or Name
        customer_id = st.text_input("Enter Customer ID or Name", placeholder="e.g., 12345 or John Doe")

        if customer_id:
            customer_details = get_customer_details(customer_id)

            if customer_details is not None:
                # Display customer information
                st.markdown("<div class='customer-details'>", unsafe_allow_html=True)
                st.write("### Customer Details")
                st.write(f"**ID**: {customer_details['Customer ID']}")
                st.write(f"**Name**: {customer_details['Customer Name']}")
                st.write(f"**Contact**: {customer_details['Zip Code']}")
                st.write(
                    f"**Email**: {customer_details['Customer Name'].replace(' ', '').lower()}@example.com")  # Placeholder email
                st.markdown("</div>", unsafe_allow_html=True)

                # Display existing products
                st.markdown("<div class='products'>", unsafe_allow_html=True)
                st.write("### Existing Products")
                existing_products = [col for col in df.columns[6:] if customer_details[col] == "Yes"]
                if existing_products:
                    st.write(", ".join(existing_products))
                else:
                    st.write("No products yet.")
                st.markdown("</div>", unsafe_allow_html=True)

                # Display predicted products (placeholder)
                st.markdown("<div class='products'>", unsafe_allow_html=True)
                st.write("### Predicted Products")
                st.write("Personal Loan, Auto Loan, Cash Back Credit Card")  # Placeholder predictions
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Customer not found. Please try again.")

        # Back button to go to Page 1
        st.markdown("####")
        if st.button("⬅️ Back to Main Page"):
            st.session_state.page = 1

        # Footer
        st.markdown("<div class='footer'>© 2023 Capital One | Empowered by AI-Driven Insights</div>",
                    unsafe_allow_html=True)


if __name__ == "__main__":
    main()
