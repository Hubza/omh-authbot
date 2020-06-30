<?php 
session_start();
?>
<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>OMH AUTH</title>
    <link rel="stylesheet" type="text/css" href="main.css">
</head>

<body>
    <img src="https://upload.hubza.co.uk/i/logo.png" />
    <div class="cont">
        <?php 
if(isset($_GET['discord'])) {
$_SESSION['discord'] = $_GET['discord'];
?>
<?php 

$discord = $_SESSION['discord'];
if (is_numeric($discord)){
    
?>

        <h1>Log-in with osu!</h1>
        <form action="https://osu.ppy.sh/oauth/authorize" method="GET" class="opl-login">
            <input type="hidden" name="response_type" value="code">
            <input type="hidden" name="client_id" value="1624">
            <input type="hidden" name="redirect_uri" value='https://omh.auth.hubza.co.uk/auth'>
            <input type="submit" class="your button css classes" value="Login">
        </form>
        <h3>Why do you need this?</h3>
        <p>After you log-in with your osu! account, we check your amount of medals, and automatically give you roles
            according to them.<br>This also allows us to verify your account. | Please login to osu! first at <a style="color: white !important" href="https://osu.ppy.sh/">https://osu.ppy.sh/<a></p>
            <p style="opacity: 0.5"><br>Debug Info<br>Discord: <?php echo $_GET['discord']?></p>

            <?php
}}

?>


    <?php 
if(isset($_GET['discord'])) {
$_SESSION['discord'] = $_GET['discord'];
?>
<?php
if (!is_numeric($discord)){ ?>


        <h1>The Discord ID is formed incorrectly.</h1>
        <h3>If you think this error is incorrect, please contact me at Hubz#6283 on discord.</h3>
        <p style="opacity: 0.5"><br>Error code: 0x0002</p>
    <?php } ?>

<?php }else{ ?>
            <h1>The URL is formed incorrectly.</h1>
        <h3>If you think this error is incorrect, please contact me at Hubz#6283 on discord.</h3>
        <p style="opacity: 0.5"><br>Error code: 0x0001</p>

        
<?php } ?>





    </div>
</body>

</html>