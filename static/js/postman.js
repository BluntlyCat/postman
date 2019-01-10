$(document).ready(function () {
    let form = $('#postmanAjaxForm');
    let formWrapper = $('#formWrapper');
    let postman = $('#postman');

    function submit(event) {
        event.stopPropagation();
        event.preventDefault();

        submitAjax();
    }

    let submitAjax = function () {
        let ajax = new Ajax(function (error) {
            console.log(error);
        });

        ajax.addAllData(form);
        ajax.request(form.attr('action'), function (data) {
            let mailData = data.json;

            if (mailData.success) {
                postman.removeClass('alert-danger alert-warning alert-info');
                postman.addClass('alert-success');
                formWrapper.html(mailData.form);
            } else if (mailData['formErrors'] || mailData['errors'] || mailData['alreadySent']) {
                if (mailData['errors'])
                    postman.addClass('alert-danger');
                else if (mailData['formErrors'])
                    postman.addClass('alert-warning');
                else if (mailData['alreadySent'])
                    postman.addClass('alert-info');

                formWrapper.html(mailData.form);
                form = $('#postmanAjaxForm');
                form.submit(submit);
            }
        });
    };

    form.submit(submit)
});