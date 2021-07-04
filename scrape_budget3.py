from selenium import webdriver
from time import sleep
import pandas as pd
from DreamsList import DreamList


def load_all_dreams(driver):
    sleep(5)
    def find_button(driver):
        mt7 = driver.find_elements_by_xpath("//button")
        button = None
        for b in mt7:
            divs = b.find_elements_by_xpath(".//div")
            if divs:
                button = b
        return button

    while True:
        button = find_button(driver)
        if button is None:
            break
        button.click()
        sleep(1)


def find_all_dream_links(driver):
    hrefs = driver.find_elements_by_xpath("//a[@href]")
    hrefs = [e.get_attribute('href') for e in hrefs]
    hrefs = [e for e in hrefs if e.startswith("https://kiezburn.dreams.wtf/kb21/60")]
    return hrefs


def find_dreamers(driver):
    els = driver.find_elements_by_xpath("//div[@class='mt-5 space-y-5']")
    els = els[0]
    k = els.find_elements_by_xpath(".//div[@User]")
    users = [k1.get_attribute('alt') for k1 in k]
    return users

def find_funded(driver):
    paragraph = driver.find_elements_by_xpath("//p[text()='EUR']")
    votes = None
    for p in paragraph:
        split = p.text.split()
        split = combine_numbers(split)
        if len(split) == 2:
            votes = float(split[0])
    return votes


def combine_numbers(split):
    to_remove = []
    if len(split) != 4:
        for index, (n, one) in enumerate(zip(split[:-1], split[1:])):
            try:
                float(n)
                float(one)
                success = True
            except:
                success = False
            if success:
                new_number = n + one
                split[index] = new_number
                to_remove.append(one)
    split = list(filter(lambda x: x not in to_remove, split))
    return split


def calculate_budget(table):
    cells = table.find_elements_by_xpath(".//td")
    all_min = 0
    all_max = 0
    for cell in cells:
        txt = cell.text
        split = txt.split()
        if any(x == "EUR" for x in split):
            split = combine_numbers(split)
            minimum = float(split[0])
            try:
                maximum = float(split[2])
            except IndexError:
                maximum = minimum
            all_min += minimum
            all_max += maximum
    return all_min, all_max


def calculate_prefunding(table):
    cells = table.find_elements_by_xpath(".//td")
    prefund = 0
    for cell in cells:
        text = cell.text
        split = text.split()
        if any(x=="EUR" for x in split):
            split = combine_numbers(split)
            prefund += float(split[0])
    return prefund


def find_budget(driver):
    votes = find_funded(driver)
    tables = driver.find_elements_by_xpath("//table")
    if len(tables) == 1:
        all_min, all_max = calculate_budget(tables[0])
        return {"minimum_budget": all_min, "maximum_budget": all_max, "preexisting_funding": 0, "total_funding": votes}

    elif len(tables) == 2:
        all_min, all_max = calculate_budget(tables[0])
        pre = calculate_prefunding(tables[1])
        return {"minimum_budget": all_min, "maximum_budget": all_max, "preexisting_funding": pre, "total_funding": votes}
    else:
        return {"minimum_budget": 0, "maximum_budget": 0, "preexisting_funding": 0, "total_funding": 0}

def main(driver):
    driver.get("https://kiezburn.dreams.wtf/kb21")
    load_all_dreams(driver)
    hrefs = find_all_dream_links(driver)
    all_dreams = []
    for h in hrefs:
        driver.get(h)
        sleep(1)
        this_dream = {}
        this_dream['link'] = h
        this_dream['name'] = find_name(driver)
        print(this_dream.get('name'))
        this_dream['dreamers'] = find_dreamers(driver)
        this_dream.update(find_budget(driver))
        all_dreams.append(this_dream)
    return all_dreams


def find_name(driver):
    headers = driver.find_elements_by_xpath("//div/h1")
    return headers[0].text

if __name__ == "__main__":
    driver = webdriver.Chrome()
    #url = "https://kiezburn.dreams.wtf/kb21/60c9aed9551867002ccd8fcb"
    #driver.get(url)
    #find_name(driver)
    #dreamers = find_budget(driver)
    #print(dreamers)
    all_dreams = main(driver)
    df = pd.DataFrame(all_dreams)
    print(df.head())
    import pickle
    with open("dumped_df_with_names.pickle", "wb") as f:
        pickle.dump(df, f)
    ##d_list = DreamList.from_dataframe(df)
    driver.close()


