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
                    // Hide the artist and title input elements and their labels
                    hideArtistAndAlbumInput(artistInput, titleInput);
                    // Populate the input fields with the fetched album details
                    titleInput.value = data.title;
                    artistInput.value = data.artist;
                    imageUrlInput.value = data.image_url;
                    descriptionInput.value = data.description;
                });
        } else {
            // Clear the input fields if no album is selected
            // call showArtistAndAlbumInput function to show the artist and title input elements and their labels
            showArtistAndAlbumInput(artistInput, titleInput);
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

function hideArtistAndAlbumInput(artistInput, titleInput) {
    /**
     * Function to hide the artist and title input elements and their labels
     * @param {Element} artistInput - The artist input element
     * @param {Element} titleInput - The title input element
     * @returns {void}
     */
    artistInput.style.display = 'none';
    titleInput.style.display = 'none';
    const artistLabel = document.querySelector('label[for="id_artist"]');
    const titleLabel = document.querySelector('label[for="id_title"]');
    if (artistLabel) artistLabel.style.display = 'none';
    if (titleLabel) titleLabel.style.display = 'none';
}

function showArtistAndAlbumInput(artistInput, titleInput) {
    /**
     * Function to show the artist and title input elements and their labels
     * @param {Element} artistInput - The artist input element
     * @param {Element} titleInput - The title input element
     * @returns {void}
     */
    artistInput.style.display = '';
    titleInput.style.display = '';
    const artistLabel = document.querySelector('label[for="id_artist"]');
    const titleLabel = document.querySelector('label[for="id_title"]');
    if (artistLabel) artistLabel.style.display = '';
    if (titleLabel) titleLabel.style.display = '';
}

