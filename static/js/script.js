// get album form input elements
document.addEventListener('DOMContentLoaded', function () {
    const albumTitleInput = document.getElementById('id_title'); // Get the title input element
    const artistInput = document.getElementById('id_artist'); // Get the artist input element
    const imageUrlInput = document.getElementById('id_image_url'); // Get the image_url input element
    const descriptionInput = document.getElementById('id_description'); // Get the description input element
    const albumDropdown = document.getElementById('id_album_dropdown');  // Get the dropdown element

    hideDescriptionAndImageUrl(descriptionInput, imageUrlInput);
});

function hideDescriptionAndImageUrl(descriptionInput, imageUrlInput) {
    // Hide the description and image URL input elements
    descriptionInput.style.display = 'none';
    imageUrlInput.style.display = 'none';

    // Hide the labels for the description and image URL input elements
    const descriptionLabel = document.querySelector('label[for="id_description"]');
    const imageUrlLabel = document.querySelector('label[for="id_image_url"]');
    if (descriptionLabel) descriptionLabel.style.display = 'none';
    if (imageUrlLabel) imageUrlLabel.style.display = 'none';
}


