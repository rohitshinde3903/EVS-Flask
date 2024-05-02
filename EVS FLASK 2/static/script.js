// JavaScript code for interactive elements

// Hover effect for buttons
const buttons = document.querySelectorAll('.btn');

buttons.forEach(button => {
    button.addEventListener('mouseenter', () => {
        button.style.backgroundColor = '#555'; // Darker gray button background on hover
    });

    button.addEventListener('mouseleave', () => {
        button.style.backgroundColor = '#333'; // Restore original button background color
    });
});
