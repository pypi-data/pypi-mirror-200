#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries

# In[1]:


import pandas as pd
import numpy as np
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from sklearn.preprocessing import MinMaxScaler, StandardScaler

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import numpy as np

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, SpectralClustering, MeanShift, Birch

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, SpectralClustering, MeanShift, Birch

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, SpectralClustering, MeanShift, Birch
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB


# In[ ]:





# ### Functions

# In[2]:


def clean_data(df, drop_cols=None, fillna_cols=None, numeric_cols=None, date_cols=None, text_cols=None, regex_dict=None):
    """
    A function that performs advanced data cleaning on a pandas DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be cleaned.
    drop_cols (list of str): Columns to be dropped. Default is None.
    fillna_cols (dict): Columns and their respective values to fill missing values with. Default is None.
    numeric_cols (list of str): Columns to be converted to numeric data type. Default is None.
    date_cols (list of str): Columns to be converted to datetime data type. Default is None.
    text_cols (list of str): Columns to be cleaned using regex. Default is None.
    regex_dict (dict): A dictionary of column names and their respective regex patterns to clean. Default is None.

    Returns:
    pandas.DataFrame: The cleaned DataFrame.
    """

    # Drop columns
    if drop_cols:
        df = df.drop(drop_cols, axis=1)

    # Fill missing values
    if fillna_cols:
        for col, val in fillna_cols.items():
            df[col] = df[col].fillna(val)

    # Convert numeric columns to float data type
    if numeric_cols:
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Convert date columns to datetime format
    if date_cols:
        df[date_cols] = df[date_cols].apply(pd.to_datetime, errors='coerce')

    # Clean text columns using regex
    if text_cols and regex_dict:
        for col in text_cols:
            for regex_name, regex_pattern in regex_dict.items():
                df[col] = df[col].apply(lambda x: re.sub(regex_pattern, regex_name, str(x), flags=re.IGNORECASE))

    # Remove special characters from string columns
    if text_cols:
        for col in text_cols:
            df[col] = df[col].replace('[^A-Za-z0-9\s]+', '', regex=True)

    # Remove leading and trailing whitespaces from string columns
    if text_cols:
        for col in text_cols:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # Convert all string columns to lowercase
    if text_cols:
        for col in text_cols:
            df[col] = df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)

    # Reset index
    df = df.reset_index(drop=True)

    return df


# In[3]:


def remove_outliers(df, numeric_cols, threshold=3):
    for col in numeric_cols:
        z_scores = (df[col] - df[col].mean()) / df[col].std()
        df = df[abs(z_scores) < threshold]
    return df


# In[4]:


def standardize_text(df, text_cols):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    for col in text_cols:
        df[col] = df[col].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split() if word not in stop_words]))
    return df


# In[5]:


def encode_categorical(df, cat_cols, encoding='one-hot'):
    if encoding == 'one-hot':
        encoder = OneHotEncoder()
        encoded = encoder.fit_transform(df[cat_cols])
        df_encoded = pd.DataFrame(encoded.toarray(), columns=encoder.get_feature_names(cat_cols))
        df = pd.concat([df, df_encoded], axis=1)
    elif encoding == 'label':
        encoder = LabelEncoder()
        for col in cat_cols:
            df[col] = encoder.fit_transform(df[col])
    return df


# In[6]:


def handle_missing_values(df, numeric_cols, cat_cols):
    for col in numeric_cols:
        df[col].fillna(df[col].mean(), inplace=True)
    for col in cat_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)
    return df


# In[7]:


def remove_duplicates(df):
    df.drop_duplicates(inplace=True)
    return df


# In[8]:


def normalize_data(df, numeric_cols, scaling='min-max'):
    if scaling == 'min-max':
        scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    elif scaling == 'z-score':
        scaler = StandardScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df


# In[9]:


def clean_text(df, text_cols):
    for col in text_cols:
        df[col] = df[col].apply(lambda x: re.sub('<.*?>', '', x))
        df[col] = df[col].apply(lambda x: re.sub(r'http\S+', '', x))
        df[col] = df[col].apply(lambda x: re.sub(r'[^\w\s]', '', x))
    return df


# In[10]:


def handle_noisy_data(df, column, window):
    # Apply Moving Average smoothing to column
    smoothed_values = df[column].rolling(window=window).mean()
    
    # Replace original column values with smoothed values
    df[column] = smoothed_values
    
    return df


# In[11]:


def generate_visualizations(df):
    # Summary statistics
    print(df.describe())

    # Histogram for all numeric columns
    df.hist(figsize=(10,10))
    plt.show()

    # Box plot for all numeric columns
    sns.boxplot(data=df)
    plt.show()

    # Heatmap for correlation matrix
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.show()

    # Scatter plot matrix for all numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) >= 2:
        sns.pairplot(df[numeric_cols])
        plt.show()

    # Bar plot for categorical column
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        sns.countplot(x=categorical_cols[0], data=df)
        plt.show()

        # Stacked bar plot for two categorical columns
        if len(categorical_cols) >= 2:
            sns.countplot(x=categorical_cols[0], hue=categorical_cols[1], data=df)
            plt.show()

    # Scatter plot for two numeric columns
    if len(numeric_cols) >= 2:
        for i in range(len(numeric_cols)):
            for j in range(i+1, len(numeric_cols)):
                sns.scatterplot(x=numeric_cols[i], y=numeric_cols[j], data=df)
                plt.show()

    # Violin plot for all numeric columns
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            sns.violinplot(y=col, data=df)
            plt.show()

    # Line plot for a numeric column against a categorical column
    if len(numeric_cols) > 0 and len(categorical_cols) > 0:
        for col in numeric_cols:
            sns.lineplot(x=categorical_cols[0], y=col, data=df)
            plt.show()

    # Boxen plot for all numeric columns
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            sns.boxenplot(y=col, data=df)
            plt.show()


# In[12]:


def perform_regression(df, target_column, feature_columns, regression_type='linear', test_size=0.2, random_state=42):
    """
    Perform regression on a given dataset and return the trained model object.

    Parameters:
        df (pandas.DataFrame): The input dataset.
        target_column (str): The name of the target column.
        feature_columns (list): A list of column names to use as features.
        regression_type (str): The type of regression to perform. Must be one of ['linear', 'ridge', 'lasso',
            'elastic_net', 'decision_tree', 'random_forest', 'gradient_boosting']. Default is 'linear'.
        test_size (float): The proportion of the data to use for testing. Default is 0.2.
        random_state (int): The random seed to use for reproducibility. Default is 42.

    Returns:
        A trained regression model object.
    """
    # Split the data into training and testing sets
    X = df[feature_columns]
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Train the selected regression model on the training data
    if regression_type == 'linear':
        model = LinearRegression()
    elif regression_type == 'ridge':
        model = Ridge()
    elif regression_type == 'lasso':
        model = Lasso()
    elif regression_type == 'elastic_net':
        model = ElasticNet()
    elif regression_type == 'decision_tree':
        model = DecisionTreeRegressor()
    elif regression_type == 'random_forest':
        model = RandomForestRegressor()
    elif regression_type == 'gradient_boosting':
        model = GradientBoostingRegressor()
    else:
        raise ValueError("Invalid regression type: {}".format(regression_type))
    
    model.fit(X_train, y_train)

    # Evaluate the model on the testing data
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Print the model's performance metrics
    print("Mean squared error: {:.2f}".format(mse))
    print("R2 score: {:.2f}".format(r2))

    # Plot the predicted vs. actual values for the testing set
    sns.set_style('darkgrid')
    ax = sns.scatterplot(x=y_test, y=y_pred)
    ax.set(xlabel='Actual values', ylabel='Predicted values', title='Actual vs. Predicted values')
    plt.show()

    # Plot the feature importance (if applicable) for tree-based models
    if regression_type in ['decision_tree', 'random_forest', 'gradient_boosting']:
        feature_importance = model.feature_importances_
        sorted_idx = feature_importance.argsort()
        plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx])
        plt.yticks(range(len(sorted_idx)), X.columns[sorted_idx])
        plt.xlabel('Feature Importance')
        plt.title('Feature Importance')
        plt.show()

    return model


# In[13]:


def get_best_regression(df):
    """
    Identify the best regression model for a given dataset and return the trained model object.

    Parameters:
        df (pandas.DataFrame): The input dataset.

    Returns:
        A trained regression model object.
    """
    # Identify numeric columns as potential target and feature columns
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if len(numeric_cols) < 2:
        raise ValueError("Not enough numeric columns for regression")

    # Scale the numeric data
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # Split the data into training and testing sets
    target_column = numeric_cols[-1]
    feature_columns = numeric_cols[:-1]
    X = df[feature_columns]
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train and evaluate a linear regression model
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    mse_lr = mean_squared_error(y_test, y_pred_lr)

    # Train and evaluate a ridge regression model
    ridge = Ridge()
    ridge.fit(X_train, y_train)
    y_pred_ridge = ridge.predict(X_test)
    mse_ridge = mean_squared_error(y_test, y_pred_ridge)

    # Train and evaluate a lasso regression model
    lasso = Lasso()
    lasso.fit(X_train, y_train)
    y_pred_lasso = lasso.predict(X_test)
    mse_lasso = mean_squared_error(y_test, y_pred_lasso)

    # Train and evaluate an elastic net regression model
    en = ElasticNet()
    en.fit(X_train, y_train)
    y_pred_en = en.predict(X_test)
    mse_en = mean_squared_error(y_test, y_pred_en)

    # Train and evaluate a decision tree regression model
    dt = DecisionTreeRegressor()
    dt.fit(X_train, y_train)
    y_pred_dt = dt.predict(X_test)
    mse_dt = mean_squared_error(y_test, y_pred_dt)

    # Train and evaluate a random forest regression model
    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    mse_rf = mean_squared_error(y_test, y_pred_rf)

    # Train and evaluate a gradient boosting regression model
    gb = GradientBoostingRegressor()
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_test)
    mse_gb = mean_squared_error(y_test, y_pred_gb)

    # Find the regression model with the lowest MSE and return it
    mses = {'Linear Regression': mse_lr, 'Ridge Regression': mse_ridge, 'Lasso Regression': mse_lasso,
            'Elastic Net Regression': mse_en, 'Decision Tree Regression': mse_dt, 'Random Forest Regression': mse_rf,
            'Gradient Boosting Regression': mse_gb}
    best_model = min(mses, key=mses.get)
    
    return best_model


# In[14]:


def perform_clustering(df):
    """
    Performs various clustering models on a given dataframe and returns the resulting labels and inertia values for each model.
    
    Parameters:
    df (pd.DataFrame): Dataframe to be clustered
    
    Returns:
    results (dict): A dictionary containing the resulting labels and inertia values for each clustering model
    """
    # Drop any missing values
    df = df.dropna()

    # Standardize the data
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans_labels = kmeans.fit_predict(df_scaled)
    kmeans_inertia = kmeans.inertia_

    # Perform Agglomerative clustering
    agg = AgglomerativeClustering(n_clusters=2)
    agg_labels = agg.fit_predict(df_scaled)

    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=1, min_samples=3)
    dbscan_labels = dbscan.fit_predict(df_scaled)

    # Perform Spectral clustering
    spectral = SpectralClustering(n_clusters=2, affinity='nearest_neighbors')
    spectral_labels = spectral.fit_predict(df_scaled)

    # Perform MeanShift clustering
    ms = MeanShift()
    ms_labels = ms.fit_predict(df_scaled)

    # Perform Birch clustering
    birch = Birch(n_clusters=2)
    birch_labels = birch.fit_predict(df_scaled)

    # Store results in a dictionary
    results = {
        'KMeans': {'labels': kmeans_labels, 'inertia': kmeans_inertia},
        'Agglomerative': {'labels': agg_labels},
        'DBSCAN': {'labels': dbscan_labels},
        'Spectral': {'labels': spectral_labels},
        'MeanShift': {'labels': ms_labels},
        'Birch': {'labels': birch_labels}
    }

    # Visualize the results
    fig, axs = plt.subplots(2, 3, figsize=(18, 12))
    axs = axs.ravel()
    for i, (name, result) in enumerate(results.items()):
        if name == 'KMeans':
            axs[i].scatter(df_scaled[:, 0], df_scaled[:, 1], c=result['labels'])
            axs[i].set_title(f"{name}\nInertia: {result['inertia']:.2f}")
        else:
            axs[i].scatter(df_scaled[:, 0], df_scaled[:, 1], c=result['labels'])
            axs[i].set_title(name)

    plt.tight_layout()
    plt.show()

    return results


# In[29]:


# def detect_best_clustering_model(df):
#     """
#     Detects the best clustering model for a given dataframe and returns the resulting labels.
    
#     Parameters:
#     df (pd.DataFrame): Dataframe to be clustered
    
#     Returns:
#     labels (np.array): Resulting cluster labels from the best clustering model
#     """
#     # Drop any missing values
#     df = df.dropna()

#     # Standardize the data
#     from sklearn.preprocessing import StandardScaler
#     scaler = StandardScaler()
#     df_scaled = scaler.fit_transform(df)

#     # Define list of clustering models
#     models = [
#         KMeans(n_clusters=2, random_state=42),
# #         AgglomerativeClustering(n_clusters=2),
#         DBSCAN(eps=1, min_samples=3),
#         SpectralClustering(n_clusters=2, affinity='nearest_neighbors'),
#         MeanShift(),
#         Birch(n_clusters=2)
#     ]

#     # Perform clustering for each model and record the resulting labels and score
#     best_score = -np.inf
#     best_labels = None
#     for model in models:
#         labels = model.fit_predict(df_scaled)
#         score = model.score(df_scaled)
#         if score > best_score:
#             best_score = score
#             best_labels = labels

#     # Return the labels from the best clustering model
#     return best_labels


# In[ ]:





# In[30]:


# def find_best_clustering_model(df):
#     """
#     Detects the best clustering model for a given dataframe, applies the model to the dataset,
#     and returns the resulting cluster labels and the model used.
    
#     Parameters:
#     df (pd.DataFrame): Dataframe to be clustered
    
#     Returns:
#     labels (np.array): Resulting cluster labels from the best clustering model
#     model_name (str): Name of the best clustering model used
#     """
#     # Drop any missing values
#     df = df.dropna()

#     # Standardize the data
#     scaler = StandardScaler()
#     df_scaled = scaler.fit_transform(df)

#     # Define list of clustering models
#     models = [
#         KMeans(n_clusters=2, random_state=42),
#         AgglomerativeClustering(n_clusters=2),
#         DBSCAN(eps=1, min_samples=3),
#         SpectralClustering(n_clusters=2, affinity='nearest_neighbors'),
#         MeanShift(),
#         Birch(n_clusters=2)
#     ]

#     # Perform clustering for each model and record the resulting labels and score
#     best_score = -np.inf
#     best_labels = None
#     best_model_name = ''
#     for model in models:
#         labels = model.fit_predict(df_scaled)
#         score = model.score(df_scaled)
#         if score > best_score:
#             best_score = score
#             best_labels = labels
#             best_model_name = type(model).__name__

#     # Apply the best clustering model to the dataset and return the labels and model name
#     best_model = models[np.argmax([model.score(df_scaled) for model in models])]
#     best_labels = best_model.fit_predict(df_scaled)
#     return best_labels, best_model_name


# In[43]:


def apply_classification(dataset, target_column, classification_technique):
    # Load the dataset
    X = dataset.drop(columns=[target_column])
    y = dataset[target_column]
    
    # Preprocess the data
    # ...
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Choose a classification technique
    if classification_technique == "decision_tree":
        model = DecisionTreeClassifier()
    elif classification_technique == "random_forest":
        model = RandomForestClassifier()
    elif classification_technique == "logistic_regression":
        model = LogisticRegression()
    elif classification_technique == "svm":
        model = SVC()
    elif classification_technique == "naive_bayes":
        model = GaussianNB()
    else:
        raise ValueError("Invalid classification technique.")
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average=None)
    recall = recall_score(y_test, y_pred, average=None)
    f1 = f1_score(y_test, y_pred, average=None)
    
    # Predict using the model
    # ...
    
    return model, accuracy, precision, recall, f1

# model, accuracy, precision, recall, f1 = apply_classification(my_dataset, "target", "logistic_regression")


# In[44]:


def find_best_classification(dataset, target_column):
    # Load the dataset
    X = dataset.drop(columns=[target_column])
    y = dataset[target_column]
    
    # Preprocess the data
    # ...
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Choose the best classification technique
    techniques = {
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Logistic Regression": LogisticRegression(),
        "SVM": SVC(),
        "Naive Bayes": GaussianNB()
    }
    best_technique = None
    best_accuracy = 0
    for technique_name, model in techniques.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        if accuracy > best_accuracy:
            best_technique = technique_name
            best_accuracy = accuracy
    
    # Train the best model
    if best_technique == "Decision Tree":
        model = DecisionTreeClassifier()
    elif best_technique == "Random Forest":
        model = RandomForestClassifier()
    elif best_technique == "Logistic Regression":
        model = LogisticRegression()
    elif best_technique == "SVM":
        model = SVC()
    elif best_technique == "Naive Bayes":
        model = GaussianNB()
    else:
        raise ValueError("Invalid classification technique.")
    model.fit(X_train, y_train)
    
    # Evaluate the best model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average=None)
    recall = recall_score(y_test, y_pred, average=None)
    f1 = f1_score(y_test, y_pred, average=None)
    
    return model, best_technique, accuracy, precision, recall, f1

# model, best_technique, accuracy, precision, recall, f1 = find_best_classification(my_dataset, "target")


# In[ ]:




