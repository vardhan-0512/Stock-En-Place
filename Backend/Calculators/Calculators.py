import numpy as np

def calculate_stock_profit_loss(purchase_price: float, sale_price: float, quantity: int, purchase_commission: float = 0, sale_commission: float = 0):
    gross_profit_loss = (sale_price - purchase_price) * quantity
    total_commission = purchase_commission + sale_commission
    net_profit_loss = gross_profit_loss - total_commission
    return {
        "gross_profit_loss": gross_profit_loss,
        "net_profit_loss": net_profit_loss,
        "total_commission": total_commission
    }

def calculate_position_size(account_balance: float, risk_percentage: float, entry_price: float, stop_loss_price: float):
    risk_amount = account_balance * (risk_percentage / 100)
    risk_per_share = entry_price - stop_loss_price
    if risk_per_share <= 0:
        return 0
    position_size = risk_amount / risk_per_share
    return position_size

def calculate_risk_reward_ratio(entry_price: float, stop_loss_price: float, target_price: float):
    potential_risk = entry_price - stop_loss_price
    potential_reward = target_price - entry_price
    if potential_risk <= 0:
        return float('inf')
    return potential_reward / potential_risk

def calculate_breakeven_point(purchase_price: float, quantity: int, total_fees: float):
    total_cost = (purchase_price * quantity) + total_fees
    breakeven_price = total_cost / quantity
    return breakeven_price

def calculate_capital_gains_tax(profit: float, tax_rate: float):
    return profit * (tax_rate / 100)

def calculate_dividend_yield(stock_price: float, annual_dividend_per_share: float):
    if stock_price <= 0:
        return 0
    return (annual_dividend_per_share / stock_price) * 100

def calculate_investment_return(initial_investment: float, final_value: float):
    absolute_return = final_value - initial_investment
    if initial_investment == 0:
        percentage_return = float('inf')
    else:
        percentage_return = (absolute_return / initial_investment) * 100
    return {"absolute_return": absolute_return, "percentage_return": percentage_return}

def calculate_cagr(beginning_value: float, ending_value: float, years: int):
    if beginning_value <= 0 or years <= 0:
        return 0
    return ((ending_value / beginning_value) ** (1 / years) - 1) * 100

def calculate_compound_growth(principal: float, annual_rate: float, years: int, compounds_per_year: int = 1):
    rate = annual_rate / 100
    future_value = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)
    return future_value

def calculate_future_value(present_value: float, annual_rate: float, years: int):
    rate = annual_rate / 100
    return present_value * ((1 + rate) ** years)

def calculate_present_value(future_value: float, annual_rate: float, years: int):
    rate = annual_rate / 100
    return future_value / ((1 + rate) ** years)

def calculate_dca(investment_amounts: list, share_prices: list):
    total_invested = sum(investment_amounts)
    total_shares = sum(amount / price for amount, price in zip(investment_amounts, share_prices))
    if total_shares == 0:
        average_cost = 0
    else:
        average_cost = total_invested / total_shares
    return {"total_shares": total_shares, "average_cost_per_share": average_cost}

def calculate_average_price(quantities: list, prices: list):
    total_cost = sum(q * p for q, p in zip(quantities, prices))
    total_quantity = sum(quantities)
    if total_quantity == 0:
        return 0
    return total_cost / total_quantity

def calculate_option_profit_loss(option_type: str, strike_price: float, stock_price_at_expiry: float, premium_paid: float, quantity: int = 1, contracts: int = 1):
    if option_type.lower() == 'call':
        profit_per_share = max(0, stock_price_at_expiry - strike_price) - premium_paid
    elif option_type.lower() == 'put':
        profit_per_share = max(0, strike_price - stock_price_at_expiry) - premium_paid
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    net_profit_loss = profit_per_share * quantity * contracts
    return net_profit_loss

def calculate_total_cost(trade_value: float, commission_rate: float = 0, fixed_fee: float = 0):
    commission = trade_value * (commission_rate / 100)
    total_cost = trade_value + commission + fixed_fee
    return total_cost