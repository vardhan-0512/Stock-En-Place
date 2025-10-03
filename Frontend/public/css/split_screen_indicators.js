// Initialize AOS
        AOS.init({
            duration: 800,
            once: true,
            offset: 50,
        });

        // --- Mock Data ---
        const stockData = {
            "AAPL": { name: "Apple Inc." },
            "TSLA": { name: "Tesla, Inc." },
            "GOOGL": { name: "Alphabet Inc." },
            "DEFAULT": { name: "Stock Ticker" }
        };
        
        const indicatorAnalysis = {
            'bollinger-bands': 'Bollinger Bands are widening, suggesting increased volatility. The price is currently touching the upper band, which could indicate an overbought condition.',
            'relative-strength-index': 'The Relative Strength Index (RSI) is at 62, indicating bullish momentum but approaching overbought territory. Caution is advised.',
            'macd': 'The MACD line has recently crossed above the signal line, a common bullish indicator suggesting upward momentum may continue.',
            'default': 'This is a general analysis. Please select a specific indicator for a more detailed summary.'
        };

        // --- Page Setup Logic ---
        window.onload = function() {
            const urlParams = new URLSearchParams(window.location.search);
            const ticker = urlParams.get('ticker') || 'STOCK';
            const indicatorSlug = urlParams.get('indicator') || 'default';
            const indicatorName = urlParams.get('name') || 'Analysis';

            const stockInfo = stockData[ticker.toUpperCase()] || stockData['DEFAULT'];
            const analysisText = indicatorAnalysis[indicatorSlug] || indicatorAnalysis['default'];

            // Populate header and titles
            document.getElementById('page-title').textContent = `${ticker}: ${indicatorName}`;
            document.getElementById('stock-fullname-header').textContent = stockInfo.name;
            document.getElementById('chart-title').textContent = `${indicatorName} Chart`;
            document.getElementById('ai-title').textContent = `AI Analysis: ${indicatorName}`;

            // Set back button link to navigate to the indicator selection page
            document.getElementById('back-button').href = `indicator-selection-page.html?ticker=${ticker}`;
            
            // Add the initial, dynamic AI message
            addMessage(analysisText, 'ai');
        };

        // --- Chat UI Logic ---
        const chatForm = document.getElementById('chat-form');
        const chatInput = document.getElementById('chat-input');
        const chatWindow = document.getElementById('chat-window');

        chatForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const userMessage = chatInput.value.trim();
            if (userMessage) {
                addMessage(userMessage, 'user');
                chatInput.value = '';
                chatWindow.scrollTop = chatWindow.scrollHeight;
                setTimeout(() => {
                    const aiResponse = `This is a simulated AI response regarding "${userMessage}". A real LLM would provide a detailed answer here.`;
                    addMessage(aiResponse, 'ai');
                    chatWindow.scrollTop = chatWindow.scrollHeight;
                }, 1000);
            }
        });

        function addMessage(message, sender) {
    const messageWrapper = document.createElement('div');
    const messageBubble = document.createElement('div');
    messageWrapper.classList.add('flex', 'w-full');
    messageBubble.classList.add(
        'p-3',
        'rounded-lg',
        'max-w-md',
        'text-sm',
        'border',
        'transition-all',
        'duration-300'
    );

    if (sender === 'user') {
        // User messages (right side)
        messageWrapper.classList.add('justify-end');
        messageBubble.classList.add(
            'bg-[#1e1e1e]',
            'border-gray-700',
            'text-white',
            'hover:border-white'
        );
    } else {
        // AI messages (left side)
        messageWrapper.classList.add('justify-start');
        messageBubble.classList.add(
            'bg-[#1e1e1e]',
            'border-gray-700',
            'text-gray-200',
            'hover:border-white'
        );
    }

    messageBubble.textContent = message;
    messageWrapper.appendChild(messageBubble);
    chatWindow.appendChild(messageWrapper);
}
