<!DOCTYPE html>

<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QueryMaster Search</title>
    <style type = "text/css">
        .buttonstyle, .buttonstyle input, .buttonstyle a{
            font-weight: bold;
            color: #ffffff;
            height: 30px;
            width: 80px;
            padding:5px 15px;
            background:#000000;
            border:0 none;
            cursor:pointer;
            -webkit-border-radius: 5px;
            border-radius: 5px;
        }
        .tablestyle, .tablestyle th{
            padding-bottom: 10px;
        }

        .tablestyle{
            padding-left: 40px;
            width: 50%;
        }
    </style>
</head>

<body>
    %if user_email=="":
        <div align = "right">
            <a href=signIn>  <button class="buttonstyle" type="'button">Sign In</button></a>
        </div>
    %end
    %if user_email!="":
        <div align = "right">
            <table rowspan = "1">
                <tr>
                    <td>
                        <div style = "padding-top: 5px;">Signed in as: {{user_email}}</div>
                    </td>
                    <td>
                        <a href=signOut>  <button style = "width: 100px;" class="buttonstyle" type="'button">Sign out</button></a>
                    </td>
                </tr>
            </table>
        </div>
    %end
    <img align = "center" src="/static/QueryMaster-logo4.jpg" alt="Search Logo" title = "Awesome Search Engine's Awesome Logo!" style="display: block; margin-left: auto; margin-right: auto; padding-top: 5%;">
    <div style = "padding-top: 5px; font-size: 25px; text-align: center;">Please enter your query below:</div>
    <form style="text-align: center; padding-top: 10px; padding-bottom: 70px;" action="/results" method="get">
        <input style = "height: 30px; width: 400px;" name="keywords" type="text" id="search_box"/>
        <input class ="buttonstyle" value="Search" type="submit"/>
    </form>
    <div align = "left" style = "width: 100%; margin: auto auto;">
        %if ans:
        <table align = "left" class = "tablestyle" id="results">
            <th align = "right"><font size = 5>Math Operation Results for: {{keywords}}</font></th>
            <tr align = "right">
                <td style = "width: 500px;">{{ans}}</td>
            </tr>
        </table>
        %end
        <table align = "left" class = "tablestyle" id="results">
            <th align = "left"><font size = 5>Query Results for: {{keywords}}</font></th>
        %if len(url_list) > 0:
            %if show_next_prev:
            <tr>
                <td><a href="/results?keywords={{keywords}}&pageid={{prev_pageid}}"><button class="buttonstyle" type="'button">Prev</button></a></td>
                <td><a href="/results?keywords={{keywords}}&pageid={{next_pageid}}"><button class="buttonstyle" type="'button">Next</button></a></td>
            </tr>
            %end
            %for url in url_list:
            <tr>
                <td style = "width: 500px;"><a href="{{url}}">{{url}}</a></td>
            </tr>
            %end
        %end
        %if len(url_list) == 0:
            <tr><td>No results found</td></tr>
        %end
        </table>
    </div>
    
     <!-- load scripts last for better UI responsiveness, use google cdn for libs  -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
    <link href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/ui-lightness/jquery-ui.css" rel="stylesheet">
    <script type="text/javascript" src="/static/main.js"></script>
</body>
</html>