document.addEventListener('DOMContentLoaded', function() {
    const display = document.getElementById('display');
    const buttons = document.querySelectorAll('button');
    
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            if (button.classList.contains('clear')) {
                // Clear the display
                display.value = '';
            } else if (button.classList.contains('equals')) {
                // Calculate the result
                try {
                    calculateResult();
                } catch (error) {
                    display.value = 'Error';
                }
            } else if (button.classList.contains('backspace')) {
                // Delete the last character
                display.value = display.value.slice(0, -1);
            } else if (button.classList.contains('function')) {
                // Add function name and opening parenthesis
                display.value += button.textContent + '(';
            } else {
                // Add the button's text to the display
                display.value += button.textContent;
            }
        });
    });
    
    // Add keyboard support
    document.addEventListener('keydown', (event) => {
        const key = event.key;
        
        if (key >= '0' && key <= '9' || key === '.' || key === '+' || key === '-' || 
            key === '*' || key === '/' || key === '(' || key === ')' || key === '^') {
            display.value += key;
        } else if (key === 'Enter') {
            calculateResult();
        } else if (key === 'Backspace') {
            display.value = display.value.slice(0, -1);
        } else if (key === 'Escape') {
            display.value = '';
        }
    });
    
    function calculateResult() {
        const expression = display.value;
        
        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expression })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                display.value = 'Error: ' + data.error;
            } else {
                display.value = data.result;
            }
        })
        .catch(error => {
            display.value = 'Error';
            console.error('Calculation error:', error);
        });
    }
});