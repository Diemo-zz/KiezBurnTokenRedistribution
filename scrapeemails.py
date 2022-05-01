from selenium import webdriver
from scrape_budget3 import login
from time import sleep

def main():
    #driver = webdriver.Chrome()
    #driver.get('file:///C:/Users/diarm/Documents/Dreams2022/Kiez Burn 2022 _ Kiez Burn.html')
    #tables = driver.find_elements_by_xpath('//tbody')
    #sec_tables = tables[1].find_elements_by_xpath('./tr')

    #all_name = {}
    #for i, s in enumerate(sec_tables):
    #    if i%40 == 0:
    #        print("Done ", i)

    #    names = s.find_elements_by_xpath('.//p')
    #    start = value = None
    #    for n in names:
    #        if n.text.startswith('@'):
    #            start = n.text
    #        elif '@' in n.text:
    #          value = n.text
    #    if start and value:
    #        all_name[start] = value
    #driver.close()

    import pickle
    #with open('dumped_dreamers.pickle', 'wb') as f:
    #    pickle.dump(all_name, f)
    with open("dumped_dreamers.pickle", 'rb') as f:
        all_name = pickle.load(f)
    with open("dumped_df_with_names_kb22and_budgets.pickle", 'rb') as f:
        df = pickle.load(f)
    dreamers = [d  for dreamer in df.dreamers  for d in dreamer]
    dreamers = [f'@{d}' for d in dreamers]
    emails = {d: all_name.get(d) for d in dreamers}
    from pprintpp import pprint
    pprint(emails)


def main2():
    test = ['hanna.oukka@gmail.com',
 'ankatrin@posteo.net',
 'djbriggs.1985@gmail.com',
 'paula.schulz@aol.de',
 'gabezcua@gmail.com',
 'silvienamail@gmail.com',
 'hannes.westphal@gmail.com',
 'holger.fuessler@posteo.de',
 'oystein.wicklund@gmail.com',
 'caro.tyka@gmail.com',
 'olanoisasi@gmail.com',
 'jessie.dietrich@gmx.de',
 'courtofkings11@gmail.com',
 'sophiaimanske@gmail.com',
 'diarmaiddeburca@gmail.com',
 'melindagonzalez2000@gmail.com',
 'cecicast@hotmail.it',
 'noack_andreas@gmx.at',
 'julianavolberding@gmail.com',
 'katharina.chu@gmx.de',
 'cj@cjyetman.com',
 'fabio.venturini@gmail.com',
 'capricornjain@gmail.com',
 'julia.goransdotter@gmail.com',
 'stephaniebergeronline@yahoo.com',
 'bulovic.ana@gmail.com',
 'laxmita666@gmail.com',
 'brian.pertti@gmail.com',
 'kiaa14@gmail.com',
 'ajacuthbertson@gmail.com',
 'epperleind@gmail.com',
 'bastian.brabec@posteo.de',

 'huwg@mailbox.org',
 'huwg@mailbox.org',
 'paula.schulz@aol.de',
 'ftbacpdapyqbhcfchc@kvhrr.com',
 'oneunitedflower@gmail.com', 'sebastian.hoerner@gmx.de', 'brian.pertti@gmail.com', 'diarmaiddeburca@gmail.com', 'c.dauchy14@eabjm.org', 'camilo.b.c@hotmail.com', None, 'caro.tyka@gmail.com', 'melindagonzalez2000@gmail.com', 'knitterprofessor@gmail.com', 'carloshvieira2@gmail.com', 'ftbacpdapyqbhcfchc@kvhrr.com', None, 'classiclenny@gmail.com', 'danliebenthal77@gmail.com', 'caro.tyka@gmail.com', 'mandytory88@gmail.com', 'ansomertz@gmail.com', 'stefanvonulan@googlemail.com', 'mandytory88@gmail.com', 'sandraschmidt.bbg@gmail.com', 'm.gloegl@gmail.com', 'gabezcua@gmail.com', 'louisschamrothgreen@gmail.com', 'ankatrin@posteo.net', 'kiezburn@psychonautical.org', 'natan.sitis@gmail.com', 'kris@microdisko.no', 'edanner@gmail.com', 'krachschmidt@freenet.de', 'giulia.brabetz@gmx.de', 'johannes.kloeppner@googlemail.com', 'freja.a.knudsen@gmail.com', 'caporusciochiara1@gmail.com', 'jarr.wright@gmail.com']
    asset = set(test)
    from pprintpp import pprint
    pprint(asset)

if __name__ == '__main__':
    main()

