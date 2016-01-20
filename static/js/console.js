var userList = '';
var html_code_for_svn = '';
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
    console.log(html_code_for_svn);
    $("#parse_svn").append(html_code_for_svn);

    $(".menuLink").click(function (val) {
        username = $(val.target).text();
    });
});

function parseStuff(text) {
    userList = text;
}
