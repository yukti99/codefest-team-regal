$(document).ready(function() {
    console.log(client)
    displayClientDetails(client);
});

function displayClientDetails(info){
    console.log("info");
    console.log(info);
    let main_div = $('<form method="POST" action="/admit_client">');
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
    div2 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label">NHS number<div id="details">'+info.nsh_number+'</div></label></div></div>')
    row3.append(div1);
    row3.append(div2);

    div2 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label">Phone<div id="details">'+info.phone_number+'</div></label></div></div>')
    row3.append(div2);
    difficulty_div = $('<label id="difficulty-header" class="form-label">Difficulty(s)</label>')
    
    for (var d in info.issues){
        print("hbdcjkdsncdjn")
        console.log(info.issues)
        var c = d+1
        var sub_div = $('<div class="col issue-table">')
        div1 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label-small">Issue Type<div id="details">'+info.issues[d].issue_type+'</div></label></div></div>')
        div2 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label-small">Issue Description<div id="details">'+info.issues[d].issue_desc+'</div></label></div></div>')
        if (info.issues[d].therapist_id != -1){
            div3 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label-small">Issue Therapist<div id="details">'+info.issues[d].therapist_name+'</div></label></div></div>')
        }else{
            div3 = $('<div class="col"><div class="form-outline sm-1"><label class="form-label-small">Issue Therapist<div id="details"></div></label></div></div>')
            btn_div = '<button id="update-therapist-btn" type="submit" class="btn btn-primary">Update</button>'
            let form_div = $('<form method="POST" action="/edit_therapist"><input type="text" placeholder="please update" id="therapist-input" name="therapist-name" class="form-control"/><input type="text" name="issue_id_submit" value="'+info.issues[d].issue_id+'" hidden>')
            form_div.append(btn_div)
            div3.append(form_div)
        }
        sub_div.append(div1)
        sub_div.append(div2)
        sub_div.append(div3)

        difficulty_div.append(sub_div)
        
    }
    
    difficulty_div.append('</label>')


    main_div.append(row1);
    main_div.append(row2);
    main_div.append(row3);
    $("#difficulty-header").text("Difficulty(s)");
    main_div.append(difficulty_div);
    btn_div = '<th><button id="admit-btn" type="submit" class="btn btn-success">Admit<input type="text" name="client_id_submit" value="'+info.issues[d].client_id+'" hidden></button></th>'
    main_div.append(btn_div)


    $("#client_details-div").append(main_div);

    

}

                    