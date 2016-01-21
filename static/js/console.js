var userList = '';
var html_code_for_svn = '<li class="collection-header"><h5>Usernames</h5></li>';
var username = '';

$(document).ready(function () {
    $.each(userList, function (index, name) {
        //console.log(index + ": " + name);
        html_code_for_svn += "<li class='collection-item'><a id='" +
            index.toString() +
            "' class='menuLink'>" +
            name.toString() +
            "</a></li>\n";
    });
    //console.log(html_code_for_svn);
    $("#parse_svn").append(html_code_for_svn);

    $("#dynamic").on("click", "a.menuLink", function (val) {
        username = $(val.target).text();
        $("#parse_svn").empty();
        $("#parse_svn").append('<form action="/consolePage/svnMod" id="svnMod" class="col s12" method="post">' +
            '<div class="row">' +
            '<h5>' + username.toString() + '</h5>' +
            '<div class="input-field col s12">' +
            '<input name="username" type="hidden" value="' + username.toString() + '">' +
            '<input name="passwd" id="first_name" type="text" class="validate" required>' +
            '<label for="passwd">Password</label>' +
            '</div>' + '' +
            '</form>' +
            '<button id="resetDOM" class="col s5 waves-effect waves-light btn" type="button">Back</button>' +
            '<button style="float:right;"class="col s5 waves-effect waves-light btn" type="submit" form="svnMod" value="Submit">Submit</button>');
        $("#parse_svn").removeClass("with-header");
        $("#parse_svn").removeClass("collection");
    });

    $("#dynamic").on("click", "button#resetDOM", function () {
        $("#parse_svn").empty();
        $("#parse_svn").append(html_code_for_svn);
        $("#parse_svn").addClass("collection");
        $("#parse_svn").addClass("with-header");
    });

});

function parseStuff(text) {
    userList = text;
};