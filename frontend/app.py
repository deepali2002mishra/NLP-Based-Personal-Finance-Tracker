import streamlit as st
import requests

# Streamlit page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="centered",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Center-align the title */
    .css-10trblm.e16nr0p34 {
        text-align: center;
    }
    body {
        zoom: 0.9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.title("Personal Finance Tracker 💰")

# File Upload Section
st.header("Upload Bank Statement PDF")
uploaded_file = st.file_uploader(
    "Drag and drop your bank statement PDF here", type=["pdf"], help="Limit 200MB per file."
)

if uploaded_file:
    st.write(f"📄 **Uploaded File:** {uploaded_file.name}")
    # Save the uploaded file temporarily for sending to the backend
    with open(f"temp_{uploaded_file.name}", "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())

    # Send the file to the backend for processing
    try:
        with open(f"temp_{uploaded_file.name}", "rb") as temp_file:
            response = requests.post("http://127.0.0.1:5000/upload", files={"file": temp_file})

        if response.status_code == 200:
            data = response.json()

            # Spending Analysis Section
            st.header("📊 Spending Analysis")

            # Display category totals
            if "category_totals" in data["analysis"]:
                st.subheader("Category Totals:")
                for category, amount in data["analysis"]["category_totals"].items():
                    st.write(f"- **{category}:** ₹{amount:,.2f}")
            else:
                st.error("No category totals available.")

            # Display key insights
            st.subheader("Key Insights:")
            total_spending = data["analysis"].get("total_spending", "N/A")
            average_spending = data["analysis"].get("average_spending", "N/A")
            highest_transaction = data["analysis"].get("highest_transaction", {})

            st.write(f"**Total Spending:** ₹{total_spending:,.2f}")
            st.write(f"**Average Spending:** ₹{average_spending:,.2f}")
            if highest_transaction:
                st.write("**Highest Transaction:**")
                st.write(f"- **Amount:** ₹{highest_transaction['Amount']:,.2f}")
                st.write(f"- **Category:** {highest_transaction['Category']}")
                st.write(f"- **Date:** {highest_transaction['Date']}")
                st.write(f"- **Description:** {highest_transaction['Description']}")

            # Display monthly breakdown
            st.subheader("Monthly Spending Breakdown:")
            if "monthly_breakdown" in data["analysis"]:
                for month, amount in data["analysis"]["monthly_breakdown"].items():
                    st.write(f"- **{month}:** ₹{amount:,.2f}")
            else:
                st.error("No monthly breakdown available.")

            # Display Charts
            st.header("📈 Charts")
            if "bar_chart" in data["charts"]:
                st.image(f"http://127.0.0.1:5000{data['charts']['bar_chart']}", caption="Bar Chart")
            else:
                st.error("Bar chart not available.")

            if "line_chart" in data["charts"]:
                st.image(f"http://127.0.0.1:5000{data['charts']['line_chart']}", caption="Line Chart")
            else:
                st.error("Line chart not available.")
        else:
            st.error(f"Failed to process file: {response.json().get('error', 'Unknown error')}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        💡 Powered by Personal Finance Tracker | © 2024
    </div>
    """,
    unsafe_allow_html=True,
)
