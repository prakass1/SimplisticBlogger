function add_comment(author_name, author_email, author_comment, g_recaptcha, blog_title) {
    //Upload image via ajax
    $("#log").hide();
    //var data = new FormData();
    var data = {
        "author_email": author_email,
        "author_name": author_name,
        "author_comment": author_comment,
        "g_recaptcha": g_recaptcha,
        "blog_title": blog_title
    };

    var csrftoken = $('meta[name=csrf-token]').attr('content');
    $.ajax({
        url: "/api/comment",
        cache: false,
        contentType: "application/json",
        processData: false,
        data: JSON.stringify(data),
        type: "POST",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }

            // Text processing to understand the comment type
            var comment_arr = author_comment.split(" ");
            if (author_name.length <= 3){
                $("<strong class='log-info'>The author name must be greater than 3 characters</strong>").prependTo("#log");
                $("#log").show().fadeOut(25000, "linear");
                this.abort();
            }

            else if (author_comment === "") {
                $("<strong class='log-info'>The comment cannot be empty!</strong>").prependTo("#log");
                $("#log").show().fadeOut(25000, "linear");
                this.abort();
            }

            else if (comment_arr.length <=3){
                $("<strong class='log-info'>The comment should atleast contain 3 or more words</strong>").prependTo("#log");
                $("#log").show().fadeOut(25000, "linear");
                this.abort();
            }

        },
        success: function (response) {
            $('<strong class="log-info">' + response + '</strong>').prependTo("#log");
            $("#log").show().fadeOut(25000,"linear");
            $('#add-form-comment')[0].reset();
        },
        error: function (data) {
            console.log(data);
            $('<strong class="log-info">' + data + '</strong>').prependTo("#log");
            $("#log").show().fadeOut(25000,"linear");
            $('#add-form-comment')[0].reset();
        }
    });
}


//Export functions to be imported in main wrapper
export { add_comment };