Git Link - Code works perfectly fine locally
AWS Link - The Index Page Loads, but an issue of Selenium which does not allow Browsers to open on the EC2 instance could not be solved, so we don't get any output on Cloud
Azure Link - Azure does not accept sign-up using debit cards (only credit card accepted), so could not sign-up, but even on Azure same Selenium issue would have occured. 

mySQL DB Table -> desc video_details;
+-------------+--------------+------+-----+---------+-------+
| Field       | Type         | Null | Key | Default | Extra |
+-------------+--------------+------+-----+---------+-------+
| Title       | varchar(200) | YES  | UNI | NULL    |       |
| Date        | varchar(20)  | YES  |     | NULL    |       |
| Views       | varchar(20)  | YES  |     | NULL    |       |
| Likes       | varchar(20)  | YES  |     | NULL    |       |
| Channel     | varchar(200) | YES  |     | NULL    |       |
| Subscribers | varchar(30)  | YES  |     | NULL    |       |
+-------------+--------------+------+-----+---------+-------+

Google Chrome Version should be '110.0.5481'.--

USAGE :
Search - Enter a youtube URL, click the button and wait for approx 20-25 seconds to get the video details(if available)
Get Upload Count - Click this button and wait for approx 50-60 seconds to get the upload count

TESTS SEARCH CASES WERE PERFORMED SUCCESSFULLY:
    Search Cases based on actual youtube videos :
        1. https://www.youtube.com/watch?v=mPvUU07ViM8 (was live streaming)
        2. https://www.youtube.com/watch?v=cEP3JgLyHSU (0 comments video)
        3. https://www.youtube.com/watch?v=NWzbdWf7Yts (high comment video)
    Search Cases based on non-youtube or wrong url :
         1. www.google.com (non-youtube)
         2. asasasdasda (not a url)
         3. https://www.youtube.com/watch?v=adksaljdalk (wrong youtube url)


Challenge number 2 : 
1. Go to ineuron , krish , collegewallah channel    - Done
2. Find out how many videos are uplaoded            - Done
3. take input  url for a perticualr video and give me below output
    1. Video title          - Done
    2. video Details        - Done
    3. number of likes      - Done
    4. person name with commnet - Done 
4. strore all the information in a MYSQL DB (you have to design your own table mention it in your git link) - Done
5. logging is mandatory - Done
6. Exception handling is nescessary - Done 
7. modular coding is nescessary - Done
8. Classs and object is must    - Done
9. Finally submit your 3 hosted URL to me and sunny along with your code base git hub link
