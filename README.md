# Pathy: Turkish Twitter Sentiment Analysis Platform. 

## Overview of Pathy and Its Achievements

Pathy is our senior project for graduation from the Computer Science Department of Bilkent University. It is a sentiment analysis platfrom in Turkish, which aids professionals/companies in gaining insight about the engagement between their products/events and the public via Twitter hashtags. Specifically, the customers of Pathy can just type in a hashtag they would like to gain insight about, perhaps created for a company event or a product and learn about how the public reacted to this event/product.

Sentiment analysis in Turkish had not been studied in depth at the time and it was (and still is) perceived to be a challenging task. On the other hand, after our discussions with several CEOs, we identified that there was a need for such a tool in the market. Our ambition in tackling this hard problem and our multi-step creative solution led Pathy being a highly praised senior project and receiving **The Innovation Award** at the Senior Projects Fair.

## Pipeline of Pathy

We actually just need the sentiment analysis results. Unfortunately, the Google Cloud Sentiment Analysis API was not available in Turkish at the time, so we had to create a pipeline to solve this problem. Let us go over it with a picture! 

![Alt text](pipeline.png?raw=true "Title")


1. The customer invokes the platform by typing in a hashtag
2. The hashtag miner, which works with the oauth2 library, retrieves the tweets with that hashtag. 
3. These tweets, which have the potential to be quite informally written, cannot be directly given as input to the translate platform. In the figure, we gave an example of what we mean by the informal tweet: "slm" instead of "Selam", which means "Hello" in Turkish. You can think of this in English as the relationship between "sup?" and "What's up?" We tried invoking the Turkish to English translation API with these informal words and the results were quite bad!
4. Thus, before we move forward to the translation part, we normalize and formalize these tweets and transform all "slm"s to "Selam"s and whatnot. We achieve this by the brilliant [Turkish Pipeline Caller API](https://github.com/0xferit/ITU-Turkish-NLP-Pipeline-Caller) provided by Gulsen Eryigit et al.
5. Now that we have the normalized tweets, it is time to translate them to English. Fortunately, Google had just started using transformers for the translation tasks at the time and the translation quality was really good. So, we used the Google Cloud Translate API and retrived the tweets in English.
6. Finally, the tweets are given as input to the sentiment analysis API and we are done!


## Code 
This code only includes the backend of this project. The front-end of the project has been deprecated. However, we provided a ```mongoDB``` wrapper called ```PathyDB.py``` and separated each part of the pipeline into different files that speak with an instance of ```PathyDB```. Therefore, if you would like to use this backend for your project, you can easily integrate it using the scripts provided in the ```backend_files``` folder. If you have any questions, feel free to reach me at iremlergun@gmail.com.

We also provided you with a file called ```united.py``` that takes input a hashtag and outputs the sentiment score of the tweets of the hashtag. For running this file, you need to first run ```pip3 install -r requirements.txt``` to install the required libraries. Then you need to generate keys for the Twitter API, Google Cloud API, and Pipeline Caller API and paste the keys into the file.  Then, its syntax looks like the following: ```python3 united.py -h hashtag```. 