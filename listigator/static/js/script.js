let list_data = [[]];

function updateInput()
{
    let list_div = document.getElementById('list-content');

    $("#name").on("keyup", updateResults);
    $("#city").on("keyup", updateResults);
    $("#field").on("change", updateResults);
    $("#phone").on("keyup", updateResults);
    $("#state").on("change", updateResults);

    document.getElementById('new-list-btn').addEventListener('click', () => {
        if (list_div.style.display === 'none') {
            list_div.style.display = 'block';
        } else {
            list_div.style.display = 'none'
        }
    })

    document.getElementById('create-list-btn').addEventListener('click', () => {
        const title = document.getElementById('list-title').value;
        if (list_data.length > 0 && title) {
            //give our list a title
            list_data.push(title)
            
            let url = "/create";
            request = $.ajax({
                type: "POST",
                url: url,
                data: JSON.stringify(list_data),
                contentType: "application/json",
                success: (response) => {
                    console.log(response)
                },

            });
            list_data = [[]]

            //clear the DOM node
    
            const myNode = document.getElementById("lawyers-table-content");
            while (myNode.firstChild) {
                myNode.removeChild(myNode.lastChild);
            }
    
            //clear the list
            document.getElementById('list-title').value = ''
        }
    })
}

function setUpTable()
{
    const buttons = $(".lawyer-add-button");

    //for everything in the table essentially
    function clickCallback() {

        //on click
        var parent = $(this).parent("td").parent("tr");

        var name = parent.children(".name").text();
        var city = parent.children(".city").text();
        var field = parent.children(".field").text();
        var phone = parent.children(".phone").text();
        var license = parent.children(".license-no").text();

        const vals = [name, city, field, phone, license];

        const obj = {
            name: name,
            city: city,
            field: field,
            phone: phone,
            license: license,
        }

        const tr = document.createElement('tr');

        for(let i=0; i<5; i++) {
            let td = tr.appendChild(document.createElement('td'));
            td.textContent = vals[i]
        }

        list_data[0].push(obj);

        document.getElementById('lawyers-table-content').appendChild(tr);
    }

    buttons.on("click", clickCallback);
}

function updateResults()
{
    let name = $("#name").val();
    let city = $("#city").val();
    let phone = $("#phone").val();
    let field = $("#field").val();
    let state = $("#state").val();

    if (field == '--Any--') {
        field = ''
    }

    //encodeURIComponent searchPrefix

    let url = "/search?name=" + name + "&" + "city=" + city + "&" + "phone=" + phone + "&" + "field=" + field + "&state=" + state; //add on to flash route the prefix (aka whatever is in the search Prefix)

    request = $.ajax({
        type: "GET", //get request
        url: url,
        success: (response) => {
            $("#results").html(response); //put the response from the db into the results section of index.html (cause jquery is linked in the index.html file)
            setUpTable();
        }
    });
}

function setup()
{
    updateInput();
}


$(document).ready(setup);