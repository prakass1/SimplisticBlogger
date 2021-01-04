function approve_comment(comment_status, comment_ref_id) {
    //Upload image via ajax
    $("#log").empty();
    $("#log").hide();
    //var data = new FormData();
    var data = {
        "comment_status": comment_status,
        "comment_ref_id": comment_ref_id
    };

    var csrftoken = $('meta[name=csrf-token]').attr('content');
    $.ajax({
        url: "/api/comment",
        cache: false,
        contentType: "application/json",
        processData: false,
        data: JSON.stringify(data),
        type: "PUT",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }

            if (comment_status === "" || comment_ref_id === "") {
                $("#log").append("Empty payload, aborting request!!");
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
export { approve_comment };