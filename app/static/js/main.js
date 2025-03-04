// dark or light theme
const iconSwitchTheme = document.getElementById('iconSwitchTheme');
const btnSwitchTheme = document.getElementById('btnSwitchTheme');

const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-bs-theme', savedTheme);
if (savedTheme === 'dark') {
    iconSwitchTheme.classList.remove('bi-moon');
    iconSwitchTheme.classList.add('bi-sun');
} else {
    iconSwitchTheme.classList.remove('bi-sun');
    iconSwitchTheme.classList.add('bi-moon');
}

btnSwitchTheme.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    if (newTheme === 'dark') {
        iconSwitchTheme.classList.remove('bi-moon');
        iconSwitchTheme.classList.add('bi-sun');
    } else {
        iconSwitchTheme.classList.remove('bi-sun');
        iconSwitchTheme.classList.add('bi-moon');
    }
});

// htmx error handling
document.body.addEventListener('htmx:error', function(event) {
    let toastBody = document.querySelector("#error-toast .toast-body");
    toastBody.textContent = `${JSON.parse(event.detail.errorInfo.xhr.response).detail}`;

    let toast = new bootstrap.Toast(document.getElementById("error-toast"));
    toast.show();
});

// htmx success handling
document.body.addEventListener('htmx:afterRequest', function(event) {
    try {
        let data = JSON.parse(event.detail.xhr.response);
        let toastBody = document.querySelector("#success-toast .toast-body");
        if (data.toast) {
            toastBody.textContent = `${data.message}`;
    
            let toast = new bootstrap.Toast(document.getElementById("success-toast"));
            toast.show();
        }
    } catch (warn) {
        console.warn("Not trigger toast:", warn)
    }
});