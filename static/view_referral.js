$(document).ready(function() {
    console.log(client)
    displayClientDetails(client);
});

function displayClientDetails(info){
    console.log("info");
    console.log(info);
    let main_div = $('<form>');
    let row1 = $('<div class="row mb-4">')
    let div1 = $('<div class="col"><div class="form-outline"><label class="form-label">First name: <div id="details">'+info.first_name+'</div></label></div>');
    let div2 = $('<div class="col"><div class="form-outline"><label class="form-label">Last name: <div id="details">'+info.last_name+'</div></label></div>');
    
    row1.append(div1);
    row1.append(div2);

    let row2 = $('<div class="form-outline mb-4">')
    div1 = $('<label class="form-label">Address<div id="details">'+info.address+'</div></label>')
    row2.append(div1);

    let row3 = $('<div class="row mb-4">')
    div1 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label">Date of Birth<div id="details">'+info.date_of_birth+'</div></label></div></div>')
    div2 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label">NHS number<div id="details">'+info.nhs_number+'</div></label></div></div>')
    row3.append(div1);
    row3.append(div2);

    div1 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label">Email<div id="details">'+info.email+'</div></label></div></div>')
    div2 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label">Phone<div id="details">'+info.phone_number+'</div></label></div></div>')
    row3.append(div1);
    row3.append(div2);
    div2 = $(' <label class="form-label">Difficulty(s)<div id="details">'+info.issue_desc+'</div></label>')

    main_div.append(row1);
    main_div.append(row2);
    main_div.append(row3);
    main_div.append(div2);
    $("#client_details-div").append(main_div);

}

                    