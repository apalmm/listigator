function updateInput()
{
    $("#name").on("keyup", updateResults);
    $("#city").on("keyup", updateResults);
    $("#field").on("change", updateResults);
    $("#phone").on("keyup", updateResults);
    // $("#probono").on("change", updateResults);
}

function updateResults()
{
    let name = $("#name").val();
    let city = $("#city").val();
    let phone = $("#phone").val();
    let field = $("#field").val();

    if (field == '--Any--') {
        field = ''
    }

    //encodeURIComponent searchPrefix

    let url = "/search?name=" + name + "&" + "city=" + city + "&" + "phone=" + phone + "&" + "field=" + field //add on to flash route the prefix (aka whatever is in the search Prefix)

    console.log(url)

    request = $.ajax({
        type: "GET", //get request
        url: url,
        success: (response) => {
            $("#results").html(response); //put the response from the db into the results section of index.html (cause jquery is linked in the index.html file)
        }
    });
}

function setup()
{
    console.log('setup');
    updateInput();
}


$(document).ready(setup);