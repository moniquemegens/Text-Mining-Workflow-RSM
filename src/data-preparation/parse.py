import json

f = open('../../gen/data-preparation/temp/whitehouse_briefing_27_04.json','r', encoding='utf-8')

con = f.readlines()

outfile = open('../../gen/data-preparation/temp/parsed-data.csv', 'w', encoding = 'utf-8')

outfile.write('tweet_id\tuser_id\tfollowers\tfollowing\tcreated_at\tlanguage\ttext\tswearword_count\tsource\n')

cnt = 0
for line in con:
    if (len(line)<=5): continue

    cnt+=1

    obj = json.loads(line.replace('\n',''))

    text = obj.get('text')
    text = text.replace('\t', '').replace('\n', '')

    swearwords = ['arse', 'ass', 'asshole', 'assholes', 'bastard', 'bastards', 'bitch', 'bitches', 'bugger', 'bullshit',
                  'crap', 'cunt', 'damn', 'dick', 'dickhead', 'dickheads', 'fuck', 'fucking', 'fuckin', 'goddamn',
                  'hate', 'hell', 'idiot', 'idiots', 'motherfucker', 'motherfuckers', 'moron', 'morons', 'piss',
                  'prick', 'pricks', 'pussy', 'shit', 'shitass', 'slut', 'son of a bitch', 'trashy', 'wanker', 'wanker', 'whore']

    swearword_count = 0

    text_swear_count = text.lower().replace('.', ' ').replace(',', ' ').replace('#', ' ') \
        .replace('!', ' ').replace('?', ' ').replace(':', ' ').replace(';', ' ').replace('&', ' ') \
        .replace('/', ' ').replace('&', ' ').split()

    for word in text_swear_count:
        if word in swearwords:
            swearword_count += 1

    outfile.write(obj.get('id_str') + '\t' + obj.get('user').get('id_str') + '\t' + str(obj.get('user').get('followers_count'))
                  + '\t' + str(obj.get('user').get('friends_count')) + '\t' + obj.get('created_at') + '\t' +
                  obj.get('lang') + '\t' + text + '\t' + str(swearword_count) + '\t' + str(obj.get('source')) + '\n')
    #if (cnt>2000): break

print('done.')