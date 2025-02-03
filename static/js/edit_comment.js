document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.edit-comment-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            this.nextElementSibling.classList.toggle('d-none');
        });
    });
});