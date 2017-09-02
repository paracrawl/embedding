import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.autograd import Variable


"""
    NOT ENOUGH MEMORY TO RUN THIS MODEL ON AZURE WITH DUMMY DATA

    The input is: <96,384,50> tensor                <batch_size,  sequence_len, word_embed_len>
        - BLSTM with 512 cells in each direction => <96,50,512> tensor
        - Context vectors are concatenated       => <96,50,1024>
        - Max Pooling across sequence            => <96,1024>

"""

SEQUENCE_LEN = 50
WORD_EMBED_LEN = 384
BATCH_LEN = 96
ENCODER_HIDDEN_LEN = 512
DECODER_HIDDEN_LEN = SEQUENCE_LEN * WORD_EMBED_LEN
SENTENCE_EMBED_LEN = 2 * ENCODER_HIDDEN_LEN

DROPOUT = 0.2
CLIPPING_THRESHOLD = 2
INIT_LEARNING_RATE = 0.01
LEARNING_RATE_DECAY = 0.9

BUILDING_BLOCKS = {}
for lang in ['en', 'fr', 'sp', 'ru', 'ar', 'zh']:
    print "Creating %s encoder/decoder" % lang
    hidden_enc_state = (torch.zeros(2, 1, ENCODER_HIDDEN_LEN).numpy(), torch.zeros(2, 1, ENCODER_HIDDEN_LEN).numpy())
    hidden_dec_state = (torch.zeros(2, 1, DECODER_HIDDEN_LEN).numpy(), torch.zeros(2, 1, DECODER_HIDDEN_LEN).numpy())
    BUILDING_BLOCKS[lang] = {'enc_state': hidden_enc_state, 'dec_state': hidden_dec_state}

class BLSTM(nn.Module):

    def __init__(self, encoder_state, decoder_state):
        super(BLSTM, self).__init__()

        # Encoder specification
        self.encoder = nn.LSTM(WORD_EMBED_LEN, ENCODER_HIDDEN_LEN, bidirectional=True, batch_first=True, dropout=0.2)
        self.encoder_hidden_state = (Variable(torch.from_numpy(encoder_state[0])), Variable(torch.from_numpy(encoder_state[1])))

        # Max-pooling specification
        self.max_pool = nn.MaxPool2d((SEQUENCE_LEN, 1), stride=(1,1))

	# Decoder specification
        self.decoder = nn.LSTM(SENTENCE_EMBED_LEN, DECODER_HIDDEN_LEN, bidirectional=False)
        self.decoder_hidden_state = (Variable(torch.from_numpy(decoder_state[0])), Variable(torch.from_numpy(decoder_state[1])))
        
    def forward(self, batch):
        print "\tForward pass (%s)" % src
        # ENCODER
	encoder_output, self.encoder_hidden_state = self.encoder(batch, self.encoder_hidden_state)

        # POOLING
        max_pool_output = self.max_pool(encoder_output)

        # DECODER
    	decoder_output, self.decoder_hidden_state = self.decoder(max_pool_output, self.decoder_hidden_state)
        decoder_output = decoder_output.view(BATCH_LEN, SEQUENCE_LEN, WORD_EMBED_LEN)

        return (decoder_output, self.encoder_hidden_state, self.decoder_hidden_state)

print ""
print "############################################"
print "                 LEARNING                   "
print "############################################"

# Artificial Random Data
batches    = [Variable(torch.randn((BATCH_LEN, SEQUENCE_LEN, WORD_EMBED_LEN))) for _ in xrange(10)]
src = 'en'
tgt = 'fr'
prev_perplexity = 99999


# Training (need rework for real data)
learning_rate = INIT_LEARNING_RATE
criterion = nn.MSELoss()
for epoch in xrange(100):
    for i in xrange(10):
        print "(E%d/%d:B%d/%d)" % (epoch, 100, i, len(batches))
        model = BLSTM(BUILDING_BLOCKS[src]['enc_state'], BUILDING_BLOCKS[tgt]['dec_state'])

        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        batch = batches[i]

        model.train(); optimizer.zero_grad()

        # Feeding new batch
        output, new_encoder_state, new_decoder_state = model(batch)
        BUILDING_BLOCKS[src]['enc_state'] = (new_encoder_state[0].data.numpy(), new_encoder_state[1].data.numpy())
        BUILDING_BLOCKS[tgt]['dec_state'] = (new_decoder_state[0].data.numpy(), new_decoder_state[1].data.numpy())

        # Calculating the loss
        loss = criterion(output, batch)
        print "\tBackpropagation"
        loss.backward()

        # Updating the weights
        print "\tUpdating the weights"
        optimizer.step()

        perplexity = np.exp(loss.data[0])
        print "\tPerplexity: %5.4f (was %5.4f)" % (perplexity, prev_perplexity)
        better = perplexity < prev_perplexity

        # Decrease learning rate if no improvement
        # (WARNING: this is performed on training data !!!)
        if not better and i > 0:
            learning_rate = learning_rate * LEARNING_RATE_DECAY
            optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
            print "\tPerplexity did not improve. New learning rate = %.4f" % (learning_rate)
        else:
            optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
            prev_perplexity = perplexity
