from transformers import AutoTokenizer, BertModel
from manim import *
import matplotlib


class SelfAttentionGraph(VGroup):
    """VGroup object for visualizing self attention scores."""

    def __init__(
        self,
        sentence,
        tokenizer,
        transformer,
        layer_index=0,
        head_index=0,
        device="cpu",
    ):
        """Takes a sentence and passes it through a given transformer model. 
        Saves each of the self attention scores for the given layer_id (with 
        a default being the first layer). Returns tensor of self attention 
        scores. The tensor is of shape (num_heads, seq_len, seq_len).

        Parameters
        ----------
        sentence : str
            Input text sentence
        tokenizer : transformers.Tokenizer
            Tokenizer to apply to the sentence
        transformer : transformers.PreTrainedModel
            Transformer model to pass the sentence through.
        layer_index : int, optional
            index of layer to pull attentions from, by default None
        device : str, optional
            device identifier string, by default "cpu"
        """
        super().__init__()
        self.sentence = sentence
        self.tokenizer = tokenizer
        self.transformer = transformer
        self.layer_index = layer_index
        self.head_index = head_index
        self.device = device
        # Compute the attention scores
        inputs = self.tokenizer(
            self.sentence, 
            return_tensors="pt"
        )
        self.tokens = self.tokenizer.convert_ids_to_tokens(
            inputs["input_ids"][0]
        )
        outputs = self.transformer(
            **inputs,
            output_attentions=True,
        )
        self.attention_scores = outputs.attentions[self.layer_index].squeeze()
        # Make the attention graph
        attention_graph = self.make_attention_graph()
        self.add(attention_graph)

    def make_attention_graph(self, token_spacing=0.6, side_spacing=4.0, cmap="inferno"):
        """Creates the graph of the attention scores"""
        graph = VGroup()
        left_tokens = self.tokens.copy()
        right_tokens = self.tokens.copy()
        left_text = []
        right_text = []
        # Plot the edges
        for token in left_tokens:
            left_text.append(
                Text(token)
            )
            if len(left_text) > 1:
                left_text[-1].next_to(
                    left_text[-2], 
                    DOWN, 
                    buff=token_spacing
                )
        left_tokens = VGroup(*left_text)

        for token in right_tokens:
            right_text.append(
                Text(token)
            )
            if len(right_text) > 1:
                right_text[-1].next_to(
                    right_text[-2], 
                    DOWN, 
                    buff=token_spacing
                )
        right_tokens = VGroup(*right_text)
        right_tokens.shift(
            side_spacing * RIGHT
        )
        # Plot the edges
        edges = VGroup()
        for token_index, token in enumerate(self.tokens):
            for other_token_index, other_token in enumerate(self.tokens):
                edge = Line(
                    left_tokens[token_index].get_center(),
                    right_tokens[other_token_index].get_center(),
                    stroke_width=4.0,
                )
                attention_score = self.attention_scores[self.head_index, token_index, other_token_index]
                cmap = matplotlib.cm.get_cmap(cmap)
                rgba = np.array(cmap(
                    attention_score.item()
                ))
                rgb = (rgba * 255).astype(int)
                hex = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

                edge.set_color(
                    hex
                )
                edges.add(edge)
        graph.add(edges)
        graph.add(left_tokens, right_tokens)

        return graph

class SelfAttentionGraphTest(Scene):

    def construct(self):
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        model = BertModel.from_pretrained("bert-base-uncased")

        self_attention_graph = SelfAttentionGraph(
            "This is a test sentence",
            tokenizer,
            model,
        )
        self_attention_graph.move_to(ORIGIN)
        self.add(self_attention_graph)
    