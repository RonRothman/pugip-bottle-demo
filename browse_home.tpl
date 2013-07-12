<html>
<head><title>Browsing Zip Codes</title></head>
<body>

Browse the zip codes:

<ul>
    {% for zc in all_zips %}
        <li><a href='/population/{{ zc.zip|e }}?all=1'>{{ zc.zip|e }}</a>: {{ zc.primary_city|e }}</li>
    {% endfor %}
</ul>

</body>
