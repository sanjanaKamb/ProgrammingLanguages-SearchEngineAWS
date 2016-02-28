Feature #1: Enhanced Page Rank: 

Improved the efficiency of the page rank functionality by integrating a new algorithm.The pagerank functionality implemented in Lab3 was using the algorithm suggested in the lab handout which calculates the rank based on the number of outbound links and the set of all incoming documents. basically it uses the following equation: 

The new algorithm implemented in Lab 4 uses the following equation: [1]
(1-d)(1/N) + d[ PriorPageRank(1)(1/number of links on page 1) + PriorPageRank(2)(1/number of links on page 2) + … + PriorPageRank(k)*(1/number of links on page k)]
d = probability , N = number of links
In order to integrate this new functionality into crawler.py, I had to introduce a new data structure called graph which is a dictionary with current page as the key and a set containing a list of document ids which can be found in the current page. I populate the entries for graph in the crawler function and call the new_page_rank function with the graph data structure. new_page_rank function will return a dictionary with the document ids as the key and ranking score as the value. 
Not only that the new algorithm uses a more complex and enhanced computation to calculate the pagerank functionality, it is faster as well. As you can see in the following screenshot, old pagerank function took 0.018053 seconds to compute while the new pagerank function took 0.000673 seconds to compute. It becomes significant upon feeding it a large data. 

After sorting the data structure returned by old pagerank and new pagerank, As it is clear from the below screenshot the ranking scores have been changed and the scores returned by the new_page_rank is more precise. 

Feature #2 Autocompletion:

The goal of this feature is to present the user with a list suggested search query words, similar to google search suggestions, based on the words in the search engine's persistent storage.
The way the search suggestion is accomplished is typical AJAX architecture. The web pages where the user can type a search query, detect any changes in the input box, and fire off HTTP requests in the background, to the server with the value of the input box that the user has typed so far. The server then looks into its lexicon to find words that begin with this pattern, and returns JSON data back to the web browser, if any matches were found in the server's lexicon.
On the web server the following new route has been added:
/api/json/word_suggestion
an example get request to this route:
/api/json/word_suggestion?prefix=tor
the server then queries the sqlite lexicon for matches, constructs a JSON version of the results using the json python module and returns the result. 
On the client side, the following libraries were used: jQuery, jQuery-ui
The client html pages first load the jQuery libraries from the google cdn (content delivery network). This happens at the end of the document so as to not slow the rendering of the document down. Once jQuery is loaded its methods are used to install listener function for any changes of the value of the input box. The listener function will take the value of the input box send a HTTP request to the server, and get back the JSON result. if the JSON result is not empty, it is given to the autocomplete feature of jQuery-ui along with a reference of the input box into the DOM, (using jQuery's CSS style selectors) jQuery-ui then takes care of rendering the matches if any exist.
Since the AJAX request are all happening in the background, the page does not need to be refreshed for the user to see the search suggestions.

Feature #3 One click deployment:

This feature aims to make the deployment easy for the user. The user is provided with a launch and a termination script. The user is required to zip all the files to be deployed into a folder. The launch script launched an EC2 instance on amazon web services. It provides the required security key for authentication in the process that ensures a secure connection. The specified zip file is unzipped on the server and the files are organized accordingly. The search engine dynamically creates redirect, signIn and signOut pages with the new domain name created from a new EC2 instance. This is done by the launch script that provides the frontend search engine startup python script with the new domain name as a command line argument. The search engine is then run as a background process on the process. The launch script then print the domain name where the search engine is running and an instance ID. 
In addition, the user is also provided with a terminate script, where the instance ID is provided as a command line argument. This automatically terminates the specified instance on AWS. 

Feature #4 Query phrase interpretation:

This feature lets the user type in simple mathematical queries, and the search engine evaluates it and displays the result as well as display query results. The operations are limited to addition, subtract, division, multiplication, and exponentiation. It lets the user type in the queries with or without space, however is limited to only binary queries (a op b). The query string input by the user is already stored in a variable called keywords. In order to implement math operations, the keywords had to be parsed, and stored as its respective int values IF they exist. When it doesn’t exist, the search page displays as it used to. The parsing is done by first converting keywords into a list of characters, and then each character is parsed to see if they represent an int. Consequent int characters are created into an multidigit positive int value. The operator is stored in a variable as a string, and if conditions are used to branch into the different operation sequences.

Feature #5 Minimize number of clicks for each search:
This feature lets the user type queries and see the results on the same page. This eliminates the need for clicking back to go to previous page which increases the user friendliness. This is implemented by having only one template page which hosts the logo, the query bar and the results table regardless of the results returned. Even if there are no results, the same page is displayed. The results table is implemented using an if statement that checks to see if a query has been completed yet. If so, it displays the results table with the header. Otherwise, it doesn’t display the table at all. Once this check passes and the results table header is displayed, it checks for results. If no results found, it displays a string that states so. Otherwise, it will display the results one by one.
