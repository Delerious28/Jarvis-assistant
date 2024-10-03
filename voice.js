function startVoiceRecognition() {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onstart = function() {
        $('#status img').addClass('listening');
    };

    recognition.onresult = function(event) {
        const command = event.results[0][0].transcript.trim();
        $('#command').val(command);
        $('#current-command-text').text(command);

        let firstCommandExecuted = true;

        if (firstCommandExecuted) {
            $('#older-commands').show();
            $('#older-commands-list').append('<li>' + command + '</li>');
        } else {
            firstCommandExecuted = true;
        }

        executeCommand(command);
    };

    recognition.onend = function() {
        $('#status img').removeClass('listening');
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
    };
}
