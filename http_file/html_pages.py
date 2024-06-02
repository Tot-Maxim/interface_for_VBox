TAP_manager = """
<!DOCTYPE html>
<html lang='ru'>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TAP interface</title>
    <style>
        .top-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #5399A7;
            padding: 10px;
            color: white;
            text-align: left;
        }
        body {
            background: url('back.png'), #365979;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;

            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        }

        form {
            display: grid;
            gap: 20px;
            justify-items: center;
            margin-top: 40px;
        }

        form_input {
            display: grid;
            gap: 30px;
            justify-items: left;
            margin-top: -20px;
        }

        button {
            background-color: white;
            color: black;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        input {
            padding: 5px;
        }

        label {
            color: white;
            text-align: right;
            padding-right: 10px;
            grid-column: 1 / 2;
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <h1 style="color: white;">TAP Manager</h1>
        <button style="font-size: 20px; font-weight: bold;" onclick="redirect_to_tap()">TAP MANAGER</button>
        <button style="font-size: 20px; font-weight: bold;" onclick="redirect_to_client()">SOKET CLIENT</button>
        <button style="font-size: 20px; font-weight: bold;" onclick="redirect_to_server()">SOCKET SERVER</button>
    </div>
    <form_input>
        <label for="src_ip">Введите IP-адрес источника:</label>
        <label for="dst_ip">Введите IP-адрес назначения:</label>
        <label for="password">Введите пароль:</label>
        <label for="serial_port">Введите последовательный порт:</label>
    </form_input>
    <form method="post">
        <input type="text" id="src_ip" name="src_ip" value="10.1.1.8">
        <input type="text" id="dst_ip" name="dst_ip" value="10.1.1.7">
        <input type="password" id="password" name="password">
        <input type="text" id="serial_port" name="serial_port" value='/dev/ttyACM0'>
        <button onclick="window.location.href='/tap_manager'">Запуск TAP интерфейса</button>
    </form>
    <script>
        function redirect_to_tap() {
            window.location.href = '/tap_manager';
        } 
        function redirect_to_client() {
            window.location.href = '/socket_client';
        } 
        function redirect_to_server() {
            window.location.href = '/socket_server';
        }

    </script>
</body>
</html>
"""

socket_client = """
<!DOCTYPE html>
<html lang='ru'>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TAP interface</title>
    <style>
        .top-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #5399A7;
            padding: 10px;
            color: white;
            text-align: left;
        }
        body {
            background: url('back.png'), #365979;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;

            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        }

        form {
            display: grid;
            gap: 20px;
            justify-items: center;
            margin-top: 40px;
        }

        form_input {
            display: grid;
            gap: 30px;
            justify-items: left;
            margin-top: -20px;
        }

        button {
            background-color: white;
            color: black;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        input {
            padding: 5px;
        }

        label {
            color: white;
            text-align: right;
            padding-right: 10px;
            grid-column: 1 / 2;
        }
    </style>
</head>
<body>
     <div class="top-bar">
        <h1 style="color: white;">Soket client</h1>
        <button style="font-size: 20px; font-weight: bold;" onclick="redirect_to_tap()">TAP MANAGER</button>
        <button style="font-size: 20px; font-weight: bold;" onclick="redirect_to_client()">SOKET CLIENT</button>
        <button style="font-size: 20px; font-weight: bold;" onclick="redirect_to_server()">SOCKET SERVER</button>
    </div>
     <form_input>
        <label for="dst_ip">Введите IP-адрес сервера:</label>
        <label for="port">Введите порт сервера:</label>
        <label for="file_path">Введите имя файла для передачи:</label>
    </form_input>
    <form method="post">
        <input type="text" id="client_ip" name="client_ip" value="10.1.1.7">
        <input type="number" id="client_port" name="client_port" value="5050">
        <input type="text" id="file_path" name="file_path" value='logo.png'>
        <button onclick="window.location.href='/socket_client'">Передать файл</button>
    </form>
    <script>
        function redirect_to_tap() {
            window.location.href = '/tap_manager';
        }        
        function redirect_to_client() {
            window.location.href = '/socket_client';
        }        
        function redirect_to_server() {
            window.location.href = '/socket_server';
        }
    </script>
</body>
</html>
"""

socket_server = """
<!DOCTYPE html>
<html lang='ru'>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TAP interface</title>
    <style>
        .top-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #5399A7;
            padding: 10px;
            color: white;
            text-align: left;
        }
        body {
            background: url('back.png'), #365979;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;

            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        }

        form {
            display: grid;
            gap: 20px;
            justify-items: center;
            margin-top: 40px;
        }

        form_input {
            display: grid;
            gap: 30px;
            justify-items: left;
            margin-top: -20px;
        }

        button {
            background-color: white;
            color: black;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        input {
            padding: 5px;
        }

        label {
            color: white;
            text-align: right;
            padding-right: 10px;
            grid-column: 1 / 2;
        }
    </style>
</head>
<body>
     <div class="top-bar">
        <h1 style="color: white;">Soket server</h1>
        <button style="font-size: 20px; font-weight: bold;" onclick="redirect_to_tap()">TAP MANAGER</button>
        <button style="font-size: 20px; font-weight: bold;" onclick="redirect_to_client()">SOKET CLIENT</button>
        <button style="font-size: 20px; font-weight: bold;" onclick="redirect_to_server()">SOCKET SERVER</button>
    </div>
    <form_input>
        <label for="dst_ip">Введите IP-адрес сервера:</label>
         <label for="dst_ip">Введите порт сервера:</label>
    </form_input>
    <form method="post">
        <input type="text" id="socket_ip" name="socket_ip" value="10.1.1.8">
        <input type="number" id="socket_port" name="socket_port" value="5050">
        <button onclick="window.location.href='/socket_server/starting'">Запуск ceрвера</button>
    </form>
    <script>
        function redirect_to_tap() {
            window.location.href = '/tap_manager';
        }        
        function redirect_to_client() {
            window.location.href = '/socket_client';
        }        
        function redirect_to_server() {
            window.location.href = '/socket_server';
        }
    </script>
</body>
</html>
"""

