$('#autoresizing').on('input', function () {
    this.style.height = 'auto';
     
    if (this.scrollHeight < 220) {
    this.style.height =
            (this.scrollHeight) + 'px';
    }
    else {
        this.style.height =
        220 + 'px';
    }
});

function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function(e) {
        var image = document.createElement('img');
        image.id = "post-photo-preview";
        var photos_block = document.getElementById("post-photos");
        photos_block.appendChild(image);


        $('#post-photo-preview').attr('src', e.target.result);
      }
  
      reader.readAsDataURL(input.files[0]);
    }
  }
 
  
  $("#add-photo-field").change(function() {
    readURL(this);
  });
