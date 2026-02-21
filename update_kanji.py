import re
import json

html_file = 'index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

expanded_data = {
    '一': {'meaning': 'One', 'reading': 'ichi, itsu / hito-, hito.tsu', 'example_ja': '一日', 'example_read': 'tsuitachi / ichinichi', 'example_en': 'First day of the month / One day'},
    '二': {'meaning': 'Two', 'reading': 'ni, ji / futa, futa.tsu', 'example_ja': '二人', 'example_read': 'futari', 'example_en': 'Two people'},
    '三': {'meaning': 'Three', 'reading': 'san / mi, mi.tsu, mit.tsu', 'example_ja': '三日月', 'example_read': 'mikazuki', 'example_en': 'Crescent moon (3rd-day moon)'},
    '四': {'meaning': 'Four', 'reading': 'shi / yon, yo, yo.tsu, yot.tsu', 'example_ja': '四季', 'example_read': 'shiki', 'example_en': 'Four seasons'},
    '五': {'meaning': 'Five', 'reading': 'go / itsu, itsu.tsu', 'example_ja': '五感', 'example_read': 'gokan', 'example_en': 'The five senses'},
    '六': {'meaning': 'Six', 'reading': 'roku, riku / mu, mu.tsu, mut.tsu', 'example_ja': '六本木', 'example_read': 'Roppongi', 'example_en': 'Roppongi (place name)'},
    '七': {'meaning': 'Seven', 'reading': 'shichi / nana, nana.tsu', 'example_ja': '七夕', 'example_read': 'tanabata', 'example_en': 'Star Festival'},
    '八': {'meaning': 'Eight', 'reading': 'hachi / ya, ya.tsu, yat.tsu, you', 'example_ja': '八百屋', 'example_read': 'yaoya', 'example_en': 'Greengrocer'},
    '九': {'meaning': 'Nine', 'reading': 'kyuu, ku / kokono, kokono.tsu', 'example_ja': '九州', 'example_read': 'Kyuushuu', 'example_en': 'Kyushu (island)'},
    '十': {'meaning': 'Ten', 'reading': 'juu, ji, to, too', 'example_ja': '十分', 'example_read': 'juubun', 'example_en': 'Enough / Sufficient'},
    '百': {'meaning': 'Hundred', 'reading': 'hyaku, byaku / momo', 'example_ja': '百貨店', 'example_read': 'hyakkaten', 'example_en': 'Department store'},
    '千': {'meaning': 'Thousand', 'reading': 'sen / chi', 'example_ja': '千葉', 'example_read': 'Chiba', 'example_en': 'Chiba (prefecture, lit. Thousand leaves)'},
    '万': {'meaning': 'Ten Thousand, Many', 'reading': 'man, ban / yorozu', 'example_ja': '万歳', 'example_read': 'banzai', 'example_en': 'Hurrah / Long life'},
    '円': {'meaning': 'Yen, Circle, Round', 'reading': 'en / maru.i', 'example_ja': '円滑', 'example_read': 'enkatsu', 'example_en': 'Smooth / Unhindered'},
    '日': {'meaning': 'Sun, Day, Japan', 'reading': 'nichi, jitsu / hi, -bi, -ka', 'example_ja': '日曜日', 'example_read': 'nichiyoubi', 'example_en': 'Sunday'},
    '月': {'meaning': 'Moon, Month', 'reading': 'getsu, gatsu / tsuki', 'example_ja': '今月', 'example_read': 'kongetsu', 'example_en': 'This month'},
    '火': {'meaning': 'Fire', 'reading': 'ka / hi, -bi, ho-', 'example_ja': '花火', 'example_read': 'hanabi', 'example_en': 'Fireworks'},
    '水': {'meaning': 'Water', 'reading': 'sui / mizu', 'example_ja': '水星', 'example_read': 'suisei', 'example_en': 'Mercury (planet)'},
    '木': {'meaning': 'Tree, Wood', 'reading': 'boku, moku / ki, ko-', 'example_ja': '木漏れ日', 'example_read': 'komorebi', 'example_en': 'Sunlight filtering through trees'},
    '金': {'meaning': 'Gold, Money, Metal', 'reading': 'kin, kon, gon / kane, kana-', 'example_ja': 'お金持ち', 'example_read': 'okanemochi', 'example_en': 'Rich person'},
    '土': {'meaning': 'Earth, Soil, Ground', 'reading': 'do, to / tsuchi', 'example_ja': 'お土産', 'example_read': 'omiyage', 'example_en': 'Souvenir'},
    '山': {'meaning': 'Mountain', 'reading': 'san, zan / yama', 'example_ja': '富士山', 'example_read': 'Fujisan', 'example_en': 'Mount Fuji'},
    '川': {'meaning': 'River, Stream', 'reading': 'sen / kawa', 'example_ja': '天の川', 'example_read': 'amanogawa', 'example_en': 'The Milky Way'},
    '人': {'meaning': 'Person, Human', 'reading': 'jin, nin / hito', 'example_ja': '人間', 'example_read': 'ningen', 'example_en': 'Human being'},
    '男': {'meaning': 'Man, Male', 'reading': 'dan, nan / otoko', 'example_ja': '男の子', 'example_read': 'otokonoko', 'example_en': 'Boy'},
    '女': {'meaning': 'Woman, Female', 'reading': 'jo, nyo, nyou / onna, me', 'example_ja': '女神', 'example_read': 'megami', 'example_en': 'Goddess'},
    '子': {'meaning': 'Child, Offspring', 'reading': 'shi, su, tsu / ko, -ko', 'example_ja': '迷子', 'example_read': 'maigo', 'example_en': 'Lost child'},
    '目': {'meaning': 'Eye, Vision', 'reading': 'moku, boku / me, -me, ma-', 'example_ja': '目的', 'example_read': 'mokuteki', 'example_en': 'Purpose / Goal'},
    '耳': {'meaning': 'Ear, Hearing', 'reading': 'ji / mimi', 'example_ja': '耳打ち', 'example_read': 'mimiuchi', 'example_en': 'Whispering in ear'},
    '口': {'meaning': 'Mouth, Entrance', 'reading': 'kou, ku / kuchi', 'example_ja': '非常口', 'example_read': 'hijouguchi', 'example_en': 'Emergency exit'},
    '手': {'meaning': 'Hand, Skill', 'reading': 'shu, zu / te, -te, ta-', 'example_ja': '苦手', 'example_read': 'nigate', 'example_en': 'Weak at / Dislike'},
    '足': {'meaning': 'Foot, Leg, Sufficient', 'reading': 'soku / ashi, ta.riru, ta.su', 'example_ja': '満足', 'example_read': 'manzoku', 'example_en': 'Satisfaction'},
    '上': {'meaning': 'Up, Above, Top', 'reading': 'jou, shou, shan / ue, uwa-, kami', 'example_ja': '上手', 'example_read': 'jouzu', 'example_en': 'Skillful'},
    '下': {'meaning': 'Down, Below, Bottom', 'reading': 'ka, ge / shita, shimo, moto', 'example_ja': '地下鉄', 'example_read': 'chikatetsu', 'example_en': 'Subway'},
    '中': {'meaning': 'Middle, Inside, Center', 'reading': 'chuu / naka, uchi, ata.ru', 'example_ja': '世界中', 'example_read': 'sekaijuu', 'example_en': 'All over the world'},
    '外': {'meaning': 'Outside, External', 'reading': 'gai, ge / soto, hoka, hazu.su', 'example_ja': '外国人', 'example_read': 'gaikokujin', 'example_en': 'Foreigner'},
    '右': {'meaning': 'Right', 'reading': 'uu, you / migi', 'example_ja': '右利き', 'example_read': 'migikiki', 'example_en': 'Right-handed'},
    '左': {'meaning': 'Left', 'reading': 'sa, sha / hidari', 'example_ja': '左翼', 'example_read': 'sayoku', 'example_en': 'Left-wing'},
    '大': {'meaning': 'Big, Large', 'reading': 'dai, tai / oo-, oo.kii', 'example_ja': '大丈夫', 'example_read': 'daijoubu', 'example_en': 'Okay / All right'},
    '小': {'meaning': 'Small, Little', 'reading': 'shou / chii.sai, ko-, o-', 'example_ja': '小説', 'example_read': 'shousetsu', 'example_en': 'Novel'},
    '高': {'meaning': 'High, Tall, Expensive', 'reading': 'kou / taka.i, taka, taka.maru', 'example_ja': '高校', 'example_read': 'koukou', 'example_en': 'High school'},
    '安': {'meaning': 'Cheap, Safe, Peaceful', 'reading': 'an / yasu.i, yasu.maru', 'example_ja': '安心', 'example_read': 'anshin', 'example_en': 'Peace of mind / Relief'},
    '新': {'meaning': 'New', 'reading': 'shin / atara.shii, ara.ta, nii-', 'example_ja': '新幹線', 'example_read': 'shinkansen', 'example_en': 'Bullet train'},
    '古': {'meaning': 'Old', 'reading': 'ko / furu.i, furu-', 'example_ja': '中古', 'example_read': 'chuuko', 'example_en': 'Used / Secondhand'},
    '長': {'meaning': 'Long, Leader, Superior', 'reading': 'chou / naga.i, osa', 'example_ja': '社長', 'example_read': 'shachou', 'example_en': 'Company president'},
    '多': {'meaning': 'Many, Frequent', 'reading': 'ta / oo.i, masa.ni', 'example_ja': '多分', 'example_read': 'tabun', 'example_en': 'Probably'},
    '少': {'meaning': 'Few, Little', 'reading': 'shou / suko.shi, suku.nai', 'example_ja': '少女', 'example_read': 'shoujo', 'example_en': 'Young girl'},
    '早': {'meaning': 'Early, Fast', 'reading': 'sou, saｯ / haya.i, haya, haya.maru', 'example_ja': '早起き', 'example_read': 'hayaoki', 'example_en': 'Early rising'},
    '行': {'meaning': 'Go, Conduct, Line', 'reading': 'kou, gyou, an / i.ku, yu.ku, okona.u', 'example_ja': '旅行', 'example_read': 'ryokou', 'example_en': 'Travel / Trip'},
    '来': {'meaning': 'Come, Next', 'reading': 'rai, tai / ku.ru, kita.ru', 'example_ja': '来年', 'example_read': 'rainen', 'example_en': 'Next year'},
    '食': {'meaning': 'Eat, Food', 'reading': 'shoku, jiki / ta.beru, ku.u, ku.rau', 'example_ja': '食べ放題', 'example_read': 'tabehoudai', 'example_en': 'All-you-can-eat'},
    '飲': {'meaning': 'Drink', 'reading': 'in, on / no.mu', 'example_ja': '飲み物', 'example_read': 'nomimono', 'example_en': 'Drink / Beverage'},
    '見': {'meaning': 'See, Look, Idea', 'reading': 'ken / mi.ru, mi.eru, mi.seru', 'example_ja': '花見', 'example_read': 'hanami', 'example_en': 'Cherry blossom viewing'},
    '聞': {'meaning': 'Hear, Listen, Ask', 'reading': 'bun, mon / ki.ku, ki.koeru', 'example_ja': '新聞', 'example_read': 'shinbun', 'example_en': 'Newspaper'},
    '読': {'meaning': 'Read', 'reading': 'doku, toku, tou / yo.mu', 'example_ja': '読書', 'example_read': 'dokusho', 'example_en': 'Reading books'},
    '書': {'meaning': 'Write, Book, Document', 'reading': 'sho / ka.ku', 'example_ja': '図書館', 'example_read': 'toshokan', 'example_en': 'Library'},
    '話': {'meaning': 'Speak, Talk, Story', 'reading': 'wa / hana.su, hanashi', 'example_ja': '電話', 'example_read': 'denwa', 'example_en': 'Telephone'},
    '買': {'meaning': 'Buy', 'reading': 'bai / ka.u', 'example_ja': '買い物', 'example_read': 'kaimono', 'example_en': 'Shopping'},
    '教': {'meaning': 'Teach, Faith, Doctrine', 'reading': 'kyou / oshi.eru, oso.waru', 'example_ja': '教室', 'example_read': 'kyoushitsu', 'example_en': 'Classroom'},
    '休': {'meaning': 'Rest, Day off, Retire', 'reading': 'kyuu / yasu.mu, yasu.maru', 'example_ja': '夏休み', 'example_read': 'natsuyasumi', 'example_en': 'Summer vacation'},
    '立': {'meaning': 'Stand, Establish', 'reading': 'ritsu, ryuu / ta.tsu, ta.teru', 'example_ja': '目立つ', 'example_read': 'medatsu', 'example_en': 'To stand out'},
    '座': {'meaning': 'Sit, Seat, Theater', 'reading': 'za / suwa.ru', 'example_ja': '口座', 'example_read': 'kouza', 'example_en': 'Bank account'},
    '今': {'meaning': 'Now, This', 'reading': 'kon, kin / ima', 'example_ja': '今日', 'example_read': 'kyou', 'example_en': 'Today'},
    '時': {'meaning': 'Time, Hour', 'reading': 'ji / toki, -doki', 'example_ja': '時計', 'example_read': 'tokei', 'example_en': 'Clock / Watch'},
    '分': {'meaning': 'Minute, Part, Understand', 'reading': 'bun, fun, bu / wa.keru, wa.karu', 'example_ja': '自分', 'example_read': 'jibun', 'example_en': 'Myself / Oneself'},
    '半': {'meaning': 'Half, Middle', 'reading': 'han / naka.ba', 'example_ja': '半年', 'example_read': 'hantoshi', 'example_en': 'Half a year'},
    '午': {'meaning': 'Noon, Sign of the horse', 'reading': 'go / uma', 'example_ja': '午前', 'example_read': 'gozen', 'example_en': 'Morning / AM'},
    '前': {'meaning': 'Before, Front', 'reading': 'zen / mae', 'example_ja': '名前', 'example_read': 'namae', 'example_en': 'Name'},
    '後': {'meaning': 'After, Behind', 'reading': 'go, kou / ushi.ro, ato, nochi', 'example_ja': '午後', 'example_read': 'gogo', 'example_en': 'Afternoon / PM'},
    '去': {'meaning': 'Past, Leave, Quit', 'reading': 'kyo, ko / sa.ru', 'example_ja': '去年', 'example_read': 'kyonen', 'example_en': 'Last year'},
    '年': {'meaning': 'Year', 'reading': 'nen / toshi', 'example_ja': '今年', 'example_read': 'kotoshi', 'example_en': 'This year'},
    '毎': {'meaning': 'Every', 'reading': 'mai / goto', 'example_ja': '毎日', 'example_read': 'mainichi', 'example_en': 'Every day'},
    '何': {'meaning': 'What', 'reading': 'ka / nani, nan', 'example_ja': '何か', 'example_read': 'nanika', 'example_en': 'Something'},
    '春': {'meaning': 'Spring', 'reading': 'shun / haru', 'example_ja': '青春', 'example_read': 'seishun', 'example_en': 'Youth'},
    '夏': {'meaning': 'Summer', 'reading': 'ka, ge / natsu', 'example_ja': '真夏', 'example_read': 'manatsu', 'example_en': 'Midsummer'},
    '秋': {'meaning': 'Autumn, Fall', 'reading': 'shuu / aki', 'example_ja': '秋分', 'example_read': 'shuubun', 'example_en': 'Autumnal equinox'},
    '冬': {'meaning': 'Winter', 'reading': 'tou / fuyu', 'example_ja': '真冬', 'example_read': 'mafuyu', 'example_en': 'Midwinter'},
    '北': {'meaning': 'North', 'reading': 'hoku / kita', 'example_ja': '北海道', 'example_read': 'Hokkaidou', 'example_en': 'Hokkaido (island)'},
    '南': {'meaning': 'South', 'reading': 'nan, na / minami', 'example_ja': '南口', 'example_read': 'minamiguchi', 'example_en': 'South exit'},
    '東': {'meaning': 'East', 'reading': 'tou / higashi', 'example_ja': '東京', 'example_read': 'Toukyou', 'example_en': 'Tokyo'},
    '西': {'meaning': 'West', 'reading': 'sei, sai / nishi', 'example_ja': '関西', 'example_read': 'Kansai', 'example_en': 'Kansai (region)'},
    '雨': {'meaning': 'Rain', 'reading': 'u / ame, ama-', 'example_ja': '大雨', 'example_read': 'ooame', 'example_en': 'Heavy rain'},
    '天': {'meaning': 'Sky, Heaven', 'reading': 'ten / amatsu, ame', 'example_ja': '天気', 'example_read': 'tenki', 'example_en': 'Weather'},
    '空': {'meaning': 'Sky, Empty, Void', 'reading': 'kuu / sora, a.ku, kara', 'example_ja': '空気', 'example_read': 'kuuki', 'example_en': 'Air / Atmosphere'},
    '気': {'meaning': 'Spirit, Mind, Air', 'reading': 'ki, ke / iki', 'example_ja': '元気', 'example_read': 'genki', 'example_en': 'Healthy / Energetic'},
    '車': {'meaning': 'Car, Wheel', 'reading': 'sha / kuruma', 'example_ja': '電車', 'example_read': 'densha', 'example_en': 'Train'},
    '電': {'meaning': 'Electricity', 'reading': 'den', 'example_ja': '電話', 'example_read': 'denwa', 'example_en': 'Telephone'},
    '馬': {'meaning': 'Horse', 'reading': 'ba / uma, ma', 'example_ja': '乗馬', 'example_read': 'jouba', 'example_en': 'Horse riding'},
    '魚': {'meaning': 'Fish', 'reading': 'gyo / sakana, uo', 'example_ja': '金魚', 'example_read': 'kingyo', 'example_en': 'Goldfish'},
    '鳥': {'meaning': 'Bird', 'reading': 'chou / tori', 'example_ja': '焼き鳥', 'example_read': 'yakitori', 'example_en': 'Grilled chicken skewers'},
    '語': {'meaning': 'Language, Word, Tell', 'reading': 'go / kata.ru', 'example_ja': '日本語', 'example_read': 'nihongo', 'example_en': 'Japanese language'},
    '名': {'meaning': 'Name, Noted, Distinguished', 'reading': 'mei, myou / na', 'example_ja': '有名', 'example_read': 'yuumei', 'example_en': 'Famous'},
    '店': {'meaning': 'Store, Shop', 'reading': 'ten / mise', 'example_ja': '喫茶店', 'example_read': 'kissaten', 'example_en': 'Coffee shop'},
    '駅': {'meaning': 'Station', 'reading': 'eki', 'example_ja': '駅長', 'example_read': 'ekichou', 'example_en': 'Stationmaster'},
    '道': {'meaning': 'Road, Way, Path', 'reading': 'dou, tou / michi', 'example_ja': '柔道', 'example_read': 'juudou', 'example_en': 'Judo'},
    '社': {'meaning': 'Company, Shrine, Society', 'reading': 'sha / yashiro', 'example_ja': '会社', 'example_read': 'kaisha', 'example_en': 'Company'},
    '国': {'meaning': 'Country, Nation', 'reading': 'koku / kuni', 'example_ja': '外国', 'example_read': 'gaikoku', 'example_en': 'Foreign country'},
    '白': {'meaning': 'White', 'reading': 'haku, byaku / shiro, shiro.i', 'example_ja': '面白い', 'example_read': 'omoshiroi', 'example_en': 'Interesting'},
    '黒': {'meaning': 'Black', 'reading': 'koku / kuro, kuro.i', 'example_ja': '黒板', 'example_read': 'kokuban', 'example_en': 'Blackboard'},
    '赤': {'meaning': 'Red', 'reading': 'seki, shaku / aka, aka.i', 'example_ja': '赤ちゃん', 'example_read': 'akachan', 'example_en': 'Baby'},
    '青': {'meaning': 'Blue, Green', 'reading': 'sei, shou / ao, ao.i', 'example_ja': '青年', 'example_read': 'seinen', 'example_en': 'Youth / Young man'},
    '入': {'meaning': 'Enter, Insert', 'reading': 'nyuu / i.reru, hai.ru', 'example_ja': '入口', 'example_read': 'iriguchi', 'example_en': 'Entrance'},
    '出': {'meaning': 'Exit, Leave, Protude', 'reading': 'shutsu, sui / de.ru, da.su', 'example_ja': '出口', 'example_read': 'deguchi', 'example_en': 'Exit'},
    '友': {'meaning': 'Friend', 'reading': 'yuu / tomo', 'example_ja': '友達', 'example_read': 'tomodachi', 'example_en': 'Friend'},
    '校': {'meaning': 'School, Exam', 'reading': 'kou, kyou', 'example_ja': '学校', 'example_read': 'gakkou', 'example_en': 'School'},
    '勉': {'meaning': 'Exertion, Endeavor', 'reading': 'ben / tsuto.meru', 'example_ja': '勉強', 'example_read': 'benkyou', 'example_en': 'Study'},
    '母': {'meaning': 'Mother', 'reading': 'bo / haha, mo', 'example_ja': 'お母さん', 'example_read': 'okaasan', 'example_en': 'Mother'},
    '父': {'meaning': 'Father', 'reading': 'fu / chichi', 'example_ja': 'お父さん', 'example_read': 'otousan', 'example_en': 'Father'},
    '学': {'meaning': 'Study, Learning, Science', 'reading': 'gaku / mana.bu', 'example_ja': '学生', 'example_read': 'gakusei', 'example_en': 'Student'},
    '先': {'meaning': 'Before, Ahead, Previous', 'reading': 'sen / saki, ma.zu', 'example_ja': '先生', 'example_read': 'sensei', 'example_en': 'Teacher'},
    '生': {'meaning': 'Life, Genuine, Birth', 'reading': 'sei, shou / i.kiru, u.mu, nama', 'example_ja': '誕生日', 'example_read': 'tanjoubi', 'example_en': 'Birthday'},
}

# Regex to find kanjis array in index.html and update it
pattern = r"kanjis:\s*\[\s*({\s*kanji:.*?})\s*\],"
# Wait, parsing this with regex is hard. Let's do string replacement manually based on lines.

lines = content.split('\n')
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'kanjis: [' in line:
        start_idx = i
    if start_idx != -1 and '],' in line and i > start_idx + 50:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    # Build new kanjis array
    new_lines = [lines[start_idx]]
    
    # We need to extract the origin story to keep it.
    old_block = "\n".join(lines[start_idx:end_idx])
    import ast
    
    # We will just regex matching for each kanji inside the block
    items = re.findall(r"{\s*kanji:\s*'([^']+)',\s*meaning:\s*'([^']+)',\s*reading:\s*'([^']+)',\s*origin_story:\s*'([^']+)'", old_block)
    
    for kanji, meaning, reading, story in items:
        # Get expanded data
        if kanji in expanded_data:
            ex = expanded_data[kanji]
            # Replace single quotes
            story = story.replace("'", "\\'")
            mean = ex['meaning'].replace("'", "\\'")
            read = ex['reading'].replace("'", "\\'")
            ex_ja = ex['example_ja'].replace("'", "\\'")
            ex_rd = ex['example_read'].replace("'", "\\'")
            ex_en = ex['example_en'].replace("'", "\\'")
            new_lines.append(f"                    {{ kanji: '{kanji}', meaning: '{mean}', reading: '{read}', origin_story: '{story}', example_ja: '{ex_ja}', example_read: '{ex_rd}', example_en: '{ex_en}', flipped: false }},")
        else:
            story = story.replace("'", "\\'")
            new_lines.append(f"                    {{ kanji: '{kanji}', meaning: '{meaning}', reading: '{reading}', origin_story: '{story}', example_ja: '', example_read: '', example_en: '', flipped: false }},")
            
    # Reassemble
    final_content = "\n".join(lines[:start_idx]) + "\n" + "\n".join(new_lines) + "\n                 ],\n" + "\n".join(lines[end_idx+1:])
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("Updated index.html successfully.")
else:
    print("Failed to find kanjis block.")
