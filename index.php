<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jarvis</title>
    <link rel="stylesheet" href="../static/style.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
<div class="container">
    <h1>Jarvis</h1>
    <form class="command_cont" id="command-form">
        <input type="text" id="command" name="command" autocomplete="off">
        <button type="submit">Submit</button>
    </form>
    <div id="status">
        <img src="../static/logo.png" alt="Processing..." width="150" height="150">
    </div>

    <div id="response"></div>

    <div id="image-display"></div>

    <button id="toggle-commands">Toggle Commands</button>

    <div id="current-command">
        <h3>Current Command</h3>
        <p class="cmd" id="current-command-text"></p>
    </div>

    <div id="older-commands" style="display: none;">
        <h3>Older Commands</h3>
        <ul class="cmd" id="older-commands-list"></ul>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="../static/main.js"></script>
<script src="../static/voice.js"></script>
<script src="../static/toggle.js"></script>
</body>
</html>
