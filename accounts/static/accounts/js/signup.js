document.addEventListener("DOMContentLoaded", function () {
  const signupForm = document.getElementById("signup-form");
  if (!signupForm) {
    console.error("회원가입 폼이 존재하지 않습니다.");
    return;
  }

  signupForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(signupForm);
    const data = {
      username: formData.get("username"),
      first_name: formData.get("first_name"),
      last_name: formData.get("last_name"),
      email: formData.get("email"),
      password: formData.get("password"),
      nickname: formData.get("nickname"),
      gender: formData.get("gender"),
      age: formData.get("age"),
    };
    const imageFile = formData.get("image");
    if (imageFile.size > 0) {
      data.image = imageFile;
    }

    const csrfToken = getCsrfToken();

    axios.post('/api/accounts/api/signup/', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        alert('회원가입 성공!')
    })
    .catch(error => {
        console.error(error);
        console.log(error);
    })
  });
});
