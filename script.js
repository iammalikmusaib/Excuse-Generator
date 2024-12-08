document.getElementById('generateExcuse').addEventListener('click', async () => {
    const topic = document.getElementById('topic').value.trim();
    const output = document.getElementById('excuseOutput');

    // Check if the input is empty
    if (!topic) {
        output.textContent = 'Please enter a topic to generate an excuse.';
        return;
    }

    output.textContent = 'Generating...';

    try {
        const response = await fetch('/generate_excuse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic }),
        });

        if (response.ok) {
            const data = await response.json();
            output.textContent = data.excuse || 'No excuse found!';
        } else {
            output.textContent = 'Error: Could not fetch excuse!';
        }
    } catch (error) {
        output.textContent = 'Error: Something went wrong!';
        console.error(error);
    }
});
