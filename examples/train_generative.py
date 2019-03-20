import argparse
import sentneuron as sn

parser = argparse.ArgumentParser(description='train_generative.py')

parser.add_argument('-data_path'  , type=str,   required=True,  help="Training dataset."       )
parser.add_argument('-data_type'  , type=str,   required=True,  help="Type of the training dataset: 'txt', 'midi_note', 'midi_chord' or 'midi_perform'." )
parser.add_argument('-embed_size' , type=int,   default=64   ,  help="Embedding layer size."   )
parser.add_argument('-hidden_size', type=int,   default=128  ,  help="Hidden layer size."      )
parser.add_argument('-n_layers'   , type=int,   default=1    ,  help="Number of LSTM layers."  )
parser.add_argument('-dropout'    , type=int,   default=0    ,  help="Dropout probability."    )
parser.add_argument('-epochs'     , type=int,   default=100  ,  help="Training epochs."        )
parser.add_argument('-seq_length' , type=int,   default=256  ,  help="Training batch size."    )
parser.add_argument('-lr'         , type=float, default=5e-4 ,  help="Learning rate."          )
parser.add_argument('-lr_decay'   , type=float, default=0.7  ,  help="Learning rate detay."    )
parser.add_argument('-grad_clip'  , type=int,   default=5    ,  help="Gradiant clipping value.")
parser.add_argument('-batch_size' , type=int,   default=128  ,  help="Batch size."             )
opt = parser.parse_args()

# Train a generative model to predict characters in a sequence
neuron, seq_data = sn.utils.train_generative_model(opt.data_path, opt.data_type, opt.embed_size, \
                                                   opt.hidden_size, opt.n_layers, opt.dropout, \
                                                   opt.epochs, opt.seq_length, opt.lr, \
                                                   opt.lr_decay, opt.grad_clip, opt.batch_size)

# Save trainned model for sampleing
dataset_name = opt.data_path.split("/")[-1]
neuron.save(seq_data, "../trained_models/" + dataset_name)
