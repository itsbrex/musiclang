import musiclang
from .base.predictor import BasePredictor


class ChordTransformerPredictor(BasePredictor):
    """
    Create a transformer model to predict chord progression model of a given score
    """
    def init_model(self, *args, **kwargs):
        from .transformer_model import TransformerModelWrapper
        from .chord_tokenizer import TOKENS
        n_tokens = len(TOKENS)  # size of vocabulary
        d_model = 50  # embedding dimension
        d_hid = 50  # dimension of the feedforward network model in nn.TransformerEncoder
        n_layers = 2  # number of nn.TransformerEncoderLayer in nn.TransformerEncoder
        n_head = 2  # number of heads in nn.MultiheadAttention
        dropout = 0.2  # dropout probability
        batch_size = 8
        bptt = 35
        return TransformerModelWrapper(n_tokens, d_model, n_head,  d_hid, n_layers, bptt, batch_size, dropout=dropout)


    def save_model(self, filepath):
        self.model.save_model(filepath)

    @classmethod
    def load_model(cls, filepath, *args, **kwargs):
        from .transformer_model import TransformerModelWrapper
        predictor = cls(*args, **kwargs)
        predictor.model = TransformerModelWrapper.load_model(filepath)
        return predictor


    def predict_from_text(self, start_text, include_start=True, n_tokens=5, max_tokens=None):
        if max_tokens is None:
            max_tokens = 3 * n_tokens

        if n_tokens >= max_tokens:
            raise ValueError('"n_tokens" should be less than "max_tokens"')
        chars = ''
        last_valid_candidate = None
        tokens = self.tokenize(start_text)
        prepend_text = '' if not include_start else start_text
        while True:
            from musiclang.predict.chord_tokenizer import get_candidates_idx, get_is_terminal
            is_terminal = get_is_terminal(start_text)
            if is_terminal and (len(chars) - len(start_text)) >= n_tokens:
                return prepend_text + chars
            elif is_terminal:
                last_valid_candidate = chars
            elif len(chars) > max_tokens:
                if last_valid_candidate is None:
                    raise Exception('Not able to predict a sentence, try increase the "max_tokens" parameter')
                return prepend_text + last_valid_candidate

            valid_candidates = get_candidates_idx(start_text)
            output = self.predict_proba(tokens)
            serie = (output + valid_candidates).argmax().tolist()
            text = self.untokenize([serie])
            chars += text
            start_text += text
            tokens = self.tokenize(start_text)

        return chars

    def score_to_text(self, score: 'musiclang.Score') -> str:
        from .chord_tokenizer import score_to_text
        return score_to_text(score)

    def tokenize(self, text):
        """
        Convert a text to a list of tokens (number)
        :param text:
        :return:
        """
        from .chord_tokenizer import tokenize_string
        tokens = tokenize_string(text)
        return tokens

    def untokenize(self, tokens):
        """
        Convert a list of tokens to a text
        :param tokens:
        :return:
        """
        from .chord_tokenizer import untokenize
        return untokenize(tokens)

    def text_to_score(self, text):
        """
        :param text:
        :return:
        """
        from musiclang.core.library import I, II, III, IV, V, VI, VII
        # First make sure it compiles in musiclang code
        from .chord_tokenizer import PARSER
        if not text.endswith(';'):
            text += ';'
        PARSER.parse(text)
        text = text.replace(';', '')
        score = eval(text)
        return score
