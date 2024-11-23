document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('signup-modal').style.display = 'none';
    document.getElementById('login-modal').style.display = 'none';

    const mainButton = document.querySelector('.btn-main');

    if (mainButton) {
        mainButton.addEventListener('click', function (e) {
            const isLoggedIn = mainButton.getAttribute('data-logged-in') === 'true';
            e.preventDefault();
            if (isLoggedIn) {
                const signupModal = document.getElementById('signup-modal');
                if (signupModal) {
                    signupModal.style.display = 'none';
                }
                window.location.href = '/ai_assistant';
            } else {
                const signupModal = document.getElementById('signup-modal');
                if (signupModal) {
                    signupModal.style.display = 'block';
                }
            }
        });
    }
});

function resetForms() {
    const signupModal = document.getElementById('signup-modal');
    const loginModal = document.getElementById('login-modal');

    if (signupModal) {
        const signupFields = signupModal.querySelectorAll('input');
        signupFields.forEach(field => {
            field.value = '';
        });

        const signupMessage = signupModal.querySelector('.signup-message');
        if (signupMessage) {
            signupMessage.textContent = '';
        }
    }

    if (loginModal) {
        const loginFields = loginModal.querySelectorAll('input');
        loginFields.forEach(field => {
            field.value = '';
        });

        const loginMessage = loginModal.querySelector('#login-message');
        if (loginMessage) {
            loginMessage.textContent = '';
        }
    }
}

window.addEventListener('pageshow', function (event) {
    if (event.persisted) {
        document.getElementById('signup-modal').style.display = 'none';
        document.getElementById('login-modal').style.display = 'none';
        resetForms();
    }
});

document.querySelectorAll('.btn-signup, .btn-main').forEach(function (button) {
    button.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('signup-modal').style.display = 'block';
    });
});

document.querySelector('.modal-close-signup').addEventListener('click', function () {
    document.getElementById('signup-modal').style.display = 'none';
    resetForms();
});

document.querySelectorAll('.btn-login').forEach(function (button) {
    button.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('login-modal').style.display = 'block';
    });
});

document.querySelector('.modal-close-login').addEventListener('click', function () {
    document.getElementById('login-modal').style.display = 'none';
    resetForms();
});

document.getElementById('switch-to-signup').addEventListener('click', function () {
    document.getElementById('login-modal').style.display = 'none';
    resetForms();
    document.getElementById('signup-modal').style.display = 'block';
});

document.getElementById('switch-to-login').addEventListener('click', function () {
    document.getElementById('signup-modal').style.display = 'none';
    resetForms();
    document.getElementById('login-modal').style.display = 'block';
});

document.querySelector('.btn-logout')?.addEventListener('click', async (event) => {
    event.preventDefault();
    const response = await fetch('/logout', { method: 'POST' });
    if (response.ok) {
        location.reload();
    } else {
        alert('Error logging out. Please try again.');
    }
});
