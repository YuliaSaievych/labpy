#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Cookie;

# Create a new CGI object
my $cgi = CGI->new;

# Retrieve existing cookies
my %cookies = CGI::Cookie->fetch;

# Get form data
my $name   = $cgi->param('name');
my $email  = $cgi->param('email');
my $gender = $cgi->param('gender');
my $role   = $cgi->param('role');

# Check if the form has been submitted
if ($name && $email && $gender && $role) {
    # Increment the form submission counter
    my $counter = $cookies{'form_counter'} ? $cookies{'form_counter'}->value + 1 : 1;

    # Set the form counter cookie
    my $form_counter_cookie = CGI::Cookie->new(
        -name    => 'form_counter',
        -value   => $counter,
        -expires => '+1M',
    );

    # Print the content type header with the cookie
    print $cgi->header(-cookie => [$form_counter_cookie, values %cookies], -type => 'text/html');

    # Print the HTML response
    print <<HTML;
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Submission Result</title>
</head>
<body>
    <h2>Form Submission Result</h2>
    <p>Name: $name</p>
    <p>Email: $email</p>
    <p>Gender: $gender</p>
    <p>Role: $role</p>
    <p>Form submitted $counter times.</p>

    <form action="form_processing.cgi" method="post">
        <input type="submit" name="delete_cookies" value="Delete Cookies">
    </form>
</body>
</html>
HTML
} elsif ($cgi->param('delete_cookies')) {
    # Delete all cookies
    my @cookies_to_delete = keys %cookies;
    my $delete_cookies = CGI::Cookie->new(
        -name    => $_,
        -value   => '',
        -expires => '-1d',
    ) for @cookies_to_delete;

    # Print the content type header with the cookies to delete
    print $cgi->header(-cookie => [$delete_cookies, values %cookies], -type => 'text/html');

    # Print the HTML response
    print <<HTML;
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cookies Deleted</title>
</head>
<body>
    <h2>Cookies Deleted</h2>
    <p>All cookies have been deleted.</p>
</body>
</html>
HTML
} else {
    # Print the content type header without cookies
    print $cgi->header(-type => 'text/html');

    # Print the HTML form
    print <<HTML;
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CGI Form Example</title>
    <style>
        /* Your existing CSS styles go here */
    </style>
</head>
<body>
<form action="form_processing.cgi" method="post">
    <!-- Your existing form fields go here -->

    <input type="submit" value="Submit">
</form>
</body>
</html>
HTML
}
