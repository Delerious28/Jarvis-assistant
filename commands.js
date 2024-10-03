// commands.js

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

    $('#toggle-commands').on('click', function() {
        $('#commands').toggle();
    });
});

function executeCommand(command) {
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
        },
        error: function() {
            $('#response').text('Error executing command.');
            $('#image-display').empty();
        }
    });
}
