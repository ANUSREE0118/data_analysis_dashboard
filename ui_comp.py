import streamlit as st

def load_global_css():
    st.markdown("""
    <style>
    .dashboard-row {
        display: flex;
        gap: 20px;
        margin: 25px 0;
    }
    .dashboard-card {
        flex: 1;
        padding: 22px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 6px 14px rgba(0,0,0,0.15);
    }
    .card-title {
        font-size: 15px;
        opacity: 0.9;
    }
    .card-value {
        font-size: 30px;
        font-weight: bold;
    }
    .blue { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .orange { background: linear-gradient(135deg, #ff9a44, #ff6a00); }
    .purple { background: linear-gradient(135deg, #7B2FB9, #9B59B6); }
    </style>
    """, unsafe_allow_html=True)


def dashboard_cards(total_rows, missing_pct):
    st.markdown(f"""
    <div class="dashboard-row">
        <div class="dashboard-card blue">
            <div class="card-title">Total Rows</div>
            <div class="card-value">{total_rows}</div>
        </div>

        <div class="dashboard-card orange">
            <div class="card-title">Missing Values (%)</div>
            <div class="card-value">{missing_pct:.2f}%</div>
        </div>

        <div class="dashboard-card purple">
            <div class="card-title">Outliers</div>
            <div class="card-value">--</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    import streamlit as st

def load_global_css():
    st.markdown("""
    <style>
    .dashboard-row {
        display: flex;
        gap: 20px;
        margin: 25px 0;
    }
    .dashboard-card {
        flex: 1;
        padding: 22px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 6px 14px rgba(0,0,0,0.15);
    }
    .card-title {
        font-size: 15px;
        opacity: 0.9;
    }
    .card-value {
        font-size: 30px;
        font-weight: bold;
    }
    .blue { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .orange { background: linear-gradient(135deg, #ff9a44, #ff6a00); }
    .purple { background: linear-gradient(135deg, #7B2FB9, #9B59B6); }
    .green { background: linear-gradient(135deg, #00c853, #b2ff59); } /* New color for outlier */
    </style>
    """, unsafe_allow_html=True)


def dashboard_cards(total_rows, missing_pct, outlier_count):
    st.markdown(f"""
    <div class="dashboard-row">
        <div class="dashboard-card blue">
            <div class="card-title">Total Rows</div>
            <div class="card-value">{total_rows}</div>
        </div>

        <div class="dashboard-card orange">
            <div class="card-title">Missing Values (%)</div>
            <div class="card-value">{missing_pct:.2f}%</div>
        </div>

        <div class="dashboard-card purple">
            <div class="card-title">Outliers Detected</div>
            <div class="card-value">{outlier_count}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

