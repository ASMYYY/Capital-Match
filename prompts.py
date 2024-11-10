prompt1 = """
You are a professional data analyst and product recommender at a bank. You have been provided with detailed customer information.
Analyze the following customer data and provide insights into their financial needs, potential risks, and opportunities for product offerings.
Keep the analysis short, to the point and very concise, but easy to understand.
Customer Information: {query}
"""

prompt2= """
As a professional financial advisor at a bank, your goal is to provide tailored recommendations that align with the customer's financial situation and goals.
Using the customer analysis provided and the available banking products, determine the most suitable product(s) for this customer.
Please explain why this product is the best fit in short, considering the customer's financial needs, potential risks, and long-term benefits.
Keep the the analysis, reasoning and recommendation short, to the point and very concise. The entire answer should be max 3 lines, not more than 3.
Customer Analysis: {customer_analysis}
Available Products: {product_info}
Recommendation:
"""

mail_prompt = """
Based in the product recommendation and the benefits of the product draft a short email. Add the signature as Capital One
Recommendation: {product_recommendation}
Mail:
"""

sample_reco = {"recommendation": "Based on Alison's financial needs and profile, I recommend the Visa Gold credit card and a High-Yield Savings Account. The Visa est rates, addressing her need for efficient cash management and investment opportunities."}
