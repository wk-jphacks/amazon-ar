<!DOCTYPE html>
<html lang="en">

<head>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>

<?php?>

<body>
  <div class="container">
    <form role="form" method="GET" action="url_action.php">
      <div class="form-group">
        <label for="amazonItemUrl">amazon item url</label>
        <input type="url" class="form-control" id="amazonItemUrl" name="url" placeholder="Enter amazon URL">
      </div>
    <button type="submit" class="btn btn-default">Submit</button>
    </form>
  </div>
</body>

</html>
