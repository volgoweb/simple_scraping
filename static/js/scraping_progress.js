
$(document).ready(function(){
    var progress_interval_id;
    function run_scraping() {
        $.ajax({
            type: 'POST',
            url: '/run-scraping/',
            success: function(data, status, request) {
                status_url = request.getResponseHeader('Location');
                progress_interval_id = setInterval(function() {
                    update_progress(status_url);
                }, 1000);
            },
            error: function() {
                alert('Unexpected error');
            }
        });
    }

    function update_progress(status_url) {
        $.ajax({
            type: 'POST',
            url: status_url,
            success: function(data, status, request) {
                $('.progress__percent').html(data.current + '%');
                $('.progress__percent').css('width', data.current + '%');
                console.log('data', data);
                if (data.state != 'PENDING') {
                    clearInterval(progress_interval_id);
                    $('.progress__percent').html('100%');
                    for (var i = 0; i < data.result.length; i++) {
                        var line_text = '{ARTICLE_TITLE}: {COMMENTS_COUNT}'
                            .replace('{ARTICLE_TITLE}', data.result[i][0])
                            .replace('{COMMENTS_COUNT}', data.result[i][1]);
                        var $line = $('<p></p>').text(line_text);
                        $('.result').append($line);
                    }
                    $('.progress').hide();
                }
            },
            error: function() {
                alert('update Unexpected error');
            }
        });
    }

    run_scraping();
});