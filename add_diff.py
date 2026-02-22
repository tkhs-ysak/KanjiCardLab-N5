import re
import random

easy_kanjis = set('一二三四五六七八九十百千万円日月火水木金土山川人男女子目耳口手足上下中外右左大小')
medium_kanjis = set('高安新古長多少早行来食飲見聞読書話買教休立座今時分半午前過去年毎何春夏秋冬北南東西')
hard_kanjis = set('雨天空気車電馬魚鳥語名店駅道社国白黒赤青入出友校勉母父学先生')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('kanjis: [')
end_idx = html.find('],', start_idx)
old_block = html[start_idx:end_idx]

# Match the kanji elements
items = re.findall(r"(                    { kanji: '([^']+)', .*? })", old_block)

new_lines = []
for full_match, kanji in items:
    if kanji in easy_kanjis: diff = 'easy'
    elif kanji in medium_kanjis: diff = 'medium'
    elif kanji in hard_kanjis: diff = 'hard'
    else: diff = 'medium'
    
    new_line = full_match[:-2] + f", difficulty: '{diff}' }}"
    new_lines.append(new_line)

html = html[:start_idx] + 'kanjis: [\n' + '\n'.join(new_lines) + '\n                 ' + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated index.html kanjis')
