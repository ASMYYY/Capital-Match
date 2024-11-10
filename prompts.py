prompt1 = """
You are a professional data analyst and product recommender at a bank. You have been provided with detailed customer information.
Analyze the following customer data and provide insights into their financial needs, potential risks, and opportunities for product offerings.
Customer Information: {query}
"""

prompt2= """
As a professional financial advisor at a bank, your goal is to provide tailored recommendations that align with the customer's financial situation and goals.
Using the customer analysis provided and the available banking products, determine the most suitable product(s) for this customer.
Please explain why this product is the best fit, considering the customer's financial needs, potential risks, and long-term benefits.
Customer Analysis: {customer_analysis}
Available Products: {product_info}
Recommendation:
"""