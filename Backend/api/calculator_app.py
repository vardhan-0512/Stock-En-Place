from flask import Flask, render_template, request, jsonify
from calculators import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    calc_type = data.get('type')
    
    try:
        if calc_type == 'stock_profit_loss':
            result = calculate_stock_profit_loss(
                float(data['purchase_price']),
                float(data['sale_price']),
                int(data['quantity']),
                float(data.get('purchase_commission', 0)),
                float(data.get('sale_commission', 0))
            )
        
        elif calc_type == 'position_size':
            result = calculate_position_size(
                float(data['account_balance']),
                float(data['risk_percentage']),
                float(data['entry_price']),
                float(data['stop_loss_price'])
            )
        
        elif calc_type == 'risk_reward_ratio':
            result = calculate_risk_reward_ratio(
                float(data['entry_price']),
                float(data['stop_loss_price']),
                float(data['target_price'])
            )
        
        elif calc_type == 'breakeven_point':
            result = calculate_breakeven_point(
                float(data['purchase_price']),
                int(data['quantity']),
                float(data['total_fees'])
            )
        
        elif calc_type == 'capital_gains_tax':
            result = calculate_capital_gains_tax(
                float(data['profit']),
                float(data['tax_rate'])
            )
        
        elif calc_type == 'dividend_yield':
            result = calculate_dividend_yield(
                float(data['stock_price']),
                float(data['annual_dividend_per_share'])
            )
        
        elif calc_type == 'investment_return':
            result = calculate_investment_return(
                float(data['initial_investment']),
                float(data['final_value'])
            )
        
        elif calc_type == 'cagr':
            result = calculate_cagr(
                float(data['beginning_value']),
                float(data['ending_value']),
                int(data['years'])
            )
        
        elif calc_type == 'compound_growth':
            result = calculate_compound_growth(
                float(data['principal']),
                float(data['annual_rate']),
                int(data['years']),
                int(data.get('compounds_per_year', 1))
            )
        
        elif calc_type == 'future_value':
            result = calculate_future_value(
                float(data['present_value']),
                float(data['annual_rate']),
                int(data['years'])
            )
        
        elif calc_type == 'present_value':
            result = calculate_present_value(
                float(data['future_value']),
                float(data['annual_rate']),
                int(data['years'])
            )
        
        elif calc_type == 'dca':
            amounts = [float(x) for x in data['investment_amounts'].split(',')]
            prices = [float(x) for x in data['share_prices'].split(',')]
            result = calculate_dca(amounts, prices)
        
        elif calc_type == 'average_price':
            quantities = [int(x) for x in data['quantities'].split(',')]
            prices = [float(x) for x in data['prices'].split(',')]
            result = calculate_average_price(quantities, prices)
        
        elif calc_type == 'option_profit_loss':
            result = calculate_option_profit_loss(
                data['option_type'],
                float(data['strike_price']),
                float(data['stock_price_at_expiry']),
                float(data['premium_paid']),
                int(data.get('quantity', 100)),
                int(data.get('contracts', 1))
            )
        
        elif calc_type == 'total_cost':
            result = calculate_total_cost(
                float(data['trade_value']),
                float(data.get('commission_rate', 0)),
                float(data.get('fixed_fee', 0))
            )
        
        else:
            return jsonify({'error': 'Invalid calculation type'}), 400
        
        return jsonify({'result': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)