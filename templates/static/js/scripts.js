document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            const username = document.querySelector('#username').value.trim();
            const password = document.querySelector('#password').value.trim();

            if (!username || !password) {
                event.preventDefault(); // Impede o envio do formulário
                alert('Please fill in both username and password!');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const quantityInputs = document.querySelectorAll('.quantity-input');

    quantityInputs.forEach(input => {
        input.addEventListener('change', (event) => {
            const productId = event.target.dataset.productId;
            const newQuantity = event.target.value;

            // Exemplo de requisição AJAX para atualizar o carrinho
            fetch(`/update-cart/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: newQuantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Cart updated successfully!');
                } else {
                    alert('Error updating cart.');
                }
            });
        });
    });
});
