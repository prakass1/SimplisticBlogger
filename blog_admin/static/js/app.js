import {add_post, delete_post, edit_post} from './posts_app.js';
import {approve_comment} from './comments_app.js';

$(document).ready(function(){
    $(".toast").toast("hide");
    $("#log").hide();
    $("#posts-dtable #comments-dtable").DataTable();
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
            },

            onMediaDelete: function(file){
                console.log("Filename to be deleted -- ", file[0].src);
                deleteImage(file[0].src);
            }
        }
      });

    // Loading data-tag
    $('input[name="categoryFormInput"]').amsifySuggestags({
        tagLimit: 4,
        trimValue: true,
        dashSpaces: true
	});

    function uploadImage(image){
        var csrftoken = $('meta[name=csrf-token]').attr('content');
        //Upload image via ajax
        $("#log").empty();
        $("#log").hide();
        var data = new FormData();
        var blog_title = $("#titleFormInput").val();

        //console.log(blog_title);
        //data = JSON.stringify({"image":image, "blog_title":blog_title});
        data.append("image", image);
       // data.append("blog_title", blog_title);
        $.ajax({
            url: "/image_upload",
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            type: "POST",
            beforeSend: function(xhr, settings){
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }

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


    function deleteImage(image){
        var csrftoken = $('meta[name=csrf-token]').attr('content');
        //Upload image via ajax
        $("#log").empty();
        $("#log").hide();
        $.ajax({
            url: "/image_delete",
            cache: false,
            processData: false,
            contentType: "application/json",
            data: JSON.stringify({"image_file":image}),
            type: "POST",

            beforeSend: function(xhr, settings){
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            },
            success: function(resp)
            {
                $("#log").empty();
                $("#log").append(resp);
                $("#log").show();
            },
            error: function(resp){
                console.log(resp);
                $("#log").empty();
                $("#log").append(resp);
                $("#log").show();
            }
        });
    }

    //Add a post to the database
    $("#add-form-post").on("submit", function(e){
        e.preventDefault();
        $("#log").hide();
        var blog_title = $("#titleFormInput").val();
        var blog_author = $("#authorFormInput").val();
        var blog_content = $('#summernote').summernote('code');
        var blog_tags = $("span.amsify-select-tag").get_items("items");

        add_post(blog_title, blog_author, blog_content, blog_tags);
    });

    //Edit the post and make changes
    $("#edit-form-post").on("submit",function(e){
        e.preventDefault();
        $("#log").hide();
        var blog_title = $("#edit_form_title").val();
        var old_title = $("#edit_form_old_title").val();
        var blog_content = $('#summernote').summernote('code');
        var blog_tags = $("span.amsify-select-tag").get_items("items");
        edit_post(blog_title, blog_content, old_title, blog_tags);
    });


    //delete the post
    $("#posts-dtable").on("click", ".delete-blogpost", function(e){
        e.preventDefault();
        var closest_tr = $(this).closest("tr");
        $("#log").hide();
        var blog_title = $(closest_tr).find("#post_id").text();
        //alert(blog_title);
        delete_post(blog_title, closest_tr);
    });

    //Change status of the comment
    $(".comment-status").on("change", function(e){
        var comment_status = this.value;
        var comment_ref_id = $(this).closest("tr").attr("id");
        //Settings
        if ($(".commentlog > strong").length > 0){
            $("strong").remove();
        }
        //approve comments
        approve_comment(comment_status, comment_ref_id);
    });

//End of document

});