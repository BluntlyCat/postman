$(document).ready(function () {
    let form = $('#postmanAjaxForm');
    let formWrapper = $('#formWrapper');

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
                formWrapper.removeClass('alert-danger alert-warning alert-info');
                formWrapper.addClass('alert-success');
                formWrapper.html(mailData.form);
            } else if (mailData['formErrors'] || mailData['errors'] || mailData['alreadySent']) {
                if (mailData['errors'])
                    formWrapper.addClass('alert-danger');
                else if (mailData['formErrors'])
                    formWrapper.addClass('alert-warning');
                else if (mailData['alreadySent'])
                    formWrapper.addClass('alert-info');

                formWrapper.html(mailData.form);
                form = $('#postmanAjaxForm');
                form.on('submit', function (e) {
                    submit(e);
                });
            }
        });
    };

    form.on('submit', function (e) {
        submit(e);
    })
});