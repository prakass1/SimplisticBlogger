function approve_comment(comment_status, comment_ref_id) {
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
                $('<strong>' + "Empty payload, aborting request!!" + "</strong>").prependTo(".commentlog");
                $(".toast").toast("show");
                this.abort();
            }

        },
        success: function (response) {
            if (response.resp){
                $('<strong>' + response.message + '</strong>').prependTo(".commentlog");
                $(".toast").toast("show");
                $("#" + comment_ref_id).remove();
                temp_val = $("#comment-badge").text();
                new_val = Integer.parseInt(temp_val) - 1;
                if (new_val > 0){
                    $("#comment-badge").text(new_val);
                }
                else{
                    $("a.notification").remove();
                }
                
            }
            else{
                $('<strong>' + response.message + '</strong>').prependTo(".commentlog");
                $(".toast").toast("show");
            }
            
        },
        error: function (response) {
            console.log(data);
            $('<strong">' + response.message + '</strong>').prependTo(".commentlog");
            $(".toast").toast("show");
        }
    });

}

//Export functions to be imported in main wrapper
export { approve_comment };