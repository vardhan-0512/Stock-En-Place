const calculators = [
    { id: 'block-1', name: 'Profit/Loss Calculator', slug: 'profit-loss' },
    { id: 'block-2', name: 'Position Size Calculator', slug: 'position-size' },
    { id: 'block-3', name: 'Risk/Reward Ratio Calculator', slug: 'risk-reward' },
    { id: 'block-4', name: 'Break-Even Price Calculator', slug: 'break-even-price' },
    { id: 'block-5', name: 'Compound Interest Calculator', slug: 'compound-interest' },
    { id: 'block-6', name: 'ROI Calculator', slug: 'roi' },
    { id: 'block-7', name: 'CAGR Calculator', slug: 'cagr' },
    { id: 'block-8', name: 'Dividend Yield Calculator', slug: 'dividend-yield' },
    { id: 'block-9', name: 'Dividend Reinvestment Calculator', slug: 'dividend-reinvestment' },
    { id: 'block-10', name: 'Tax Impact Calculator', slug: 'tax-impact' },
    { id: 'block-11', name: 'Capital Gains Calculator', slug: 'capital-gains' },
    { id: 'block-12', name: 'Average Cost Calculator', slug: 'average-cost' },
    { id: 'block-13', name: 'Dollar-Cost Averaging Calculator', slug: 'dollar-cost-averaging' },
    { id: 'block-14', name: 'Margin Calculator', slug: 'margin' },
    { id: 'block-15', name: 'Leverage Calculator', slug: 'leverage' },
    { id: 'block-16', name: 'Futures Profit/Loss Calculator', slug: 'futures-profit-loss' },
    { id: 'block-17', name: 'Options Profit/Loss Calculator', slug: 'options-profit-loss' },
    { id: 'block-18', name: 'Option Greeks Calculator', slug: 'option-greeks' },
    { id: 'block-19', name: 'Implied Volatility Calculator', slug: 'implied-volatility' },
    { id: 'block-20', name: 'Covered Call Calculator', slug: 'covered-call' },
    { id: 'block-21', name: 'Protective Put Calculator', slug: 'protective-put' },
    { id: 'block-22', name: 'Stock Split Calculator', slug: 'stock-split' },
    { id: 'block-23', name: 'Reverse Stock Split Calculator', slug: 'reverse-stock-split' },
    { id: 'block-24', name: 'Rule of 72 Calculator', slug: 'rule-of-72' },
    { id: 'block-25', name: 'Trading Expectancy Calculator', slug: 'trading-expectancy' },
    { id: 'block-26', name: 'Drawdown Calculator', slug: 'drawdown' },
    { id: 'block-27', name: 'Average Down Calculator', slug: 'average-down' },
    { id: 'block-28', name: 'Position Sizing Calculator', slug: 'position-sizing' },
    { id: 'block-29', name: 'Trade Journal Calculator', slug: 'trade-journal' },
    { id: 'block-30', name: 'Portfolio Rebalancing Calculator', slug: 'portfolio-rebalancing' }
];

// --- Logic to handle page setup and navigation ---
window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const ticker = urlParams.get('ticker') || 'AAPL';
    
    document.getElementById('header-title').textContent = `Select a Calculator for ${ticker}`;

    const grid = document.getElementById('indicator-grid');

    calculators.forEach(calc => {
        const block = document.createElement('a');
        block.href = `calculator_page.html?ticker=${ticker}&calculator=${calc.slug}&name=${encodeURIComponent(calc.name)}`;
        block.className = 'indicator-block bg-[#1e1e1e] border border-gray-700 rounded-xl p-6 text-center hover:border-white hover:scale-105 transition-all duration-300 flex items-center justify-center';
        block.dataset.calculator = calc.slug;

        const text = document.createElement('span');
        text.className = 'text-lg font-semibold';
        text.textContent = calc.name;
        
        block.appendChild(text);
        grid.appendChild(block);
    });
};
