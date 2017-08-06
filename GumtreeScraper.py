#!/usr/bin/python

"""Copyright® Anas Yousef 2017"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from time import sleep

import urllib.parse


class RetrieveAdInfo:

    def __init__(self, keyword, location=None, page=1):
        self.url = 'https://www.gumtree.com/'
        self.search_arg = 'search?'
        self.keyword = str(keyword)
        self.location = str(location)
        self.page = page
        self.complete_url = {'search_category':'all','search_location':self.location,'q':self.keyword, 'page':self.page}
        self.encoded_url = self.url + self.search_arg + urllib.parse.urlencode(self.complete_url)

    def get_search_url(self):
        return self.encoded_url

    def retrieve_ad_url(self, items):
        self.remove_unnecesary(items)

        ad_links = []
        for item in items:
            ad_links.append(self.url + urllib.parse.quote(item.get('href')))
        return ad_links

    def remove_unnecesary(self, list_):
            for _ in range(3):
                del list_[0]

    def retrieve_multiple_pages(self):

        multiple_urls = []

        for i in range(1, self.page + 1):

            self.__init__(self.keyword, self.location, page=i)
            multiple_urls.append(self.get_search_url())

        return multiple_urls

    def retrieve_ad_title(self, items):

        self.remove_unnecesary(items)

        title_text = []
        for item in items:
            title_text.append(item.text)
            
            
def main(user_input_search_entry, user_input_location_entry, user_input_num_pages_entry, user_input_filename_entry):

    driver = webdriver.Chrome()
    name_for_all_pages = []
    links_to_be_removed = []

    def multi_to_single_list(items):

        one_list = []

        for i in items:
            for j in i:
                one_list.append(j)

        return one_list

    def remove_falsy(items):

        for single_item in items:
            if not bool(single_item.text):
                continue
            else:
                return single_item.text

    def get_ad_details(all_urls):

        """Gets phone number and name from the add"""

        counts_of_completed = 0
        phone_numbers_for_all_pages = []
        title_names_for_all_pages = []

        for singleUrl in all_urls:

            # Open all the connections to the ad detail page

            driver.get(singleUrl)

            page_html_ad_detail = urlopen(singleUrl)
            soup_ad_detail = BeautifulSoup(page_html_ad_detail, "html.parser")

            counts_of_completed += 1
            percent_completed = str(round((counts_of_completed / ad_links_count) * 100))
            print(str(counts_of_completed) + '/' + str(ad_links_count) + ' ({}%) Completed'.format(percent_completed))

            # Retrieval of name and phone number from ad page
            try:
                driver.execute_script("document.getElementById('reply-panel-reveal-btn').click()")
                sleep(2)
                phone_number_for_single_ad = remove_falsy(driver.find_elements_by_css_selector('.form-row-label'))

                contact_name = soup_ad_detail.find("h2", {"class": "truncate-line space-mbn"}).text.replace('\n', '')

            except WebDriverException:

                # No phone number has been found
                links_to_be_removed.append(driver.current_url)
                print("Skipped!\n")
                continue

            else:

                name_for_all_pages.append(contact_name)
                title_names_for_all_pages.append(driver.title.split('|')[0].strip())

                if phone_number_for_single_ad.startswith("07") or phone_number_for_single_ad.startswith("447"):

                    phone_numbers_for_all_pages.append(phone_number_for_single_ad)

            ####

        return name_for_all_pages, phone_numbers_for_all_pages, links_to_be_removed, title_names_for_all_pages

    search_url = RetrieveAdInfo(user_input_search_entry, user_input_location_entry, user_input_num_pages_entry)

    urls = search_url.retrieve_multiple_pages()
    u_request = []
    page_html = []
    page_soup = []
    ad_links_for_all_pages = []

    for url in urls:

        u_request.append(urlopen(url))

    for a in range(len(u_request)):

        page_html.append(u_request[a].read())

    # Get page_soup for multiple pages
    for b in range(len(page_html)):

        page_soup.append(BeautifulSoup(page_html[b], "html.parser"))

    # Get Ad URL
    for c in range(len(page_soup)):

        containers_for_all_pages = page_soup[c].findAll("a", {"class":"listing-link"})
        ad_links_for_all_pages.append(search_url.retrieve_ad_url(containers_for_all_pages))

    if user_input_num_pages_entry > 1:
        ad_links_for_all_pages = multi_to_single_list(ad_links_for_all_pages)
    else:
        # It is assigned the first element since it has a multi-dimensional array
        ad_links_for_all_pages = ad_links_for_all_pages[0]

    ad_links_count = len(ad_links_for_all_pages)
    print("\n" + str(ad_links_count), "Ad(s) have/has been found\n")

    name_for_all_pages, phone_number_for_all_pages, links_to_be_removed, \
        title_ad_for_all_pages = get_ad_details(ad_links_for_all_pages)

    # Remove links that are not in list: links_to_be_removed

    ad_links_to_be_kept = []
    for item in ad_links_for_all_pages:
        if item not in links_to_be_removed:
            ad_links_to_be_kept.append(item)

    # Write all the info into the file

    filename = str(user_input_filename_entry) + '.csv'
    file = open(filename, 'w')
    file.write('Title,Name,Phone Number, Link\n')

    for title, name, phone_number, link in zip(title_ad_for_all_pages, name_for_all_pages, phone_number_for_all_pages,
                                               ad_links_to_be_kept):

            file.write(title.replace(',', '|') + ',' + name.replace(',', '|') + ',' + phone_number + ',' + link + '\n')

    file.close()
    driver.quit()

    return True

