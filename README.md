###Main Goals:
  For my scraping project, my objective was to scrape the names, dates, and links to art exhibits so that the data could be used by visitors who are trying to decide what exhibit they want to see. With this data, each exhibit will be matched with the date it is open and a link to the page so that a user could get a random exhibit to visit after inputing the dates they were visiting.

###Modifications:
  Originally, I had hoped to scrape three completely separate web pages, the Met, The MoMA, and The Guggenheim. I thought it would be too simple to scrape only one, because there were only approximately 40 exhibits per museum, however I was very wrong. My first web page took me days to scrape as I ran into the complications in this README. However, I was able to finally perfect the scraping of the Met. While I was able to scrape the titles and links from the MoMa site, the dates were not wrapped in an element that was exclusive to the dates, so the data was incomplete. The Guggenheim was a beast of its own, which I still cannot comprehend. That being said, I scraped only the Met page so that the complete data could be used to help a visitor decide which exhibit they could view in that museum.

#How I did it:
  This was the hardest project I have ever done, and also the one I have learned the most from. So, I am quite proud to explain the following:

  First, I installed everything necessary to make my code run and opened my csv file named "met_exhibits.csv". I then wrote the header row for my file using c.writerow(['titles', 'dates', 'links'])

  I then used the function driver.get('http://www.metmuseum.org/exhibitions/current-exhibitions');
  to make chromedriver open my webpage so that the code was scrapable.

  For each item I wanted to scrape, I created an empty list that would be filled after I ran my scraping functions. I created lists for titles, dates, and links.

  For titles and dates, I was able to use BeautifulSoup to collect the text from the elements I wanted and then append them to the corresponding list:

  title_list = bsObj.findAll("h2", {"class":"card__title"})
  for title in title_list:
      titles.append(title.get_text())

  date_list = bsObj.findAll("strong")
  for date in date_list:
      dates.append(date.get_text())

  For links, I needed to create a full url so I made an empty list called 'partial' and filled it with the results of my regex. I then added every 'part' in 'partial' to the first half of the url and appended that to my links list.

  The last step was to create a for loop that iterated through the corresponding index for each of my lists and wrote a new row in my csv file each time it looped. More on this in the problems section...

  The final step was to close the file I opened when writing my csv and quite the chromedriver technology using the two functions:
  csvfile.close()
  driver.quit()

##Problems:
  I learned that the Met Museum's website's code is not directly scrapable. While I was able to dig deeper into the tags using the developer tools, the tags did not contain anything in the viewsource page, which is what I was scraping. In order to access these elements, I had to pip install selenium, which acted as the thread between my scraper and the hidden code. Using chromedriver, I was able to give selenium my url, which chromedriver then loaded with the newly-scrapable code so that my app would work.

  The second issue I encountered is that once I scraped the titles, dates, and urls, from the webpage, it was all returned back to me in one large chunk. Because all of my information for each exhibit is on one page, rather than parsing through separate urls, I needed to find a way to associate the correct exhibits with its corresponding information.

    -This was especially necessary when it came to writing my output into a csv file. At first, each list (title, date, and link) was printed into a single cell per list. I needed to find a way to write a new row for each corresponding item in the three separate lists.

    -I was able to fix this problem by creating a for-loop that looped through the three lists I had created and wrote a new row in my csv file containing the nth index of each list. The code I used is this:

        n = 0
        for title in titles:

            c.writerow( [titles[n], dates[n], links[n]] )
            n = n + 1

    Now, the exhibits, dates, and link to the page line up on the same row!

  The next problem is that I initially used regex to collect my urls for each exhibit page, however this excluded the first half of the url and would be useless to a user. I had to find a way to add the first half of the url (which remained constant) to the half that was unique to each exhibit. Then, I needed to put that into a new list. I did that by using this code:

  partial = []

  for link in bsObj.findAll("a", href=re.compile("^(/exhibitions/)((?!:).)$")):
      if 'href' in link.attrs:
          partial.append(link.attrs['href'])

  links =[]
  for part in partial:
      new_link = ["http://www.metmuseum.org" + part]
      links.append(new_link)

  Next issue is directly related to the code above. I realized in my csv file that the regex I had been using included three unnecessary urls: "http://wwww.metmuseum.org/exhibitions/current-exhibitions"
  "http://wwww.metmuseum.org/exhibitions/upcoming-exhibitions"
  "http://wwww.metmuseum.org/exhibitions/upcoming-exhibitions"
  These threw off the alignment of all the exhibits in my file. I needed to edit my regex to this:

  for link in bsObj.findAll("a", href=re.compile("^(/exhibitions/listings/)((?!:).)$")):

  in order to eliminate the urls.
