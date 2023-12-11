$(document).ready(function() {
    $('#searchTab').click(function() {
        $('#uploadSection').hide();
        $('#searchSection').show();
    });

    $('#uploadTab').click(function() {
        $('#searchSection').hide();
        $('#uploadSection').show();
    });

    $('#searchBtn').click(function() {

        const query = $('#searchQuery').val();
        var xhr = new XMLHttpRequest();
        xhr.withCredentials = false;

        xhr.addEventListener("readystatechange", function() {
            if(this.readyState === 4) {
                var urls = JSON.parse(this.responseText)['photo_urls'];

                urls.forEach(img_url => {
                    const imageElement = `
                        <div class="col-md-4 mb-3">
                            <img src="${img_url}" class="img-fluid">
                        </div>`;
                    $('#searchResults').append(imageElement);
                });
            }
        });

        xhr.open("GET", `https://70frjwcsk7.execute-api.us-east-1.amazonaws.com/test/search?q=${query}`);
        xhr.send(null);
    });

    $('#uploadBtn').click(function() {
        const photo = $('#photoUpload')[0].files[0];
        const description = $('#photoDescription').val();

        var xhr = new XMLHttpRequest();
        xhr.withCredentials = false;

        xhr.addEventListener("readystatechange", function() {
            if(this.readyState === 4 && this.status == 200) {
                console.log(this.responseText);
            }
        });

        xhr.open("PUT", `https://70frjwcsk7.execute-api.us-east-1.amazonaws.com/test/upload?key=${photo.name}`);
        xhr.setRequestHeader("x-amz-meta-customLabels", description);
        xhr.setRequestHeader("Content-Type", "image/jpeg");

        xhr.send(photo);
    });
});