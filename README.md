# Trends in Bilingualism

A little project on looking into trends in Bilingualism from 1950 - 2023.

I use the PubMed API to get titles of all publications from their database for the keyword "bilingual*" and create a word cloud per decade to get an idea of trends i bilingualism research.

![2020s](https://github.com/dmnkfr/bilingual_clouds/blob/main/output/2020s.png?raw=true)

To reproduce the wordclouds, run:

    python main.py `
      -e firstname.lastname@email.com `
      -q "bilingual*" `
      -s bilingual bilingualism bilinguals bilingually monolingual monolinguals  monolingualbilingual language children

To run your own query and create a word cloud for each decade, you can run:

`python main.py -e <email> -q <query> -s <stopwords>`
