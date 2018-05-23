import csv

baseEntity = "http://www.games.com/entity/"
baseProperty = "http://www.games.com/pred/"

triples = []
publishers = []
platforms = []

filename = "clean_data/" + input("Filename: ")
file_in = open(filename, 'r', encoding='utf-8')
reader = csv.reader(file_in)
for sub, pred, obj in reader:
    if pred == 'Publisher':
        publishers.append(obj)
    elif pred == 'Platform':
        platforms.append(obj)
    triples.append((sub, pred, obj))
file_in.close()

file_platforms = open('clean_data/platforms_info.csv', 'r', encoding='utf-8')
platform_reader = csv.reader(file_platforms)
for sub, pred, obj in platform_reader:
    triples.append((sub, pred, obj))
file_platforms.close()

file_out = open('games.nt', 'w')
for sub, pred, obj in triples:
    uri_sub = '<' + baseEntity + str(sub).lower().replace(' ', '_') + '>'
    uri_pred = '<' + baseProperty + str(pred).lower().replace(' ', '_') + '>'
    if obj in platforms or obj in publishers:
        uri_obj = '<' + baseEntity + str(obj).lower().replace(' ', '_') + '>'
    else:
        uri_obj = '"' + obj + '"'
    file_out.write('{} {} {} .\n'.format(uri_sub, uri_pred, uri_obj))
file_out.close()
print("games.nt created")
