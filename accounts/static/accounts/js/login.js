document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(loginForm);
        const data = {
            username: formData.get('username'),
            password: formData.get('password'),
        };
        
        axios.post('/api/accounts/api/login/', data)
            .then(function(response) {
                const accessToken = response.data.access;
                const refreshToken = response.data.refresh;

                axios.post('/api/accounts/store_tokens/', {
                    access: accessToken,
                    refresh: refreshToken,
                }, {
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                    }
                })
                .then(function(storeResponse) {
                    alert('로그인 성공!')
                    window.location.href = '/';
                })
                .catch(function(storeError) {
                    console.error(storeError);
                    console.log('Tokenerror: ', storeError);
                });
            })
            .catch(function(error) {
                console.error(error);
                console.log('Loginerror: ', error);
            }) 
    })
})