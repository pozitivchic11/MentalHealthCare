document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btn-signup').addEventListener('click', function() {
        const name = document.getElementById('name').value.trim();
        const surname = document.getElementById('surname').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        const formMessage = document.getElementById('form-message');

        if (!name || !email || !password) {
            formMessage.textContent = 'Fields marked with * cannot be empty.';
            formMessage.style.color = 'red';
            formMessage.style.fontWeight = 'bold';
            return;
        }

        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, surname, email, password })
        })
        .then(response => {
            if (response.status === 400) {
                throw new Error('Account with this email already exists');
            } else if (response.status === 201) {
                return response.json();
            } else {
                throw new Error('An unexpected error occurred');
            }
        })
        .then(data => {
            console.log(data);

            formMessage.textContent = 'Account successfully created!';
            formMessage.style.color = 'green';
            formMessage.style.fontWeight = 'bold';
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);

            if (error.message === 'Account with this email already exists') {
                formMessage.textContent = 'Error: Account with this email already exists.';
            } else {
                formMessage.textContent = 'Error: Could not complete the sign-up process.';
            }
            formMessage.style.color = 'red';
            formMessage.style.fontWeight = 'bold';
        });
    });
});
