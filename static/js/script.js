document.addEventListener('DOMContentLoaded', function () {
    // Get references to the existing album select element and the title and artist input fields
    const existingAlbumSelect = document.querySelector('select[name="existing_album"]');
    const titleInput = document.querySelector('input[name="title"]');
    const artistInput = document.querySelector('input[name="artist"]');
    const imageUrlInput = document.querySelector('input[name="image_url"]');
    const descriptionInput = document.querySelector('textarea[name="description"]');

    // Hide the description and image URL input elements and their labels
    hideDescriptionAndImageUrl(descriptionInput, imageUrlInput);

    // Add an event listener to the existing album select element
    existingAlbumSelect.addEventListener('change', function () {
        const selectedAlbumId = this.value;
        if (selectedAlbumId) {
            // Fetch album details from the server if an album is selected
            fetch(`/api/albums/${selectedAlbumId}/`)
                .then(response => response.json())
                .then(data => {
                    // Populate the input fields with the fetched album details
                    titleInput.value = data.title;
                    artistInput.value = data.artist;
                    imageUrlInput.value = data.image_url;
                    descriptionInput.value = data.description;
                });
        } else {
            // Clear the input fields if no album is selected
            titleInput.value = '';
            artistInput.value = '';
            imageUrlInput.value = '';
            descriptionInput.value = '';
        }
    });
});

function hideDescriptionAndImageUrl(descriptionInput, imageUrlInput) {
    /**
     *  Function to hide the description and image URL input elements and their labels
     * @param {Element} descriptionInput - The description input element
     * @param {Element} imageUrlInput - The image URL input element
     * @returns {void}
     */
    descriptionInput.style.display = 'none';
    imageUrlInput.style.display = 'none';
    const descriptionLabel = document.querySelector('label[for="id_description"]');
    const imageUrlLabel = document.querySelector('label[for="id_image_url"]');
    if (descriptionLabel) descriptionLabel.style.display = 'none';
    if (imageUrlLabel) imageUrlLabel.style.display = 'none';
}


