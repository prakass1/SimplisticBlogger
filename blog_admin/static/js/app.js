$(document).ready(function(){
    $("#log").hide();
    $("#posts-dtable").DataTable();
    //Loading the summernote
    $('#summernote').summernote({
        placeholder: 'Hello !!!',
        tabsize: 2,
        height: 300,
        minHeight:null,
        maxHeight:null,
        toolbar: [
          ['style', ['style']],
          ['font', ['bold', 'underline', 'clear']],
          ['color', ['color']],
          ['para', ['ul', 'ol', 'paragraph']],
          ['table', ['table']],
          ['insert', ['link', 'picture', 'video']],
          ['view', ['fullscreen', 'codeview', 'help']]
        ],
        callbacks: {
            onImageUpload: function(image){
                uploadImage(image[0]);
            }
        }
      });
    
    function uploadImage(image){
        //Upload image via ajax
        $("#log").empty();
        $("#log").hide();
        var data = new FormData();
        var blog_title = $("#titleFormInput").val();

        //console.log(blog_title);
        //data = JSON.stringify({"image":image, "blog_title":blog_title});
        data.append("image", image);
        data.append("blog_title", blog_title);
        $.ajax({
            url: "/image_upload",
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            type: "POST",
            beforeSend: function(){
                if (blog_title === ""){
                    $("#log").append("The title of the blog cannot be empty before uploading an image !!");
                    $("#log").show();
                    this.abort();
                }
            },
            success: function(filename)
            {
                $("#log").empty();
                $("#log").append("Successfully uploaded the file");
                $("#log").show();
                var image = $("<img>").attr("src",filename).addClass("img-fluid");
                $("#summernote").summernote("insertNode", image[0]);
            },
            error: function(data){
                console.log(data);
                $("#log").empty();
                $("#log").append(data);
                $("#log").show();
            }
        });
    }

//End of document      
});