# DATA.DOX — Smart Data Analysis Dashboard
A Streamlit-based interactive dashboard for end-to-end data analysis — upload a CSV, clean it, engineer features, and visualise insights, all without writing a single line of code.


# Prerequisites
-Make sure you have Python 3.8+ installed, then install the dependencies:  
-bash-pip install streamlit pandas numpy matplotlib scipy scikit-learn  
-Run the App  
-bash-python -m streamlit run main.py  

# Features
##1.  Upload Dataset

-Upload any CSV file via the sidebar
-Supports files with mixed numeric and categorical columns

##2.  About Dataset
-Instant dataset overview including:

###Random 6-row sample
-Total row count
-DataFrame info (dtypes, non-null counts)
-Missing values count and percentage per column
-Outlier count per numeric column (IQR method)
-Full statistical summary

##3.Data Cleaning
-Choose one cleaning method and apply it:
-Drop ColumnDrops :columns where missing % exceeds a slider threshold
-Fill NA with Mean:Fills numeric NaNs with column mean
-Fill NA with Mode:Fills all NaNs with the most frequent value
-Outlier Clearance:Cap FillingClips outliers to IQR bounds (Winsorization)
-Outlier Clearance:Z-ScoreRemoves rows where any numeric column has |z| > 3

##4. Data Visualisation
-Interactive charts built with Matplotlib:
-ChartWhat it shows:
-Bar Graph:Mean of a numeric column grouped by a categorical column
-Line Chart:Trend of a numeric column over another column; supports aggregation toggle
-Histogram:Distribution of any numeric column with adjustable bin count
-Pie Chart:Value counts of any categorical column

##5. Feature Engineering
-Transform columns and add them to your dataset:
-Age Group (Binning) Numeric  Teen / Young / Adult / Senior / Elder
-Log Transform Numeric log1p of the column
-Min-Max Scaling Numeric Values scaled to [0, 1]
-Standard Scaling Numeric Zero mean, unit variance
-Label Encoding Categorical Integer-encoded labels

-Engineered dataset can be downloaded as CSV.

##6.  Add Derived Column
-Create a new column by combining two existing numeric columns with:

-Addition, Subtraction, Multiplication, or Division
-Custom name for the new column
-Result downloadable as CSV

<img width="1469" height="789" alt="Screenshot 2026-05-28 111559" src="https://github.com/user-attachments/assets/d7c63fc7-535a-414e-8722-6dee1df618b9" />
