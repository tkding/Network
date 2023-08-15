const newPostFrom = document.getElementById('newPostForm')
const messageElement = document.getElementById('message')

newPostForm.addEventListener('submit', (e) => {
    e.preventDefault()
    const formData = new FormData(newPostForm)
    const message = formData.get('message')
    
    fetch('/posts', {
        method: 'POST',
        body: formData,
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': getCookie(csrf_token)
        }
    })
    .then((response) => response.json())
    .then((data) => {
        messageElement.textContent = data.message
        newPostForm.reset();
    })
    .catch((error) => {
        console.log('Error:', error);
    });
});

// function to get CSRF token from cookie
function getCookie(name){
    let cookieValue = null;
    if(document.cookie && document.cookie !== ''){
        const cookies = document.cookie.split(';');
        for(let i = 0; i < cookies.length; i++){
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if(cookie.substring(0, name.length + 1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}