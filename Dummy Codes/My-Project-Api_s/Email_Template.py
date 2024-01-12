template = '''
        
   <!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
    <body>
        <div style="
        background-color:black;
        color:white;
        padding:40px;
        margin: 0;
        position: absolute;
        top: 50%;
        left: 50%;
        margin-right: -50%;
        transform: translate(-50%, -50%)
        ">
            <h3>Hello {},</h3>
            <p>Please click the below button for Reset Your Password
            </p>
            <button style="
            height: 30px;
            margin: 0;
            background-color: yellow;
            box-shadow: 5px 5px 5px white;
            border: 2px solid white;
            border-radius: 50px;
            " > <a style="text-decoration:none;color:black" href="http://localhost:4200/auth/reset?token={}">Reset Password</a></button>
            <p style="margin-top:20px">Thank You,</p>
        </div>
    </body>

</html>

        '''