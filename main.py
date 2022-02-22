from bs4 import BeautifulSoup # Beautiful Soup lets us scrape websites
import csv # allows us to write to csv files
import requests # allows us to request the website

URL = "https://soundcloud.com/charts/top" # code to begin scraping
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("a", itemprop="url")
#print(results)
months = [] # we use these lists to write to the csv file
days = []
years = []
for released_date in soup.find_all("time", pubdate = ""): #find the dates of all songs
  #print(released_date.text.strip())
  year = released_date.text.strip()[:4] #dates are formatted as one string, we use string slicing to get each individual part of the date
  month = released_date.text.strip()[5:7]
  day = released_date.text.strip()[8:10]
  months.append(month) # then we append each part of the dates to the above lists
  days.append(day)
  years.append(year)
a = [] # list to hold a bunch of scraped data
index1 = 0
for song_title in results:
    title_element = song_title.find("a")
    artist_element = song_title.find(
        "div",
        class_=
        "chartTrack__username sc-type-light sc-text-secondary sc-truncate")
    position_element = song_title.find("li", class_="chartTracks__item")


for link in soup.find_all("a", itemprop="url"):
     #print(link.text.strip())
    currmonth = months[index1] # matches each date in the three lists to their respective song
    currday = days[index1]
    curryear = years[index1]
    a.append([link.text.strip(),"https://soundcloud.com" +  link.get('href'),currmonth, currday, curryear]) # appends song title, song url, and date to the list
    index1+=1
#print(soup.get_text())
#song_titles = results.find("li")
#print(song_titles)
genres = []
likes = []
downloads = []
comments = [] # more lists to ultimately write to csv file

pagenum = 1
for song_links in a: # scrapes data from each individual song link
  url = song_links[1]
  response = requests.get(url)    
  soup1 = BeautifulSoup(response.content, "html.parser")
  results1 = soup1.find_all("meta", itemprop="genre")
  user = soup1.find_all("meta", itemprop="interactionCount" )
  image = soup1.find_all("img") # get image from song link
  #print(results1)

  for genre_type in results1:
    #print(genre_type.get("content"))
    genres.append(genre_type.get("content")) # get genre info for each song
  datatyp = 0 # determines if it is a like, download, or comment number
  # likes, downloads, and comments are each a separate item, thus we need to use datatyp to determine which type of item it is

  for likes_downloads_comments in user: # appends to the correct list based on which datatype it isinstance
    #print(likes_downloads_comments.get("content"))
    if datatyp % 3 == 0: # use string slicing b/c there is text before the number itself
      likes.append(likes_downloads_comments.get("content")[10:])
    if datatyp % 3 == 1:
      downloads.append(likes_downloads_comments.get("content")[14:])
    if datatyp % 3 == 2:
      comments.append(likes_downloads_comments.get("content")[13:])
    datatyp+=1
      
  
    

#print(likes, len(likes))
#print(downloads,len(downloads))
#print(genres, len(genres))
index2 = 0 # index for iterating to add genres+  likes+downloads+comments
for i in a:
  try:
    i.append(genres[index2])
  except:
    i.append("No Genre") # some genres were not scraped, hence we do this as filler data
  i.append(likes[index2]) # appends like, download, and comment info to each item in a
  i.append(downloads[index2])
  i.append(comments[index2])
  index2+=1
  



with open("test" + str(pagenum) + ".txt", "w+") as out: # test to see html in each song's page
  print(soup1, file=out)
  pagenum+=1




with open("test.txt", "w") as out: # another test to see html on the top 50 page
    print(soup, file=out)
    for i in a:
        print(i, file=out)


with open("test3.csv", "w+") as csv_file: # write the data in list a to the csv FileExistsError
    writer = csv.writer(csv_file, dialect="excel")
    writer.writerow(["Title","Link", "Month", "Day", "Year", "Genres", "Likes", "Downloads", "Comments"]) # start by writing the heading
    for i in a: # then write all the data
        writer.writerow(i)
