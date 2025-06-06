// Registration
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams(formData)
        });

        if (response.ok) {
            alert("registration successful");
            window.location.href = '/login';
        } else {
            alert(await response.text());
        }
    } catch (error) {
        alert('Registration failed');
    }
});

// Login
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams(formData)
        });

        if (response.ok) {
            window.location.href = '/home';
            alert("login successful welcome");
        } else {
            alert(await response.text());
        }
    } catch (error) {
        alert('Login failed');
    }
});

// Embed Page
document.getElementById('imageInput')?.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Allowed image file types
    const allowedExtensions = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp'];

    // Validate file type
    if (!allowedExtensions.includes(file.type)) {
        alert('Invalid file, please select an image');
        e.target.value = ''; // Clear the input
        return;
    }

    // Proceed with existing logic if the file is valid
    const formData = new FormData();
    formData.append('image', file);

    fetch('/capacity', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.capacity) {
            document.getElementById('capacityValue').textContent = data.capacity;
            document.getElementById('capacityInfo').classList.remove('hidden');
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(() => {
        alert('Capacity check failed');
    });
});

document.getElementById('embedForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    // File type validation
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    const allowedExtensions = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp'];

    if (!file || !allowedExtensions.includes(file.type)) {
        alert('Invalid file type. Please upload an image file (PNG, JPEG, JPG, BMP).');
        return; // Stop form submission
    }

    const formData = new FormData(e.target);

    try {
        const response = await fetch('/embed', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'secret.png';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            alert(await response.text());
        }
    } catch (error) {
        alert('Embedding failed');
    }
});

// Extract Page
document.getElementById('extractForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    try {
        const response = await fetch('/extract', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        if (response.ok) {
            document.getElementById('messageContent').textContent = result.message;
            document.getElementById('result').classList.remove('hidden');
        } else {
            alert(result.error || 'Extraction failed');
        }
    } catch (error) {
        alert('Extraction failed');
    }
});