$(document).ready(function () {
   $("form").submit(function(e){
        e.preventDefault();
        if ($("#passwd1").val() != $("#passwd2").val()) {
            alert("not equal!");
            $("#passwd1").val("");
            $("#passwd2").val("");
            return;
        } else {
            var form_data = $("#register-form").serialize(); 
            $.post("/register", form_data, function (data) {
                var obj = JSON.parse(data);
                if (obj.status == "E01") {
                    alert("mobile error!");
                    return;
                } else if ("00" == obj.status) {
                    location.href="/"; 
                }
            })
        }
    }); 
})