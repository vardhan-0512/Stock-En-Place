from flask import Flask, request, jsonify
import yfinance as yf
import pandas as pd
import numpy as np
import Indicators

app = Flask(__name__)

def get_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            return None
        return data
    except Exception as e:
        return None

@app.route('/indicator/<indicator_name>', methods=['GET'])
def calculate_indicator(indicator_name):
    ticker = request.args.get('ticker')
    start_date = request.args.get('start', '2023-01-01')
    end_date = request.args.get('end', pd.to_datetime('today').strftime('%Y-%m-%d'))

    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    stock_data = get_data(ticker, start_date, end_date)

    if stock_data is None:
        return jsonify({"error": f"Could not retrieve data for ticker: {ticker}"}), 404

    indicator_function = getattr(Indicators, indicator_name, None)

    if not callable(indicator_function):
        return jsonify({"error": f"Indicator '{indicator_name}' not found"}), 404

    params = {}
    for key, value in request.args.items():
        if key not in ['ticker', 'start', 'end']:
            try:
                if '.' in value:
                    params[key] = float(value)
                else:
                    params[key] = int(value)
            except ValueError:
                params[key] = value

    try:
        result = indicator_function(stock_data, **params)

        if isinstance(result, (pd.DataFrame, pd.Series)):
            json_result = result.to_json(orient='split', date_format='iso')
        elif isinstance(result, dict):
            json_result = jsonify(result)
        else:
             json_result = jsonify(str(result))

        return json_result

    except Exception as e:
        return jsonify({"error": f"Error calculating indicator: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
