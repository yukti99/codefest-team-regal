$(document).ready(function() {
    $("#search-referrals").autocomplete({
        source: referrals
    });
    displayReferrals(referrals);
});  

$(document).ready(function(){
    $("#search-referrals").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      console.log(value)
      $("#referral-table tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
});

function displayReferrals(referrals){
    $("#referral-table").empty();
    for (var r in referrals) {
        console.log(referrals[r]);
        createReferralTile(referrals[r]);
    }   
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
    div = '<td>'+ referral["client_status"] + "</td>";
    main_div.append(div) 

    $(main_div).click(function(){
        let pageURL = "http://127.0.0.1:5000/view_referral/"+referral["client_id"];
        document.location.href = pageURL;
    });
    $('#referral-table').append(main_div); 
}