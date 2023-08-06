function checkTitleAndDescriptionExists() {
  const title = document.getElementById('title').value;
  const description = document.getElementById('description').value;
  const titleErrorElement = document.getElementById('title-error');
  const descriptionErrorElement = document.getElementById('description-error');

  // Reset display settings
  titleErrorElement.style.display = 'none';
  descriptionErrorElement.style.display = 'none';
  
  if (!title) {
    titleErrorElement.style.display = '';
    return false;
  }
  if (!description) {
    descriptionErrorElement.style.display = '';
    return false;
  }
  return true;
}

function confirmDelete() {
  const message = document.getElementById('message').value;
  return confirm(message)
}