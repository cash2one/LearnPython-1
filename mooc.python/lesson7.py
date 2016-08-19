f = open("emma.txt")
word_freq = {}

for line in f:
    words = line.strip().split()
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
freq_word = []
for word, freq in word_freq.items():
    freq_word.append((freq, word))
freq_word.sort(reverse=True)
for freq, word in freq_word[:10]:
    print word
f.close()

d1 = {"zhang": 123, "wang": 456, "li": 123, "zhao": 456}
d2 = {}
for name, room in d1.items():
    if room in d2:
        d2[room].append(name)
    else:
        d2[room] = [name]
print d2


def load_dict(filename):
    word_dic = set()
    max_len = 1
    f = open(filename)
    for line in f:
        word = unicode(line.strip(), 'utf-8')
        word_dic.add(word)
        if len(word) > max_len:
            max_len = len(word)
    return max_len, word_dic


def from_word_seg(sent, max_len, word_dict):
    begin = 0
    words = []
    sent = unicode(sent, 'utf-8')
    while begin < len(sent):
        for end in range(begin + max_len, begin, -1):
            if sent[begin:end] in word_dict:
                words.append(sent[begin:end])
                break
        begin = end
    return words


max_len, word_dict = load_dict('lexicon.dic')
sent = raw_input('input:')
words = from_word_seg(sent, max_len, word_dict)
for word in words:
    print word
