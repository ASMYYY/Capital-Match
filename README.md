## Inspiration
Sales teams often face challenges when trying to connect with the right customers for the right products. The vast amount of data available about customer preferences, purchase history, and product interest can be overwhelming to sift through manually. Inspired by the potential to make sales campaigns more effective, “Capital Match” was designed to leverage customer profile data and product details to create hyper-personalized product recommendations. This solution empowers sales teams to engage their target audience with precision, boosting customer satisfaction, increasing conversion rates, and optimizing overall marketing efforts through targeted outreach.

## What it does
Capital Match is a smart recommendation service that analyzes customer profiles, including transaction patterns and preferences, alongside product data to generate personalized recommendations. It helps sales teams identify valuable prospects and automatically drafts tailored emails summarizing recommended products and their benefits. This boosts communication efficiency and increases conversion potential through thoughtful, personalized messaging.

## How we built it
Capital Match leverages **Retrieval-Augmented Generation (RAG)** with a vector database and the Llama3 API. We transformed customer profiles into embeddings using **BAAI’s bge-small-en embedding model** and stored them in a vector database. When queried, it identifies customer behavior patterns and maps them to relevant product recommendations. Using this data, hyper-personalized emails are generated with Llama3.

We utilized **LangChain** to streamline the process of prompting and creating sequential chains, enhancing the flow and interaction between various AI models. The system features a **Streamlit dashboard** for a user-friendly interface, while **FastAPI** manages data requests and communications, ensuring smooth and efficient operations. This approach delivers precise, impactful customer targeting for sales teams. 

### 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```commandline
    pip install -r requirements.txt
   ```

2. Run the API
    ```commandline
     uvicorn app:app
   ```

3. Run the app

   ```commandline
    streamlit run streamlit_app.py
   ```


## Challenges we ran into
It was difficult to find open-source customer profile data that accurately represents real-world user behavior patterns. To overcome this, we created our own synthetic data that closely mimics real-world user behaviors and interactions, enhancing the model's training and performance.

## Accomplishments that we're proud of
- Successfully built and deployed a fully functional recommendation engine tailored for the needs of sales teams, capable of hyper-personalization.
- Developed a sophisticated email drafting tool that automates the creation of compelling, highly relevant messages.
- Created a user-friendly dashboard to help sales teams easily manage and understand their customer recommendations and communications.

## What we learned
- The power of hyper-personalization in modern sales strategies and its potential to drastically improve customer engagement and sales outcomes.
- How to balance automation and personalization when crafting emails to avoid making them appear overly generic.

## What's next for Capital Match
- **Advanced Predictive Analytics:** Incorporating predictive models that anticipate customers' future needs or desires based on evolving data trends.
- **Multi-Channel Integration:** Extending personalized recommendations and messaging capabilities beyond emails to include SMS, chat, and social media campaigns.
- **Integration with CRM Platforms:** Seamless integration with popular CRM tools to make accessing customer data and insights even more convenient.
