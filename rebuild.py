import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add scrollbar CSS
html = html.replace(
"""        .card-front {
            background-image: radial-gradient(#cbd5e1 1.5px, transparent 1.5px);
            background-size: 16px 16px;
        }
    </style>""",
"""        .card-front {
            background-image: radial-gradient(#cbd5e1 1.5px, transparent 1.5px);
            background-size: 16px 16px;
        }

        /* Hide scrollbar for Chrome, Safari and Opera */
        .no-scrollbar::-webkit-scrollbar {
            display: none;
        }

        /* Hide scrollbar for IE, Edge and Firefox */
        .no-scrollbar {
            -ms-overflow-style: none; /* IE and Edge */
            scrollbar-width: none; /* Firefox */
        }
    </style>""")

# 2. Add Quiz Section
quiz_html = """
        <!-- Quiz Section -->
        <div class="max-w-2xl mx-auto mb-16 bg-white p-8 rounded-3xl border border-slate-200 shadow-sm text-center">
            <h2 class="text-2xl font-bold mb-4 text-slate-800">Mini Quiz</h2>
            <div x-show="!quiz.active">
                <button @click="startQuiz()" class="bg-black text-white px-6 py-3 rounded-xl font-bold hover:bg-slate-800 transition-colors">Start Quiz</button>
            </div>
            <div x-show="quiz.active">
                <div class="text-7xl font-sans mb-6 text-slate-800" x-text="quiz.questions[quiz.currentIndex] ? quiz.questions[quiz.currentIndex].kanji : ''"></div>
                <input x-ref="quizInput" type="text" x-model="quiz.answer" @keyup.enter="handleEnter()" :readonly="quiz.message !== ''" placeholder="Type meaning in English..." class="w-full max-w-xs border-2 border-slate-200 px-4 py-3 rounded-xl text-center focus:outline-none focus:border-black mb-4 text-lg read-only:bg-slate-50 read-only:text-slate-500">
                <div class="flex justify-center gap-4">
                    <button @click="handleEnter()" class="bg-black text-white px-6 py-3 rounded-xl font-bold hover:bg-slate-800 transition-colors" x-text="quiz.message ? 'Next Question' : 'Submit'"></button>
                </div>
                <div class="mt-6 text-2xl font-bold" :class="quiz.message === 'Correct!' ? 'text-green-500' : 'text-red-500'" x-text="quiz.message"></div>
                <div class="mt-2 text-lg text-slate-600 font-medium" x-show="quiz.message && quiz.message !== 'Correct!'">
                    Answer: <span x-text="quiz.questions[quiz.currentIndex]?.answers.join(', ')"></span>
                </div>
            </div>
        </div>

        <!-- Flashcard Grid -->"""

html = html.replace('        <!-- Flashcard Grid -->', quiz_html)

# 3. Replace Back Face
back_html = """                        <!-- Back Face -->
                        <div class="absolute inset-0 w-full h-full backface-hidden rotate-y-180 bg-white text-slate-800 rounded-3xl p-6 flex flex-col justify-start items-center text-center shadow-2xl border border-slate-200 overflow-y-auto no-scrollbar">
                            <button @click.prevent.stop="toggleBookmark(kanji)" class="absolute top-4 right-4 p-2 rounded-full hover:bg-slate-100 transition-colors z-10 group/btn shrink-0">
                                <svg class="w-7 h-7 transition-all duration-300 group-hover/btn:scale-110" :class="kanji.bookmarked ? 'text-yellow-400 fill-yellow-400' : 'text-slate-200 fill-none stroke-current'" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                                </svg>
                            </button>
                            <h3 class="text-3xl font-bold text-black mb-3 mt-2 leading-tight shrink-0" x-text="kanji.meaning"></h3>
                            <div class="flex flex-col gap-1 w-full mb-3 shrink-0">
                                <p class="text-[0.7rem] font-bold text-slate-400 uppercase tracking-widest">Readings</p>
                                <p class="text-sm text-slate-700 font-mono bg-slate-50 py-1.5 px-3 rounded-lg border border-slate-200" x-text="kanji.reading"></p>
                            </div>
                            <div class="flex flex-col gap-1 w-full mb-3 text-left shrink-0" x-show="kanji.example_ja">
                                <p class="text-[0.7rem] font-bold text-slate-400 uppercase tracking-widest text-center">Example</p>
                                <div class="bg-blue-50/40 border border-blue-100 p-3 rounded-xl">
                                    <p class="font-bold text-blue-900 text-lg mb-0.5" x-text="kanji.example_ja"></p>
                                    <p class="text-xs text-blue-800/80 mb-1 font-mono" x-text="kanji.example_read"></p>
                                    <p class="text-sm text-slate-600 leading-snug" x-text="kanji.example_en"></p>
                                </div>
                            </div>
                            <div class="relative mt-auto pt-3 border-t border-slate-100 w-full shrink-0">
                                <p class="text-[0.90rem] text-slate-500 italic leading-snug" x-text="kanji.origin_story"></p>
                            </div>
                        </div>"""

html = re.sub(r'<!-- Back Face -->.*?</div>\s*</div>\s*</div>', back_html + '\n                    </div>\n                </div>', html, flags=re.DOTALL)

# 4. Add Alpine logic
alpine_state = """                searchQuery: '',
                showBookmarksOnly: false,
                quiz: {
                    active: false,
                    questions: [],
                    currentIndex: 0,
                    answer: '',
                    message: '',
                    shuffle(array) {
                        let currentIndex = array.length, randomIndex;
                        while (currentIndex !== 0) {
                            randomIndex = Math.floor(Math.random() * currentIndex);
                            currentIndex--;
                            [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
                        }
                        return array;
                    }
                },
                handleEnter() {
                    if (this.quiz.message !== '') {
                        this.nextQuestion();
                    } else if (this.quiz.answer.trim() !== '') {
                        this.checkAnswer();
                    }
                },
                startQuiz() {
                    this.quiz.active = true;
                    this.quiz.currentIndex = 0;
                    this.quiz.answer = '';
                    this.quiz.message = '';
                    this.quiz.shuffle(this.quiz.questions);
                    this.$nextTick(() => { if (this.$refs.quizInput) this.$refs.quizInput.focus(); });
                },
                checkAnswer() {
                    let answers = this.quiz.questions[this.quiz.currentIndex].answers;
                    if (answers.includes(this.quiz.answer.toLowerCase().trim())) {
                        this.quiz.message = 'Correct!';
                    } else {
                        this.quiz.message = 'Incorrect.';
                    }
                },
                nextQuestion() {
                    if (this.quiz.currentIndex < this.quiz.questions.length - 1) {
                        this.quiz.currentIndex++;
                        this.quiz.answer = '';
                        this.quiz.message = '';
                        this.$nextTick(() => { if (this.$refs.quizInput) this.$refs.quizInput.focus(); });
                    } else {
                        this.quiz.active = false;
                        this.quiz.message = 'Quiz finished!';
                    }
                },
                init() {"""
html = html.replace('                searchQuery: \'\',\n                showBookmarksOnly: false,\n                init() {', alpine_state)

init_logic = """                init() {
                    const saved = JSON.parse(localStorage.getItem('kanji-bookmarks') || '[]');
                    this.kanjis = this.kanjis.map(k => ({
                        ...k,
                        bookmarked: saved.includes(k.kanji)
                    }));
                    this.quiz.questions = this.kanjis.map(k => ({
                        kanji: k.kanji,
                        answers: k.meaning.toLowerCase().split(/[\\/,]/).map(w => w.trim())
                    }));
                },"""
html = re.sub(r'init\(\) \{.*?\},', init_logic, html, flags=re.DOTALL)

# 5. Expand Kanji Data safely using Python dict directly in JS construction
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

# Now properly replace the kanjis array
start_idx = html.find('kanjis: [')
end_idx = html.find('],', start_idx)
old_block = html[start_idx:end_idx]

import ast

items = re.findall(r"{\s*kanji:\s*'([^']+)',\s*meaning:\s*'([^']+)',\s*reading:\s*'([^']+)',\s*origin_story:\s*'((?:[^']|\\')*)'", old_block)

new_lines = []
for kanji, meaning, reading, story in items:
    if kanji in expanded_data:
        ex = expanded_data[kanji]
        import json
        mean = json.dumps(ex['meaning'])
        read = json.dumps(ex['reading'])
        ex_ja = json.dumps(ex['example_ja'])
        ex_rd = json.dumps(ex['example_read'])
        ex_en = json.dumps(ex['example_en'])
        st=json.dumps(story.replace("\\'", "'")) # safe JSON dumps
        new_lines.append(f"                    {{ kanji: '{kanji}', meaning: {mean}, reading: {read}, origin_story: {st}, example_ja: {ex_ja}, example_read: {ex_rd}, example_en: {ex_en} }},")
    else:
        st=json.dumps(story.replace("\\'", "'"))
        new_lines.append(f"                    {{ kanji: '{kanji}', meaning: '{meaning}', reading: '{reading}', origin_story: {st}, example_ja: '', example_read: '', example_en: '' }},")

html = html[:start_idx] + "kanjis: [\n" + "\n".join(new_lines) + "\n                 " + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
