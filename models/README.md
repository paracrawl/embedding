**Framework** PyTorch

**Optimizer** ADAM, initial learning rate 0.01, decreases by 10% whenever perplexity does not imrpove

**Loss function** MSELoss

**Pipeline**

[Sentence]  -> Lang-specific-BLSTM -> MaxPool     -> Lang-specific-Decoder -> [Sentence]
<96×50×394> -> <96×50×1024> -> <96×1×1024> -> <96×50×384>

*[Sentence] is a tensor of size <96×50×384>, where 96 is batch size, 50 is sequence (sentence) length, 384 is the word embedding size*

The model stores weights for all language-specific encoders/decoders. Uses them based on the tags supplied with the batch specification.
So far, a new model is created for every language pair. Gradients should be nullified after every batch (not after every language pair), so that loss/gradients are accumulated.
