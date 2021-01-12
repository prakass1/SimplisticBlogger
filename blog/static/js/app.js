import { add_comment } from './comments.js';

$(document).ready(function () {

    $("#load_more").on("click", function (e) {
        e.preventDefault();
        var prev_limit = $("#prev_limit").val();
        // GET more
        load_more(prev_limit);
    });

    function success_state(data_response) {
        $(".display-posts").append(data_response.posts_html_reponse);
        if (data_response.prev_limit > data_response.post_len) {
            $(".clearfix").remove();
        }
        else {
            $("input[name=prev_limit]").val(data_response.prev_limit);
        }

    }

    function load_more(prev_limit) {
        $.ajax({
            url: "/blog" + "?prev_limit=" + prev_limit,
            cache: false,
            processData: false,
            content: "application/json",
            type: "GET",
            success: function (data_response) {
                if (data_response.load_more) {
                    //Load the content of the post.
                    localStorage.setItem("response", data_response);
                    success_state(data_response);
                }
            },
            error: function (data_response) {
                //catch xhrs here
                if (data_response.load_more === false) {
                    console.log("loaded all posts");
                }
            }
        });
    }

    window.onpopstate = function (e) {
        var response = localStorage.getItem('response');
        success_state(response);
    }

    //Add Comment
    $("#add-form-comment").on("submit", function (e) {
        e.preventDefault();

        if ($("#log > strong").length > 0) {
            $("#log > strong").remove();
        }
        else {
            $("#add-comment").prepend(
                "<div style='display:none;' class='alert alert-warning alert-dismissible fade show' role='alert' id='log'>" +
                "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
                "<span aria-hidden='true'>&times;</span></button>" +
               "</div>"
            );
        }

        var author_name = $("#nameFormInput").val();
        var author_email = $("#emailFormInput").val();
        var author_comment = $('#commentForm').val();
        var g_recaptcha = $("#g-recaptcha-response").val();
        var blog_title = $(".post-heading > h1").text();

        add_comment(author_name, author_email, author_comment, g_recaptcha, blog_title);
    });


    // End of file
});