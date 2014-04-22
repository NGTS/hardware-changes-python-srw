function makeHideable(i, hideable) {
    $(hideable).slideToggle('fast');
}

function addClickHandlers(new_data) {
    var added_handlers = $(new_data);
    added_handlers.find(".toggler").each(function(i, el) {
        $(el).click(function() {
            $(el).next("div.hideable").each(makeHideable);
        });
    });
    return added_handlers;
}

function add_form(i) {
    var el = $("div#forms");
    console.log("Adding form ", i);
    $.ajax({
        type: "POST",
        url: "/new_form/",
        data: { form_id: i },
        success: function(data, text_status, jqXHR) {
            $(el).append(addClickHandlers(data));
        },
    });

    $("button#submit-form").prop('disabled', false);
}

function auto_today(selector) {
    selector.val((new Date()).toJSON().slice(0, 10));
}

$(document).ready(function() {
    var button = $("button#add-form");
    var i = 0;

    $(button).click(function() {
        add_form(i);
        i++;
    });

    // Set up the date field, horrible hack to set the date automatically to today
    auto_today($("#change-date"));
});

