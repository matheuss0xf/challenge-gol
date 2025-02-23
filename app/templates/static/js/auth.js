document.addEventListener("DOMContentLoaded", function () {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));


    document.getElementById("registerForm").addEventListener("submit", function (event) {
        event.preventDefault();
        register().then(r => console.log(r)).catch(e => console.error(e));
    });
});

function showTooltip(element, message) {
    if (typeof bootstrap === "undefined") {
        console.error("Bootstrap não foi carregado corretamente!");
        return;
    }

    element.setAttribute("data-bs-original-title", message);

    let tooltip = new bootstrap.Tooltip(element, { trigger: 'manual' });
    tooltip.show();

    setTimeout(() => tooltip.dispose(), 3000);
}

async function login() {
    const email = document.getElementById('email');
    const password = document.getElementById('password');

    if (!email.value || !password.value) {
        showTooltip(email, "Por favor, preencha todos os campos.");
        return;
    }

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email.value, password: password.value }),
        });

        if (!response.ok) {
            const { error } = await response.json();
            throw new Error(error || "Login failed.");
        }

        const { user } = await response.json();
        localStorage.setItem('userName', user.name);
        window.location.href = '/dashboard';

    } catch (error) {
        showTooltip(email, 'Falha ao realizar login.');
    }
}

async function register() {
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');

    if (!name.value || !email.value || !password.value || !confirmPassword.value) {
        showTooltip(name, "Por favor, preencha todos os campos.");
        return;
    }

    if (password.value !== confirmPassword.value) {
        showTooltip(password, "As senhas não coincidem!");
        return;
    }

    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name.value, email: email.value, password: password.value }),
        });

        if (!response.ok) {
            const { error } = await response.json();
            throw new Error(error || "Registration failed.");
        }

        showTooltip(email, "Usuário registrado com sucesso! Redirecionando...");

        // Aguarda 2 segundos antes do redirecionamento
        setTimeout(() => {
            window.location.href = '/';
        }, 2000);

    } catch (error) {
        showTooltip(email, 'Falha ao registrar usuário.');
    }
}

function logout() {
    window.location.href = '/';
}

