# Assertjinator2000
Replaces junit tests with their assertj counterparts. Requires manual fixing, someitimes does not convert correctly. 
Can assertjify an entire path and a single file.
Can't handle multiline assertions. If a file fails to convert find the assertion that spans multiple lines and put it on one line. After that you can pass it through the script again. 
This script works on only junit tests. Hamcrest tests have to be converted manually. 
