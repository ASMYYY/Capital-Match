import streamlit as st
import pandas as pd
import requests
import json

# Load customer data from JSON in the 'data' folder
data_path = './data/customer_profile.json'

try:
    with open(data_path, 'r') as f:
        customers = json.load(f)
    df = pd.DataFrame(customers)
except FileNotFoundError:
    st.error(f"The file '{data_path}' was not found. Please check the file path and try again.")
    st.stop()
except json.JSONDecodeError:
    st.error(f"The file '{data_path}' is not a valid JSON file. Please check the file contents.")
    st.stop()


# Function to get customer details
def get_customer_details(customer_id):
    customer_row = df[df['CustomerID'] == customer_id]
    if customer_row.empty:
        return None
    return customer_row.iloc[0]


# Function to call the recommendation API
def get_recommendations(customer_id):
    url = "http://127.0.0.1:8000/product/recommend"
    headers = {"Content-Type": "application/json"}
    data = {"candidate_id": customer_id}
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # response = response.json()
            response = response.json().get("recommendation", "")
            # response.replace("*", "")
            # return response.json().get("recommendation", [])
            if isinstance(response, str):
                print(response, "???????")
                return response
            else:
                st.error("Invalid recommendation format received.")
                return ""
        else:
            st.error("Failed to fetch recommendations. Please try again later.")
            return []
    except requests.exceptions.RequestException as e:
        st.error("Error connecting to the recommendation service.")
        return []


# Streamlit App
def main():
    st.set_page_config(page_title="Capital Match", layout="centered")
    st.markdown(
        """
        <style>
            .main-title { font-size: 42px; color: #2A9D8F; text-align: center; }
            .sub-title { font-size: 24px; color: #264653; text-align: center; }
            .footer { font-size: 14px; color: #A8DADC; text-align: center; }
            .customer-details, .products { background-color: #F1FAEE; padding: 15px; border-radius: 8px; }
        </style>
        """, unsafe_allow_html=True
    )

    # Title and description
    st.markdown("<div class='main-title'>Capital Match</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Personalized Product Recommendations for Customers</div>",
                unsafe_allow_html=True)

    # Search box and button
    customer_id = st.text_input("Enter Customer ID", placeholder="e.g., AlisonGaines78")
    search_clicked = st.button("🔍 Search")

    if search_clicked:
        if customer_id:
            customer_details = get_customer_details(customer_id)

            if customer_details is not None:
                # Display customer information
                st.markdown("<div class='customer-details'>", unsafe_allow_html=True)
                st.write("### Customer Details")
                st.write(f"**ID**: {customer_details['CustomerID']}")
                st.write(f"**Name**: {customer_details['FirstName']} {customer_details['LastName']}")
                st.write(f"**Contact**: {customer_details['Phone']}")
                st.write(f"**Email**: {customer_details['Email']}")
                st.markdown("</div>", unsafe_allow_html=True)

                # Display existing products
                st.markdown("<div class='products'>", unsafe_allow_html=True)
                st.write("### Existing Products")
                existing_products = [product for product, status in customer_details.items() if
                                     status == "Yes" and product not in ['CustomerID', 'FirstName', 'LastName']]
                st.write(", ".join(existing_products) if existing_products else "No products yet.")
                st.markdown("</div>", unsafe_allow_html=True)

                # Fetch and display recommended products via API call
                st.markdown("<div class='products'>", unsafe_allow_html=True)
                st.write("### Recommended Products")
                recommended_products = get_recommendations(customer_id)
                st.write(recommended_products if recommended_products else "No recommendations available.")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Customer not found. Please try again.")
        else:
            st.warning("Please enter a Customer ID to search.")

    st.markdown("<div class='footer'>© 2023 Capital One | Empowered by AI-Driven Insights</div>",
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
