import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd

main_data = []
exception_companies = []

def scrapping(url):
    global exception_companies
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        excepted_tags = ['Google', 'Images', 'Videos', 'Books', 'Maps', 'News', 'Shopping', 'Search tools',
                         'Past hour', 'Past 24 hours', 'Past week', 'Past month', 'Past year', 'Verbatim',
                         'Learn more', 'Sign in', 'Settings', 'Privacy', 'Terms', 'Dark theme: Off','here']

        links = []            
        if(url.split(' ')[-1] == 'website'):
            for anchor in soup.find_all('a'):
                tag = anchor.text
                if tag not in excepted_tags:
                
                    link = anchor.get('href')
                    link = link.split('&')[0].replace('/url?q=','')
                    if('maps.' not in link and 'https://' in link):
                        links.append(link) 
                    if(len(links)):
                       break
            # print(links)
            return links[0]
        else:
            for anchor in soup.find_all('a'):
                tag = anchor.text
                if tag not in excepted_tags:
                    link = anchor.get('href')
                    link = link.split('&')[0].replace('/url?q=','')
                    if('linkedin.' in link):
                      return link
                      break

    except Exception as e:
        print('Error fetching HTML:', e)
        exception_companies.append(company_name)
        with open('exception_company.pkl', 'wb') as file:
          pickle.dump(main_data, file)
        


def google_searching(search_string):
    global main_data
    search_query = search_string  # Replace with the user's search query
    search_website_url  = f"https://www.google.com/search?q={search_query} official website" 
    search_linkedin_url = f"https://www.google.com/search?q={search_query} official linkedin" 

    website_link = scrapping(search_website_url)
    linkedin_link = scrapping(search_linkedin_url)
    
    data = {'Company_Name': search_query, 'Website_Link': website_link, 'LinkedIN_Link': linkedin_link}
    main_data.append(data)
    
    with open('data2.pkl', 'wb') as file:
      pickle.dump(main_data, file)
    
    print(data)
    
company_name_xl = pd.read_excel('German_plastic.xlsx')[258:]

for company_name in (company_name_xl['Company_Name']):
    # google_searching(company_name)
    pass

# Store Data in Xl-Sheet
# with open('data.pkl', 'rb') as file:
#     data = pd.read_pickle(file)
# df = pd.DataFrame(data)

# main_df = pd.concat([pd.DataFrame(pd.read_pickle('data.pkl')),pd.DataFrame(pd.read_pickle('data2.pkl'))])
# main_df.to_excel('output_data.xlsx', index=False)


google_searching('port F')








def google_searching(search_string):
    search_query = search_string  # Replace with the user's search query
    search_url = f"https://www.google.com/search?q={search_query} official linkedin"  

    # try:
    #     response = requests.get(search_url)
    #     response.raise_for_status()
    #     html = response.text
    #     soup = BeautifulSoup(html, 'html.parser')
    #     links = []

    #     excepted_tags = ['Google', 'Images', 'Videos', 'Books', 'Maps', 'News', 'Shopping', 'Search tools',
    #                      'Past hour', 'Past 24 hours', 'Past week', 'Past month', 'Past year', 'Verbatim',
    #                      'Learn more', 'Sign in', 'Settings', 'Privacy', 'Terms', 'Dark theme: Off','here']

    #     linkedin_link = ""
    #     website_link = ""
    #     for anchor in soup.find_all('a'):
    #         tag = anchor.text
            
    #         # if search_query.lower()  in tag.lower():
    #         link = anchor.get('href')
    #         if 'linkedin' in tag.lower():
    #             if (linkedin_link=="") : linkedin_link = link.replace('/url?q=','').split('&')[0]
    #         if website_link=="" : website_link = link
                
    #         if tag not in excepted_tags:
    #           links.append({'tag': tag, 'website_link': link})
    
    #     website_link  = website_link.split('&')[0].replace('/url?q=','')
    #     linkedin_link = linkedin_link.split('&')[0].replace('/url?q=','')
    #     data = {'Company_Name': search_query, 'Website_Link': website_link, 'Linkedin_Link':linkedin_link}
    #     print('data = ',data)
    #     print("*****************************************\n")
    #     print(links)
        

    # except Exception as e:
    #     print('Error fetching HTML:', e)
    
    scrapping(search_url)

# Call the function with the search string


