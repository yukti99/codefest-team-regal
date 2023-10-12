function filter_difficulty() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("difficulty-dropdown");
    filter = input.value.toUpperCase();
    table = document.getElementById("client-table");
    tr = table.getElementsByTagName("tr");
    if (filter == "ALL"){
      displayReferrals(referrals);
      return
    }
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display =   "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

$(document).ready(function() {
    $("#search-referrals").autocomplete({
        source: referrals
    });
    displayReferrals(referrals);
});  

$(document).ready(function(){
    $("#search-referrals").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#referral-table tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
});

function displayReferrals(referrals){
    $("#referral-table").empty();
    for (var r in referrals) {
        createReferralTile(referrals[r]);
    }   
}

function makeid() {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    let length = 8;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

function createReferralTile(referral){
    let main_div = $('<tr id="referral-row">');
    // for (var r in referral) {
    //     div = '<td>'+ referral[r] + "</td>";
    //     main_div.append(div) 
    // }
    div = '<td>'+ referral["first_name"] + "</td>";
    main_div.append(div) 
    div = '<td>'+ referral["last_name"] + "</td>";
    main_div.append(div) 
    div = '<td>'+ referral["date_of_birth"] + "</td>";
    main_div.append(div) 
    div = '<td>'+ referral["postal_code"] + "</td>";
    main_div.append(div)
    div = '<td>'+ referral["issue_type"] + "</td>";
    main_div.append(div)  
    div = '<td>'+ makeid() + "</td>";
    main_div.append(div)  
    div = '<td>'+ referral["client_status"] + "</td>";
    main_div.append(div)  
    // div = '<td><button id="admit-btn" type="button" class="btn btn-success">Admit</button></td>'
    // main_div.append(div)  

    // var diff = ""
    // for (var i in referral["issues"]){
    //     diff+=referral["issues"][i].issue_desc+", "
    // }
    // console.log(diff)
    // div = '<td>'+ diff + "</td>";
    // main_div.append(div) 

    // div = '<td><button id="admit-btn" type="button" class="btn btn-success">Admit</button></td>'
    // main_div.append(div) 

    $(main_div).click(function(){
        let pageURL = "http://127.0.0.1:5000/view_referral/"+referral["client_id"];
        document.location.href = pageURL;
    });
    $('#referral-table').append(main_div); 
}