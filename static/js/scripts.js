$("form[name=signup_form]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(response){
            console.log(response);
            window.location.href = "/dashboard";
        },
        error: function(response){
            console.log(response);
            $error.text(response.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
})

$("form[name=login_form]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (response) {
            console.log(response);
            window.location.href = "/dashboard";
        },
        error: function (response) {
            console.log(response);
            $error.text(response.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
})

$("form[name=create_form]").submit(function (e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/create_budget",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (response) {
            console.log(response);
            window.location.href = "/dashboard";
        },
        error: function (response) {
            console.log(response);
            $error.text(response.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
})

$("form[name=transaction_form]").submit(function (e) {
    var $form = $(this);
    var data = $form.serialize();

    $.ajax({
        url: "/user/add_transaction",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (response) {
            console.log(response);
            window.location.href = "/dashboard";
        },
        error: function (response) {
            console.log(response);        }
    });
    e.preventDefault();
})

function on(id) {
    document.getElementById("overlay").style.display = "block";
    var element = document.getElementsByName("budget_id");
    element[0].value = id;
    console.log(element);
}

function off() {
    document.getElementById("overlay").style.display = "none";
}

const change = () => {
    const inputValue = document.getElementById("id").value;
    console.log(inputValue);
}

function show(id) {
    document.getElementById("summary_" + id).style.display = "block";
}

function hide(id) {
    document.getElementById("summary_" + id).style.display = "none";
}