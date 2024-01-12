from flask import Flask

app=Flask(__name__)
@app.route('/test')
def test() :
    fname = 'Sayeesh'
    mname = 'M'
    lname = 'Naik'
    
    
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
     
<style>
    th{
        font-family: 'Times New Roman', serif;
        font-size: 15px;
    }
    td{
        font-family:'Arial';
        font-size: 13px;

    }
    img {
        max-width: 80px ;
        max-height: 60px ;
    }
</style> 

<div style="text-align:center">
    <img src="https://drive.google.com/thumbnail?id=1nRZ2KomzjstN68nJL5nMnDv3HIcj2-Mt" alt="logo" />
</div>
<table>
    <tr>
        <th>Hello&nbsp;'''+fname+'''&nbsp;'''+mname+'''&nbsp;'''+lname+''',</th>
    </tr>
    <tr>
        <td></td>
        <td>
            We have sent you this email in response to your request to reset your password. 
            You can use the following link to reset your Password.
        </td>
    </tr>
    <tr>
        <td></td>
        <td>
            <div style="text-align: center;">
                <a href="https://smbprice.dcc-am.com/auth/reset-password"><u> Reset Password <u></a>
                <i class="fa fa-lock icon" style="font-size:20px;margin:10px;"></i>
            </div>
        </td>
    </tr>
    <tr>
        <td></td>
        <td>
            If you didn't request a password reset,you can ignore this email. We recommend that you keep your
            password secure and not share with anyone.
        </td>
    </tr>
</table>

</body>
</html>
'''

app.run()

'''<style>
body{
       background-color:red;
     }
button{
       padding:5px;
       }
img{
       padding:50px;
    }
</style>
<body>
 <img src="https://drive.google.com/thumbnail?id=1nRZ2KomzjstN68nJL5nMnDv3HIcj2-Mt" alt="logo" />
<button>click</button>
</body>'''