from z.text import Vocab
import unittest

class Test_Vocab(unittest.TestCase):

    def test_vocab(self):
        v = Vocab()
        vocab = v.get_vocab()
        print(v.file_path)
        print(list(v.tokens))
        for i in v.tokens:
            print(f'{i}: {vocab[i]}')
        print(f'<unk>: {vocab["<unk>"]}')
        print(f'outofdict: {vocab["outofdict"]}')

if __name__ == '__main__':
    unittest.main()