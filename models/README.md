# Sentence Embedding Model

## Framework 

PyTorch

## Optimizer 

 - ADAM
 - initial learning rate 0.01, decreases by 10% whenever perplexity does not improve

## Loss function 

MSELoss

## Pipeline

[Sentence]  -> *Lang-specific-BLSTM* -> *MaxPool* -> *Lang-specific-Decoder* -> [Sentence]

<96×50×394> -> <96×50×1024> -> <96×1×1024> -> <96×50×384>

*[Sentence] is a tensor of size <96×50×384>, where 96 is batch size, 50 is sequence (sentence) length, 384 is the word embedding size*

The model stores weights for all language-specific encoders/decoders. It uses the encoders/decoders based on the tags supplied with the batch specification.
A new model is created for every language pair (this significantly slows the model down, but otherwise PyTorch throws *Not Enough Memory* error during backpropagation. This needs optimization?!) Gradients should be zeroed after every batch (not after every language pair), so that loss/gradients are accumulated.
