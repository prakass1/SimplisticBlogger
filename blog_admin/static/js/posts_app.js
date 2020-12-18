function add_post(blog_title, blog_author, blog_content, blog_tags) {
    //Upload image via ajax
    $("#log").empty();
    $("#log").hide();
    //var data = new FormData();
    var data = {
        "blog_title": blog_title,
        "blog_author": blog_author,
        "blog_content": blog_content,
        "blog_tags": blog_tags
    };
    //data.append("blog_title", blog_title);
    //data.append("blog_author", blog_author);
    //data.append("blog_content", blog_content)
    var csrftoken = $('meta[name=csrf-token]').attr('content');
    $.ajax({
        url: "/api/post",
        cache: false,
        contentType: "application/json",
        processData: false,
        data: JSON.stringify(data),
        type: "POST",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }

            if (blog_title === "") {
                $("#log").append("The title of the blog cannot be empty before uploading an image !!");
                $("#log").show().fadeOut(3000, "linear");
                this.abort();
            }

        },
        success: function (response) {
            $("#log").empty();
            //$("#log").append(response);
            //$("#log").show();
            window.location.replace(response.redirect_uri)
        },
        error: function (data) {
            console.log(data);
            $("#log").empty();
            $("#log").append(data);
            $("#log").show().fadeOut(3000,"linear");
        }
    });
}

function view_post() {


}


function delete_post(blog_title, closest_tr) {
    //Upload image via ajax
    $("#log").empty();
    $("#log").hide();
    //var data = new FormData();
    var data = {
        "blog_title": blog_title
    };

    var csrftoken = $('meta[name=csrf-token]').attr('content');
    $.ajax({
        url: "/api/post",
        cache: false,
        contentType: "application/json",
        processData: false,
        data: JSON.stringify(data),
        type: "DELETE",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }

        },
        success: function (response) {
            closest_tr.remove();
            $("#log").empty();
            $("#log").append(response);
            $("#log").show().fadeOut(3000,"linear");
        },
        error: function (data) {
            console.log(data);
            $("#log").empty();
            $("#log").append(data);
            $("#log").show().fadeOut(3000,"linear");
        }
    });

}


function edit_post(blog_title, blog_content, old_title, blog_tags) {
    //Upload image via ajax
    $("#log").empty();
    $("#log").hide();
    //var data = new FormData();
    var data = {
        "blog_title": blog_title,
        "blog_content": blog_content,
        "old_title": old_title,
        "blog_tags": blog_tags
    };

    var csrftoken = $('meta[name=csrf-token]').attr('content');
    $.ajax({
        url: "/api/post",
        cache: false,
        contentType: "application/json",
        processData: false,
        data: JSON.stringify(data),
        type: "PUT",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }

            if (blog_title === "" || blog_content === "") {
                $("#log").append("The title of the blog cannot be empty!!");
                $("#log").show();
                this.abort();
            }

        },
        success: function (response) {
            $("#log").empty();
            $("#log").append(response);
            $("#log").show();
        },
        error: function (data) {
            console.log(data);
            $("#log").empty();
            $("#log").append(data);
            $("#log").show();
        }
    });

}

//Export functions to be imported in main wrapper
export { add_post, delete_post, view_post, edit_post };