document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btn-login').addEventListener('click', function(event) {
        event.preventDefault();

        const email = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value.trim();
        const loginMessage = document.getElementById('login-message');

        if (!email || !password) {
            loginMessage.textContent = 'Email and Password are required.';
            loginMessage.style.color = 'red';
            loginMessage.style.fontWeight = 'bold';
            return;
        }

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        })
        .then(response => {
            console.log(`Response status: ${response.status}`);
            if (response.status === 200) {
                return response.json();
            } else if (response.status === 401) {
                throw new Error('Invalid email or password');
            } else {
                throw new Error(`Unexpected error: Status ${response.status}`);
            }
        })
        .then(data => {
            loginMessage.textContent = 'Login successful!';
            loginMessage.style.color = 'green';
            loginMessage.style.fontWeight = 'bold';
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            loginMessage.textContent = error.message;
            loginMessage.style.color = 'red';
            loginMessage.style.fontWeight = 'bold';
        });
    });
});
