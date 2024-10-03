$(document).ready(function(){
    let firstCommandExecuted = false;

    $('#command-form').on('submit', function(e){
        e.preventDefault();
        var command = $('#command').val();
        $('#current-command-text').text(command);

        if (firstCommandExecuted) {
            $('#older-commands').show();
            $('#older-commands-list').append('<li>' + command + '</li>');
        } else {
            firstCommandExecuted = true;
        }

        executeCommand(command);
    });

    $('#command').on('input', function() {
        const command = $(this).val().toLowerCase();
        if (command.includes('gay')) {
            $('#status').html('<img src="/static/jarvis_listening.png" alt="Listening..." class="listening">').show();
        } else {
            if (firstCommandExecuted) {
                $('#status').html('<img src="/static/logo.png" alt="Processing...">').show();
            }
        }
    });

    $('#status').html('<img src="/static/logo.png" alt="Processing...">').show();
});

function executeCommand(command) {
    $('#status').find('img').addClass('processing');

    $.ajax({
        type: 'POST',
        url: '/command',
        contentType: 'application/json',
        data: JSON.stringify({ command: command }),
        success: function(data) {
            $('#response').text(data.response.text || data.response);
            if (data.response.image_url) {
                $('#image-display').html(`<img src="${data.response.image_url}" alt="Image result" style="max-width:100%;">`);
            } else {
                $('#image-display').empty();
            }
            $('#status img').removeClass('processing');
        },
        error: function() {
            $('#status').html('<img src="/static/logo2.png" alt="Error" width="150" height="150">').show();
        }
    });
}
