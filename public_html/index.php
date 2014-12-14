<!DOCTYPE html>
<html lang="en">

<head>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet" />
  <title>Amazon - AR</title>
</head>

<?php?>

<body>
  <div class="all" style="margin-left:180px;margin-top:130px;">
    <div class="container" style="padding-top:50px;">
      <img src="/assets/img/amazon-ar-logo.png" class="img-responsive" />
    </div>
    <div class="container" style="padding-top:50px;">
      <form class="form-inline" role="form" method="GET" action="url_action.php">
        <div class="form-group">
          <!-- <label for="amazonItemUrl">amazon item url</label> -->
          <input type="url" class="form-control" id="amazonItemUrl" name="url" placeholder="Enter amazon URL" style="width:800px">
          <button type="submit" class="btn btn-primary">Go</button>
        </div>
      </form>
    </div>
  </div>
</body>

</html>
