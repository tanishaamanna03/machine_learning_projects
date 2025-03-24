<h1>House Price Prediction Using Machine Learning</h1>
<p>This project focuses on predicting future house prices using data from the Federal Reserve and Zillow. The model is built to predict whether house prices will increase or decrease in the future based on historical data and housing market trends. A random forest model is used to make these predictions, with error measured through backtesting. The model can be improved by adding new predictors.</p>

<h3>Requirements:</h3>

- Python 3.8+
- JupyterLab
- pandas
- yfinance
- scikit-learn

<h3>Datasets</h3>

You can download the datasets from the following:
1. Federal reserve data
- CPI dataset - CPIAUCSL.csv (https://fred.stlouisfed.org/series/CPIAUCSL)
- Rental vacancy rate - RRVRUSQ156N.csv (https://fred.stlouisfed.org/series/RRVRUSQ156N)
- Mortgage interest rates - MORTGAGE30US.csv (https://fred.stlouisfed.org/series/MORTGAGE30US)

2. Zillow
- ZHVI (raw, weekly) - Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_month.csv
- Median sale price (raw, all homes, weekly) - Metro_median_sale_price_uc_sfrcondo_week.csv
