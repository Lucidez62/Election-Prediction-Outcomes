import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

# --- Page Configuration ---
# Set the page to a wide layout for better dashboarding
st.set_page_config(
    page_title="Election EDA & Insights Dashboard",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Main Dashboard ---
st.title("🗳️ Indian Assembly Elections: Full Project Dashboard")
st.markdown("This interactive dashboard displays the full project: EDA, Political Insights, and ML Model Results.")

# --- Tab-Based Interface (NOW WITH 5 TABS) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analysis - 1", 
    "📈 Analysis - 2", 
    "🌍 Analysis - 3",
    "🔍 Political Insights",
    "🤖 ML Model Comparison" # <-- NEW TAB
])

# =====================================================================================
# ===                             TAB 1: UNIVARIATE                                 ===
# =====================================================================================

with tab1:
    st.header("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution of Candidate Sex")
        st.image("uni1.png", caption="Distribution of Candidate Sex")
        
        st.subheader("Distribution of Candidate Age")
        st.image("uni2.png", caption="Distribution of Candidate Age")
        
        st.subheader("Top 15 Parties by Candidate Count")
        st.image("uni3.png", caption="Top 15 Parties by Candidate Count")
        
    with col2:
        st.subheader("Winning Margin %")
        st.image("uni4.png", caption="Winning Margin")

        st.subheader("Voter Turnout %")
        st.image("uni5.png", caption="Voter Turnout")
        
        st.subheader("Distribution of Winning Margin")
        st.image("uni6.png", caption="Winning Margin %")

    st.divider()
    
    st.subheader("Top 15 states by Number of Female Candidates Winning Elections(2009-2021)")
    st.image("uni7.png", caption="Total Number of Female Winners")
    
# =====================================================================================
# ===                             TAB 2: BIVARIATE                                  ===
# =====================================================================================

with tab2:
    st.header("")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Vote Share Percentage Distribution for Major Parties")
        st.image("bi1.png", caption="Party-Wise")
        
        st.subheader("Top 15 parties by Strike Rate")
        st.image("bi3.png", caption="Party-Wise")
        
        st.subheader("Candidates Contesting Over the Years")
        st.image("bi4.png", caption="For each year")

    with col2:
        st.subheader("Total Electors vs. Election Outcome")
        st.image("bi5.png", caption="Total Electors vs. Election Outcome")
        
        st.subheader("Age Distribution of Candidates for Major Parties")
        st.image("bi7.png", caption="For Every Party")
        
        st.subheader("Density of Wins in Indian States for BJP")
        st.image("bi8.png", caption="BJP Win Rate")


# =====================================================================================
# ===                            TAB 3: MULTIVARIATE                              ===
# =====================================================================================

with tab3:
    st.header("")

    st.subheader("Retention Rate")
    st.image("mul1.png", caption="Correlation Matrix of Key Features")
    with st.expander("Insights"):
        st.markdown("Shows the linear relationships between numerical features. There are no strong correlations between predictors, which is good for many ML models. `result` is weakly negatively correlated with `ac_total_candidates` (-0.23).")

    st.divider()

# =====================================================================================
# ===                         TAB 4: POLITICAL INSIGHTS                             ===
# =====================================================================================

with tab4:
    st.header("🔍 Candidate Party-Hopping Analysis")
    st.markdown("This section visualizes the flow of candidates between the Top 5 political parties for a selected state.")
    st.markdown("*(Note: 'IND' candidates are excluded from this analysis)*")
    
    # --- 1. Create a dictionary to map state names to your Sankey images ---
    sankey_plots = {
        "Maharashtra": "mah.png",
        "Karnataka": "karnataka.png",
        "Madhya Pradesh": "mp.png",
        "Kerala": "kerala.png",
        "Jharkhand": "jrk.png",
        "Odisha": "odisha.png",
        "Nagaland": "nagaland.png",
        "Mizoram": "mizoram.png",
        "Meghalaya": "meghalaya.png",
        "Manipur": "manipur.png"
        # Add any other states and their filenames here
        # "Uttar Pradesh": "up.png", 
        # "West Bengal": "wb.png",
    }
    
    # --- 2. Create the dropdown menu ---
    state_options = list(sankey_plots.keys())
    selected_state = st.selectbox(
        "**Select a State to Analyze:**",
        state_options,
        index=0 # Defaults to the first state in the list (Maharashtra)
    )
    
    # --- 3. Get the filename for the selected state ---
    image_filename = sankey_plots[selected_state]
    
    # --- 4. Display the selected image ---
    st.markdown(f"---")
    st.markdown(f"### Visualizing Candidate Flow for: **{selected_state}**")
    
    try:
        st.image(image_filename, caption=f"Sankey Chart for {selected_state}")
    except FileNotFoundError:
        st.error(f"Error: The file '{image_filename}' was not found. Please make sure it is in the same folder as app.py.")

    
    # --- 5. Insights Section ---
    st.subheader("How to Read This Chart & Key Conclusions")
    with st.expander("Click here for insights and analysis", expanded=True):
        st.markdown("""
        This Sankey chart visualizes the movement of political candidates *between* different parties over time.

        **Filters Applied (in the notebook):**
        1.  **Independents Excluded:** All 'IND' candidates are removed from this analysis.
        2.  **Top 5 Parties:** It *only* tracks movement to and from the Top 5 most active parties in the *selected state*.

        **How to Read It:**
        * **Timeframe:** This chart is **cumulative** (all years, 2009-2021).
        * **Left Column (Source):** The party a candidate contested for in one election.
        * **Right Column (Target):** The *different* party the *same candidate* contested for in a *subsequent* election.
        * **Flow Thickness:** Proportional to the **total number of candidates** who made that switch.
        
        **Key Conclusions & What to Look For:**
        * **High-Flow States (e.g., Maharashtra, Karnataka):** A chart with many thick, crossing flows indicates a **volatile and fluid political landscape**.
        * **Low-Flow States (e.g., Mizoram, Nagaland):** A chart with very few, thin flows suggests **high party loyalty** and a rigid political structure.
        * **Asymmetrical Flow (A "Poaching" Signal):** Look for "one-way streets." If you see a large flow from Party A to Party B, but *no* flow from B back to A, it can signal a major power shift.
        """)

# =====================================================================================
# ===                         [NEW] TAB 5: ML MODEL COMPARISON                      ===
# =====================================================================================

with tab5:
    st.header("🤖 Machine Learning Model Comparison")
    st.markdown("This tab displays the performance metrics for various classification models trained on the dataset.")

    # --- 1. Define the Model Data ---
    # (I have parsed this from the text you provided)
    model_data = {
        'Model': ['Random Forest', 'CatBoost', 'XGBoost', 'LightGBM', 'Logistic Regression'],
        'Accuracy': [0.922179, 0.914412, 0.911089, 0.901265, 0.900902],
        'Precision': [0.912666, 0.910601, 0.909318, 0.907719, 0.824285],
        'Recall': [0.922179, 0.922179, 0.921089, 0.921265, 0.907902],
        'F1 Score': [0.915575, 0.912991, 0.912005, 0.908404, 0.864075]
    }
    df_models = pd.DataFrame(model_data)

    # --- 2. Display the Styled DataFrame ---
    st.subheader("Model Performance Metrics")
    
    # --- [FIXED CODE] ---
    # Apply formatting *only* to the numerical columns
    format_dict = {
        'Accuracy': '{:.6f}',
        'Precision': '{:.6f}',
        'Recall': '{:.6f}',
        'F1 Score': '{:.6f}'
    }
    
    st.dataframe(
        df_models.style.highlight_max(
            color='lightgreen', 
            axis=0, 
            subset=['Accuracy', 'F1 Score', 'Precision', 'Recall']
        ).format(format_dict), # Use the format dictionary
        use_container_width=True
    )
    # --- [END FIXED CODE] ---
    
    # --- 3. Display the Bar Chart ---
    st.subheader("Visual Comparison (F1 Score)")
    st.markdown("F1 Score is a key metric for an imbalanced dataset as it balances Precision and Recall.")
    
    fig_ml = px.bar(
        df_models.sort_values(by='F1 Score', ascending=False), 
        x='Model', 
        y='F1 Score', 
        title='Model Comparison by F1 Score', 
        color='Model',
        text_auto='.4f' # Show 4 decimal places on the bars
    )
    fig_ml.update_layout(yaxis_title="F1 Score (Higher is Better)")
    st.plotly_chart(fig_ml, use_container_width=True)
    
    # --- 4. Display the Logistic Regression Image ---
    st.divider()
    st.subheader("Baseline Model Analysis (Logistic Regression)")
    
    try:
        st.image("logistic.png", caption="Analysis of the Logistic Regression model (e.g., Confusion Matrix)")
    except FileNotFoundError:
        st.error("Error: 'logistic.png' not found. Please add it to the folder.")

    # --- 5. Insights Section ---
    st.subheader("Key Conclusions from ML Modeling")
    with st.expander("Click here for model insights", expanded=True):
        st.markdown("""
        * **Top Performer:** The **Random Forest** model achieved the highest F1 Score (0.9156) and Precision (0.9127), making it the best-performing model for this task. It also tied for the highest Accuracy.
        * **Strong Contenders:** CatBoost, XGBoost, and LightGBM (all gradient-boosted tree models) performed exceptionally well and were very close to the Random Forest.
        * **Baseline Model:** The **Logistic Regression** model served as a strong baseline, but its F1 Score (0.8641) and Precision (0.8243) were significantly lower than the tree-based ensemble models. This indicates that the relationships between the features and the election outcome are complex and non-linear, which the tree models are better at capturing.
        * **Overall Conclusion:** The high scores (F1 > 0.91) from the top models suggest that election outcomes are **highly predictable** given the features in this dataset.
        """)