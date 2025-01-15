async function login() {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token);
            console.log("JWT Token:", data.access_token);
            window.location.href = '/home';
            alert('Login successful');
        }
        else {
            alert(data.message);
        }
    }
    catch (error) {
        console.error('Error logging in:', error);
    }

}

async function register() {
    const username = document.getElementById("registerUsername").value;
    const password = document.getElementById("registerPassword").value;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        
        if (data.message === 'User created successfully') {
            window.location.href = '/';
            alert('Registration successful');
        }
        else {
            alert(data.message);
        }        
    }
    catch (error) {
        console.error('Error registering:', error);
    }
}