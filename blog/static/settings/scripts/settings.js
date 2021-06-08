function changeVariant(evt, el_id) {
    var prof = document.getElementById("profile-settings-variant");
    var security = document.getElementById("profile-security-settings-variant");

    if (el_id == "profile-settings-variant") {

        security.style.marginTop =  "0.25em"
        security.style.color= "#6b6b6b"

        prof.style.marginTop =  "0"
        prof.style.color= "mediumpurple"

        document.getElementById("security-settings-container").style.display = "none"
        document.getElementById("profile-settings-container").style.display = "inline"

    }

    else {
        prof.style.marginTop =  "0.25em"
        prof.style.color= "#6b6b6b"

        security.style.marginTop =  "0"
        security.style.color= "mediumpurple"

        document.getElementById("profile-settings-container").style.display = "none"
        document.getElementById("security-settings-container").style.display = "inline"
    }
}


function chooseAvatarImage() {
    document.getElementById("change-avatar-input").click()
}


$(document).on("change", "#change-avatar-input", function () {

    data = new FormData($('#change-avatar-super-form').get(0));

    $.ajax({
        url: '/ajax/change_avatar/',
        type: "POST",
        data: data,
        dataType: "json",
        processData: false,
        contentType: false,
        success: function (response) {
            
        },
        timeout: 10000,
    });
});