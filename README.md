# VolumeSignal - Manufacturing Client Acquisition Dashboard

This is a Streamlit application designed to identify manufacturing companies in Singapore and Malaysia that are likely increasing their production volume. It uses public hiring signals to score and rank potential client leads.

## Features

-   **VolumeSignal Leads**: A dashboard to view and filter potential leads based on hiring data.
-   **Client Volume Tracker**: Tracks the top clients of target manufacturers to identify downstream growth.
-   **Market Intelligence**: A feed of the latest signals on packaging materials, sales volumes, and production growth.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root of the project by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Then, edit the `.env` file and add your Gemini API key:
    ```
    GEMINI_API_KEY="your_actual_api_key"
    ```

## How to Run

Once the setup is complete, run the Streamlit app with the following command:

```bash
streamlit run app.py
```