import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt 
import numpy as np
from scipy.stats import zscore

from sklearn.preprocessing import MinMaxScaler,StandardScaler,LabelEncoder

if "derived_df" not in st.session_state:
    st.session_state.derived_df = None




if "cleaned_dfs" not in st.session_state:
    st.session_state.cleaned_dfs = None



#python -m streamlit run main.py

if "show_chart" not in st.session_state:
    st.session_state.show_chart=False



if "show_cleaning" not in st.session_state:
    st.session_state.show_cleaning = False

if "apply_cleaning" not in st.session_state:
    st.session_state.apply_cleaning = False
    
    
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df=False  



if "apply_fe" not in st.session_state:
    st.session_state.apply_fe=False
    

if "show_fe" not in st.session_state:
    st.session_state.show_fe = False



def about_df(df):
    df_sample = df.sample(6)
    size = df.shape[0]

    buffer = io.StringIO()
    df.info(buf=buffer)
    info = buffer.getvalue()

    columns = df.dtypes
    missing_values = df.isnull().sum()
    stats = df.describe(include='all')
    missing_percentage = (df.isnull().sum() / size) * 100

#outliers

    outlier_count={}
    numeric_col=df.select_dtypes(include=np.number).columns
    
    for col in numeric_col:
        q1=df[col].quantile(0.25)
        q3=df[col].quantile(0.75)
        
        iqr=q3-q1
        lower=q1-1.5*iqr
        upper=q3+1.5*iqr
        
        count=((df[col]<lower)|(df[col]>upper)).sum()
        outlier_count[col]=count
        
    outlier_df=pd.DataFrame.from_dict(outlier_count,orient="index",columns=["outlier_count"])      

    return df_sample, size, info, columns, missing_values, stats, missing_percentage,outlier_df

def drop_columns(df, na_threshold):
    size = df.shape[0]
    cols_to_drop = []

    for col in df.columns:
        missing_count = df[col].isnull().sum()
        na_percent = (missing_count / size) * 100
        if na_percent > na_threshold:
            cols_to_drop.append(col)

    cleaned_df = df.drop(columns=cols_to_drop)
    return cleaned_df, cols_to_drop


def by_mean(df):
    df_mean_cleaned=df.copy()
    df_mean_cleaned.replace(r'.\s*$',np.nan,regex=True,inplace=True)
    
    #only for numeric column  so dtypes
    for col in df_mean_cleaned.select_dtypes(include="number").columns:
        mean_val=round(df_mean_cleaned[col].mean(),2)
        df_mean_cleaned[col].fillna(mean_val,inplace=True)
        
    return df_mean_cleaned 

def by_mode(df):
    df_mode_cleaned=df.copy()
    mode_of_col=[]
    df_mode_cleaned.replace(r'.\*+-s&$',np.nan,regex=True,inplace=True)
    for col in df_mode_cleaned.columns:
        if df_mode_cleaned[col].isnull().sum()>0:
            mode_val=df_mode_cleaned[col].mode()
            
            if not mode_val.empty:
                df_mode_cleaned[col]=df_mode_cleaned[col].fillna(mode_val[0])
                mode_of_col.append(mode_val[0])
                
    
    return df_mode_cleaned,mode_of_col


def cap_outlier(df):
    df=df.copy()
    numeric_col=df.select_dtypes(include=np.number).columns
    
    for col in numeric_col:
        q1=df[col].quantile(0.25)
        q3=df[col].quantile(0.75)
        
        iqr=q3-q1
        lower=q1-1.5*iqr
        upper=q3+1.5*iqr
        df[col]=np.clip(df[col],lower,upper)
    return df

def z_score(df):
    df=df.copy()
    
    numeric_col=df.select_dtypes(include=np.number).columns
    z_scores=np.abs(zscore(df[numeric_col],nan_policy='omit'))
    
    df=df[(z_scores< 3).all(axis=1)]
    
    return df
    
    
     


def visualise(df):
    cols=[]
    df_v=df.copy()
    num_col=df_v.select_dtypes(include=np.number).columns.tolist()
    categ_col=df_v.select_dtypes(include=['object','category']).columns.tolist()
    
    return num_col,categ_col
    


def age_group(df,col):
    df=df.copy()
    df[col + "group"]=pd.cut(df[col],
                             bins=[0,18,30,48,62,100],
                             labels=["Teen","young","adult","senior","elder"])
    return df    


def minmax(df,col):
    df=df.copy()
    
    scaler=MinMaxScaler()
    df[col + "scaled"]= scaler.fit_transform(df[[col]])
    
    return df


def label_encode(df,col):
    df=df.copy()
    le=LabelEncoder()
    
    df[col + "ëncoded"]=le.fit_transform(df[col].astype(str))
    return df
    
def log_trans(df,col):
    df=df.copy()
    df[col + "log"]=np.log1p(df[col])
    return df    


def  stand_scale(df,col):
    df=df.copy()
    
    scaler=StandardScaler()
    df[col + "std"]=scaler.fit_transform(df[[col]])
    
    return df


def add_derived_col(df,col1,col2,operation,new_col):
    df=df.copy()
    
    if operation=="add":
        df[new_col]=df[col1]+df[col2]
        
    elif operation=="subtract":
        df[new_col]=df[col1]-df[col2]
        
    elif operation=="multiply":
        df[new_col]=df[col1]*df[col2]
        
    elif operation=="divide":
        df[new_col]=df[col1]/df[col2].replace(0,np.nan)
        
        
    return df    
        
                    






st.set_page_config(page_title="DATA.DOX", page_icon="📊", layout="wide")

st.markdown("<h1 style='text-align: center;'>📊 DATA.DOX</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Smart Data Analysis Dashboard</h4>", unsafe_allow_html=True)
st.divider()

df = pd.DataFrame()


st.sidebar.title("📂 Analysis Panel")
uploaded_file = st.sidebar.file_uploader("Choose a CSV or PDF file", type=['csv','pdf'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File uploaded successfully ✅")


if st.sidebar.button("🔍 About Dataset"):
    if df.empty:
        st.warning("⚠️ Please upload a dataset first")
    else:
        df_sample, size, info, columns,outlier_df, missing_values, stats, missing_percentage = about_df(df)

        st.subheader("📄 Dataset Sample")
        st.dataframe(df_sample)

        st.subheader("📏 Dataset Size")
        st.info(f"Total Rows: **{size}**")

        st.subheader("ℹ️ DataFrame Information")
        st.text(info)

        st.subheader("❌ Missing Values")
        st.dataframe(missing_values)

        st.subheader("Missing Percentage (%)")
        st.dataframe(missing_percentage.round(2))
        
        st.subheader("Outlier")
        st.dataframe(outlier_df)
        
        st.subheader("🧾 Column Data Types")
        st.dataframe(columns)

        st.subheader("📊 Statistical Summary")
        st.dataframe(stats)


with st.sidebar:

    if st.button("🧹 Data Cleaning"):
        st.session_state.show_cleaning = True

    if st.session_state.get("show_cleaning", False):
        st.markdown("### Data Cleaning Options")

        # MAIN CHOICE (ONLY ONE)
        cleaning_choice = st.radio(
            "Choose ONE cleaning method",
            [
                "Drop Column",
                "Fill NA with Mean",
                "Fill NA with Mode",
                "Outlier Clearance"
            ]
        )

        
        na_threshold = None
        method = None

        if cleaning_choice == "Drop Column":
            na_threshold = st.slider(
                "Drop columns with NA % greater than",
                0, 100, step=5
            )

        elif cleaning_choice == "Outlier Clearance":
            method = st.selectbox(
                "Type of outlier clearance",
                ["Z-Score", "Cap-Filling"]
            )

        apply_cleaning = st.button("Apply Cleaning")

        if apply_cleaning:
            st.session_state.apply_cleaning = True

          
    if st.session_state.get("apply_cleaning", False):

        if df.empty:
            st.write("⚠️ Please upload a dataset first")

        else:
            csv_buffer = io.StringIO()

            # ---- DROP COLUMN ----
            if cleaning_choice == "Drop Column":
                cleaned_df, cols_to_drop = drop_columns(df, na_threshold)
                st.write("Dropped columns:", cols_to_drop)

            # ---- MEAN ----
            elif cleaning_choice == "Fill NA with Mean":
                cleaned_df = by_mean(df)

            # ---- MODE ----
            elif cleaning_choice == "Fill NA with Mode":
                cleaned_df, mode_of_col = by_mode(df)
                st.write(mode_of_col)

            # ---- OUTLIER ----
            elif cleaning_choice == "Outlier Clearance":
                if method == "Cap-Filling":
                    cleaned_df = cap_outlier(df)
                else:
                    cleaned_df = z_score(df)

            # SAVE
            st.session_state.cleaned_df = cleaned_df
            cleaned_df.to_csv(csv_buffer, index=False)

            st.success("✅ Cleaning applied successfully")

            st.download_button(
                "📩 Download the cleaned dataset",
                csv_buffer.getvalue(),
                "cleaned_dataset.csv",
                "text/csv"
            )
        
            
            
    
    
        # reset flag AFTER download render
        st.session_state.apply_cleaning = False
        
        
if st.sidebar.markdown("📈Visualise data ")     :
    if not df.empty :
        
        
        vis=(
            st.session_state.cleaned_df 
            if st.session_state.cleaned_df is not None
            else df
        )
        
        num_col,categ_col=visualise(df)
        
        show_viz=st.sidebar.checkbox("show visualisation")
        
        if show_viz:
        
            type_chart= st.selectbox("select the visualisation",["Bar graph","Line chart","Histogram","pie chart"],key="chart_type")
                
           
                
            if type_chart=="Bar graph" :
                if categ_col and num_col:
                    x=st.selectbox("select the required column",categ_col,key="bar_x")
                    y=st.selectbox("select the required column ",num_col,key="bar_y")
                    data=vis.groupby(x)[y].mean()
                #  st.bar_chart(data)
                    fig ,ax=plt.subplots()
                    ax.bar(
                        data.index.astype(str),
                        data.values,
                        
                        width=0.5
                    )
                    
                    ax.set_xlabel(x)
                    ax.set_ylabel(y)
                    ax.set_title(f"{y} by {x}")

                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                
                else:
                    st.warning("⚠️Need at least one categorical and one numeric column")  
                    
            if type_chart=="Line chart":
                
                if categ_col and num_col:
                    x = st.selectbox("X axis", vis.columns, key="line_x")
                    y = st.selectbox("Y axis", num_col, key="line_y")

                    use_group = st.checkbox("Aggregate (group by X)", key="line_group")

                    fig, ax = plt.subplots()

                    if use_group:
                        data = vis.groupby(x)[y].mean()
                        ax.plot(data.index.astype(str), data.values, marker='o',color="#E3BAE3")
                    else:
                        plot_df = vis[[x, y]].dropna()
                        if len(plot_df) > 2000:
                            plot_df = plot_df.sample(2000, random_state=42)

                        ax.plot(plot_df[x], plot_df[y], marker='o',color="#E3BAE3")

                    ax.set_xlabel(x)
                    ax.set_ylabel(y)
                    ax.set_title(f"{y} vs {x}")
                    plt.xticks(rotation=45)

                    st.pyplot(fig)
                else:
                     st.warning("need numeric and atleast one category columns")
                
            if type_chart=="Histogram":
                  if categ_col and num_col:
                    
                        col=st.selectbox("select any column",num_col,key="col_hist")
                        max_bins=min(100,len(vis[col])//10)
                        
                        bins=st.slider("Bins",
                                       
                                       min_value=5,
                                       max_value=max_bins,
                                       value=min(30,max_bins),
                                       key="bins_hist")
                        
                        fig,ax=plt.subplots()   
                        
                        ax.hist(
                            
                            vis[col],
                            bins=bins,
                            edgecolor="black",
                            linewidth=0.6,
                            color="#7DAAD7"
                            
                        ) 
                        st.pyplot(fig)
                        
                  else:
                        st.warning("need numeric  and atleast one category column")   
                        
           
                        
            
            if type_chart=="pie chart" :
                if categ_col:
                    col=st.selectbox("select a categorical column",categ_col,key="pie")
                    data=vis[col].value_counts()
                    
                    fig,ax=plt.subplots()
                    
                    ax.pie(data.values,
                           labels=data.index,
                           autopct="%1.1f%%",
                           startangle=90
                           )
                    
                    ax.axis("equal")
                    ax.set_title(f"Distributiion of {col}")
                    st.pyplot(fig)
                    
                    
                    
                    
#t.subheader(" Feature Engineering")
if st.sidebar.button("🧩Feature Engineering"):
    st.session_state.show_fe = True
if  st.session_state.show_fe  and not df.empty:
            st.subheader("🧩 Feature Engineering")
        
            num_col,categ_col=visualise(df)
            
            
        #  vis=(st.session_state.cleaned_df if st.session_state.cleaned_df is not None else df
        
            if isinstance(st.session_state.cleaned_dfs, pd.DataFrame):
                vis = st.session_state.cleaned_dfs.copy()
            elif isinstance(df, pd.DataFrame) and not df.empty:
                vis = df.copy()
            else:
                st.warning("⚠️ No dataset available for feature engineering")
                vis = None
                
                
            
            engop=st.selectbox(
                "choose feature engineering method",
                [
                    "Age group (binning)",
                    "Log transform",
                    "Min-Max Scaling",
                    "standard scaling",
                    "label encoding"
                ],
                key="fe_method"
            )
            
            
            if engop in[
                    "Age group (binning)",
                    "Log transform",
                    "Min-Max Scaling",
                    "standard scaling",]:
                engcol=st.selectbox("select numeric col",num_col)
                
                
            else:
                engcol=st.selectbox("select categorical column",categ_col)
                
                
            if st.button("apply feature engineering"):
                st.session_state.apply_fe=True    
                
            if st.session_state.apply_fe and vis is not None:
                if engop=="Age group (binning)" :
                    vis=age_group(vis,engcol)  
                    
                    
                
                if engop=="Log transform":
                    vis=log_trans(vis,engcol)  
                    
                    
                
                if engop== "Min-Max Scaling":
                    vis=minmax(vis,engcol)  
                    
                    
                
                if engop== "standard scaling":
                    vis=stand_scale(vis,engcol)  
                        
                if engop==  "label encoding":
                    vis=label_encode(vis,engcol)  
                    
                    
                st.session_state.cleaned_dfs=vis
                st.success("✅Feature engineered successfully")  
            
                
                
                csv_buffers=io.StringIO()
                vis.to_csv(csv_buffers,index=False)
                
                st.download_button("📩Download the engeneered dataset",
                                csv_buffers.getvalue(),
                                "engiineered_dataset.csv",
                                
                                mime="text/csv")
if st.sidebar.checkbox("Add column"):
    st.subheader("➕ Add Derived Column")

    # Choose source dataframe safely
    if isinstance(st.session_state.cleaned_dfs, pd.DataFrame):
        base_df = st.session_state.cleaned_dfs.copy()
    elif isinstance(st.session_state.cleaned_df, pd.DataFrame):
        base_df = st.session_state.cleaned_df.copy()
    elif not df.empty:
        base_df = df.copy()
    else:
        base_df = None

    if base_df is None:
        st.warning("⚠️ No dataset available")
        st.stop()

    num_col, _ = visualise(base_df)

    if len(num_col) >= 2:
        col1 = st.selectbox("Select first numeric column", num_col)
        col2 = st.selectbox("Select second numeric column", num_col)

        operation = st.selectbox(
            "Select operation",
            ["add", "subtract", "multiply", "divide"]
        )

        new_col_name = st.text_input(
            "New column name",
            value=f"{col1}_{operation}_{col2}"
        )

        if st.button("Add column"):
            derived_df = add_derived_col(
                base_df,
                col1,
                col2,
                operation,
                new_col_name
            )

            # store ONLY here
            st.session_state.derived_df = derived_df

            st.success(f"✅ Column `{new_col_name}` added successfully")

            csv_buffer = io.StringIO()
            derived_df.to_csv(csv_buffer, index=False)

            st.download_button(
                "📩 Download dataset",
                csv_buffer.getvalue(),
                "derived_dataset.csv",
                "text/csv"
            )

    else:
        st.warning("⚠️ At least TWO numeric columns are required")
