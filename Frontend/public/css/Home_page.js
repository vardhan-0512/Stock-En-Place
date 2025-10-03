document.getElementById('searchButton').addEventListener('click', () => {
    const query = document.getElementById('searchInput').value;

    if (query) {
        // This is where you would interact with your backend.
        // For example, you could redirect to a results page:
        // window.location.href = `/analysis?company=${encodeURIComponent(query)}`;
        
        console.log(`Searching for: ${query}`);
        alert(`Your backend will now search for a ticker for "${query}"`);
    } else {
        alert('Please enter a company name.');
    }
});