import argparse
import os
import pandas as pd

import Indicators
import LLM
import forecasts

def handle_indicator(args):
    print(f"Calculating indicator '{args.name}' for ticker '{args.ticker}'...")
    
    data = forecasts.get_stock_data(args.ticker, years=5)
    if data is None:
        return

    indicator_function = getattr(Indicators, args.name, None)
    if not callable(indicator_function):
        print(f"Error: Indicator '{args.name}' not found in Indicators.py.")
        return
        
    params = {}
    if args.params:
        for param in args.params:
            if '=' not in param:
                print(f"Error: Invalid parameter format '{param}'. Use key=value.")
                return
            key, value = param.split('=', 1)
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass
            params[key] = value

    try:
        result = indicator_function(data, **params)
        print("\n--- Result ---")
        if isinstance(result, (pd.DataFrame, pd.Series)):
            print(result.tail())
        else:
            print(result)
        print("\nCalculation complete.")
    except Exception as e:
        print(f"An error occurred while calculating the indicator: {e}")


def handle_ask(args):
    print("Sending question to LLM...")
    if not os.getenv("OPENROUTER_API_KEY"):
        print("\n--- IMPORTANT ---")
        print("Error: The OPENROUTER_API_KEY environment variable is not set.")
        print("Please set it to your OpenRouter API key to use this feature.")
        print("-----------------\n")
        return
        
    response = LLM.get_llm_response(args.question)
    print("\n--- LLM Response ---")
    print(response)
    print("\n--------------------\n")


def handle_forecast(args):
    forecasts.generate_ten_year_forecast(args.ticker)


def main():
    parser = argparse.ArgumentParser(
        description="A command-line tool for stock analysis, powered by technical indicators, AI, and forecasting models.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    parser_indicator = subparsers.add_parser(
        'indicator', 
        help='Calculate a technical indicator for a stock.',
        description='Calculates a specific technical indicator using historical stock data.'
    )
    parser_indicator.add_argument('name', help='The name of the indicator function (e.g., moving_average, rsi).')
    parser_indicator.add_argument('--ticker', required=True, help='Stock ticker symbol (e.g., AAPL).')
    parser_indicator.add_argument(
        '--params', 
        nargs='*', 
        help='''Additional parameters for the indicator in key=value format.
Example: period=50 std_dev=2'''
    )
    parser_indicator.set_defaults(func=handle_indicator)

    parser_ask = subparsers.add_parser(
        'ask', 
        help='Ask a financial question to an AI model.',
        description='Sends a question to a Large Language Model and prints the response.'
    )
    parser_ask.add_argument('question', type=str, help='The question to ask the LLM, enclosed in quotes.')
    parser_ask.set_defaults(func=handle_ask)

    parser_forecast = subparsers.add_parser(
        'forecast', 
        help='Generate a 10-year stock price forecast.',
        description='Uses the Prophet model to generate and plot a 10-year forecast for a stock.'
    )
    parser_forecast.add_argument('ticker', type=str, help='The stock ticker to forecast (e.g., GOOGL).')
    parser_forecast.set_defaults(func=handle_forecast)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
