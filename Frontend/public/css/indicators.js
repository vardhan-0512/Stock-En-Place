const indicators = [
            { id: 'block-1', name: 'Bollinger Bands', slug: 'bollinger-bands' },
            { id: 'block-2', name: 'RSI', slug: 'relative-strength-index' },
            { id: 'block-3', name: 'MACD', slug: 'macd' },
            { id: 'block-4', name: 'Moving Average', slug: 'moving-average' },
            { id: 'block-5', name: 'Stochastic Oscillator', slug: 'stochastic-oscillator' },
            { id: 'block-6', name: 'Fibonacci Retracement', slug: 'fibonacci-retracement' },
            { id: 'block-7', name: 'Ichimoku Cloud', slug: 'ichimoku-cloud' },
            { id: 'block-8', name: 'On-Balance Volume', slug: 'obv' },
            { id: 'block-9', name: 'ATR', slug: 'average-true-range' },
            { id: 'block-10', name: 'VWAP', slug: 'volume-weighted-avg-price' },
            { id: 'block-11', name: 'Parabolic SAR', slug: 'parabolic-sar' },
            { id: 'block-12', name: 'CCI', slug: 'commodity-channel-index' },
            { id: 'block-13', name: 'Momentum Indicator', slug: 'momentum' },
            { id: 'block-14', name: 'Williams %R', slug: 'williams-percent-range' },
            { id: 'block-15', name: 'Chaikin Money Flow', slug: 'chaikin-money-flow' },
            { id: 'block-16', name: 'Aroon Indicator', slug: 'aroon' },
            { id: 'block-17', name: 'Supertrend', slug: 'supertrend' },
            { id: 'block-18', name: 'Donchian Channels', slug: 'donchian-channels' },
            { id: 'block-19', name: 'Keltner Channels', slug: 'keltner-channels' },
            { id: 'block-20', name: 'Rate of Change', slug: 'roc' },
            { id: 'block-21', name: 'Standard Deviation', slug: 'standard-deviation' },
            { id: 'block-22', name: 'TRIX', slug: 'trix' },
            { id: 'block-23', name: 'Vortex Indicator', slug: 'vortex' },
            { id: 'block-24', name: 'Awesome Oscillator', slug: 'awesome-oscillator' },
            { id: 'block-25', name: 'Elder-Ray Index', slug: 'elder-ray' },
            { id: 'block-26', name: 'Force Index', slug: 'force-index' },
            { id: 'block-27', name: 'Gann Angles', slug: 'gann-angles' },
            { id: 'block-28', name: 'Pivot Points', slug: 'pivot-points' },
            { id: 'block-29', name: 'Zig Zag', slug: 'zig-zag' },
            { id: 'block-30', name: 'Coppock Curve', slug: 'coppock-curve' }
        ];

        // --- Logic to handle page setup and navigation ---
        window.onload = function() {
            // Get stock ticker from URL, default to 'AAPL' for demonstration
            const urlParams = new URLSearchParams(window.location.search);
            const ticker = urlParams.get('ticker') || 'AAPL';
            
            // Update page header
            document.getElementById('header-title').textContent = `Select an Indicator for ${ticker}`;

            const grid = document.getElementById('indicator-grid');

            // Generate the 30 blocks
            indicators.forEach(indicator => {
                const block = document.createElement('a');
                block.href = `split_screen_indicators.html?ticker=${ticker}&indicator=${indicator.slug}&name=${encodeURIComponent(indicator.name)}`;
                block.className = 'indicator-block bg-[#1e1e1e] border border-gray-700 rounded-xl p-6 text-center hover:border-white hover:scale-105 transition-all duration-300 flex items-center justify-center';
                block.dataset.indicator = indicator.slug; // Store slug in data attribute

                const text = document.createElement('span');
                text.className = 'text-lg font-semibold';
                text.textContent = indicator.name;
                
                block.appendChild(text);
                grid.appendChild(block);
            });
        };