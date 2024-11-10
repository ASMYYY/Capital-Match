import streamlit as st
import pandas as pd
import requests
import json
import base64
from PIL import Image
from pathlib import Path

from app import recommendations

image = Image.open('image1.jpg')
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

# def img_to_bytes(img_path):
#     img_bytes = Path(img_path).read_bytes()
#     encoded = base64.b64encode(img_bytes).decode()
#     return encoded
# def img_to_html(img_path):
#     img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
#       img_to_bytes(img_path)
#     )
#     return img_html

def encode_logo() -> str:
    with open("image1.jpg", "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()
        return encoded_img

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
            response = response.json().get("recommendation", "")
            if isinstance(response, str):
                return response
            else:
                st.error("Invalid recommendation format received.")
                return ""
        else:
            st.error("Failed to fetch recommendations. Please try again later.")
            return []
    except requests.exceptions.RequestException:
        st.error("Error connecting to the recommendation service.")
        return []

def get_email_content(recommendation):
    print("INside email content api!")
    url = "http://127.0.0.1:8000/product/mail-content"
    headers = {"Content-Type": "application/json"}
    data = {"product_recommendation": recommendation}
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response = response.json().get("mail", "")
            if isinstance(response, str):
                return response
            else:
                st.error("Invalid mail format received.")
                return ""
        else:
            st.error("Failed to fetch mail. Please try again later.")
            return []
    except requests.exceptions.RequestException:
        st.error("Error connecting to the mail service.")
        return []

# Streamlit App
def main():
    st.set_page_config(
        page_title="Capital Match",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Enhanced CSS with soft, pleasing aesthetics
    st.markdown(
        """
        <style>
            /* Global styles */
            .main {
                background-color: #FFFFFF;
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }

            /* Typography */
            .main-title {
                font-size: 2.8rem;
                background: linear-gradient(45deg, #004977, #006090);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                font-weight: 800;
                margin: 1.5rem 0;
                font-family: 'Helvetica Neue', sans-serif;
                letter-spacing: -0.5px;
            }

            .sub-title {
                font-size: 1.3rem;
                color: #D03027;
                text-align: center;
                margin-bottom: 2.5rem;
                font-family: 'Helvetica Neue', sans-serif;
                font-weight: 500;
                opacity: 0.9;
            }

            /* Content sections */
            .content-section {
                background-color: #FFFFFF;
                padding: 0rem;
                margin: 0rem 0;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease;
            }

            .content-section:hover {
                transform: translateY(-2px);
            }

            /* Button styling */
            .stButton>button {
                background: linear-gradient(45deg, #004977, #006090);
                color: white;
                padding: 0.8rem 1.5rem;
                border-radius: 8px;
                border: none;
                font-weight: 600;
                width: 100%;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-size: 0.9rem;
            }

            .stButton>button:hover {
                background: linear-gradient(45deg, #006090, #004977);
                box-shadow: 0 4px 12px rgba(0, 73, 119, 0.2);
            }

            /* Input field styling */
            .stTextInput>div>div>input {
                border-radius: 8px;
                border: 2px solid #E5E7EB;
                padding: 0.8rem;
                font-size: 1rem;
                transition: all 0.3s ease;
            }

            .stTextInput>div>div>input:focus {
                border-color: #004977;
                box-shadow: 0 0 0 2px rgba(0, 73, 119, 0.1);
            }

            /* Section headers */
            h3 {
                color: #004977;
                font-size: 1.4rem;
                font-weight: 700;
                margin-bottom: 1.2rem;
                letter-spacing: -0.3px;
            }

            /* Logo styling */
            .logo-container {
                text-align: center;
                margin: 2rem 0;
            }

            .logo-container img {
                width: 100px;
                height: 100px;
                object-fit: cover;
                border-radius: 50%;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                margin: 0 auto;
                display: block;
            }

            /* Product tags */
            .product-tag {
                display: inline-block;
                background: linear-gradient(45deg, #f0f4f8, #e1e8f0);
                color: #004977;
                padding: 0.6rem 1.2rem;
                border-radius: 25px;
                margin: 0.4rem;
                font-size: 0.9rem;
                font-weight: 500;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }

            /* Customer details styling */
            .customer-detail {
                padding: 0.5rem 0;
                color: #2d3748;
                font-size: 1rem;
            }

            .customer-detail strong {
                color: #004977;
                font-weight: 600;
            }

            /* Footer styling */
            .footer {
                font-size: 0.9rem;
                color: #718096;
                text-align: center;
                margin-top: 4rem;
                padding-top: 2rem;
                font-weight: 500;
            }

            /* Error and warning messages */
            .stAlert {
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Logo and titles
    encoded_img = encode_logo()
    imgr = f"""<div> <img
    src = "data:image/png;base64,{encoded_img}"
    alt = "image1"
    class="logo" height="100px" border-top-left-radius="14px"/>
    </div>"""
    # st.markdown()
    col1, col2, col3 = st.columns([0.5, 0.5, 0.2])
    with col2:
        st.markdown(imgr, unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>Capital Match</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>AI-Driven Recommendations for Capital One Front Office Teams</p>",
                unsafe_allow_html=True)

    # Search interface
    customer_id = st.text_input("Enter Customer ID", placeholder="e.g., AlisonGaines78")
    search_clicked = st.button("🔍 Search Customer")

    if search_clicked:
        if customer_id:
            customer_details = get_customer_details(customer_id)

            if customer_details is not None:
                # Customer Details Section
                st.markdown("<div class='content-section'>", unsafe_allow_html=True)
                st.markdown("<h3>Customer Details</h3>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        f"<div class='customer-detail'><strong>ID:</strong> {customer_details['CustomerID']}</div>",
                        unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='customer-detail'><strong>Name:</strong> {customer_details['FirstName']} {customer_details['LastName']}</div>",
                        unsafe_allow_html=True)
                with col2:
                    st.markdown(
                        f"<div class='customer-detail'><strong>Contact:</strong> {customer_details['Phone']}</div>",
                        unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='customer-detail'><strong>Email:</strong> {customer_details['Email']}</div>",
                        unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Existing Products Section
                st.markdown("<div class='content-section'>", unsafe_allow_html=True)
                st.markdown("<h3>Existing Products</h3>", unsafe_allow_html=True)
                existing_products = [product for product, status in customer_details.items()
                                     if
                                     status == "Yes" and product not in ['CustomerID', 'FirstName', 'LastName', 'Phone',
                                                                         'Email']]
                if existing_products:
                    for product in existing_products:
                        st.markdown(f"<span class='product-tag'>{product}</span>", unsafe_allow_html=True)
                else:
                    st.write("No products yet.")
                st.markdown("</div>", unsafe_allow_html=True)

                # Recommendations Section
                st.markdown("<div class='content-section'>", unsafe_allow_html=True)
                st.markdown("<h3>Recommended Products</h3>", unsafe_allow_html=True)
                recommended_products = get_recommendations(customer_id)
                st.write(recommended_products if recommended_products else "No recommendations available.")
                st.markdown("</div>", unsafe_allow_html=True)

                email_clicked = st.button("📧 Send Email")
                if email_clicked:
                    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
                    st.markdown("<h3>Email Draft</h3>", unsafe_allow_html=True)
                    mail_content = get_email_content(recommended_products)
                    st.write(mail_content if mail_content else "No content available.")
                    st.markdown("</div>", unsafe_allow_html=True)


            else:
                st.error("Customer not found. Please try again.")
        else:
            st.warning("Please enter a Customer ID to search.")

    # Footer
    st.markdown("<div class='footer'>© 2023 Capital One | Empowered by AI-Driven Insights</div>",
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()