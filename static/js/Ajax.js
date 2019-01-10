/*!
 * Created by mhaze on 02.09.15.
 */
var Ajax = function (callbackOnError)
{
    var data = new FormData();

    var resetData = function ()
    {
        data = new FormData();
    };

    this.addAllData = function (form)
    {
        data = new FormData(form[0]);
    };

    this.appendObject = function (obj)
    {
        for (var key in obj)
        {
            if (obj.hasOwnProperty(key))
            {
                var d = data.get(key);

                if (!d)
                    data.append(key, obj[key]);
            }
        }
    };

    this.request = function (url, callback)
    {
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function (json)
            {
                if (json)
                {
                    data.json = json;

                    if (callback instanceof Function)
                        callback(data);
                }

                resetData();
            },
            error: function (xhr)
            {
                callbackOnError(xhr.responseText);
                resetData();
            }
        });
    };
};