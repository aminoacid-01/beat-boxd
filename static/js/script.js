
    document.addEventListener('DOMContentLoaded', function () {
        // Get references to the existing album select element and the title and artist input fields
        const existingAlbumSelect = document.querySelector('select[name="existing_album"]');
    const titleInput = document.querySelector('input[name="title"]');
    const artistInput = document.querySelector('input[name="artist"]');
    const imageUrlInput = document.querySelector('input[name="image_url"]');
    const descriptionInput = document.querySelector('textarea[name="description"]');

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
            }
        });
    });