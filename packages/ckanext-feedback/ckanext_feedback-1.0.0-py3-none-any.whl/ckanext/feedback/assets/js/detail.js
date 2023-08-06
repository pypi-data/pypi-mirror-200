function checkCommentExists() {
  errorElement  = document.getElementById('content-error');
  content = document.getElementById('comment-content').value;

  if (content) {
    errorElement.style.display = 'none';
    return true;
  } else {
    errorElement.style.display = '';
    return false;
  }
}

function checkDescriptionExists() {
  errorElement = document.getElementById('description-error');
  description = document.getElementById('description').value;

  if (description) {
    errorElement.style.display = 'none';
    return true;
  } else {
    errorElement.style.display = '';
    return false;
  }
}