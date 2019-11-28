import torch
from torch.utils.data import IterableDataset, DataLoader
import csv
import torch.nn.functional as F

LOG_FILE = 'logs.txt'
FILENAME = 'full_dataset_bert_title_doc2vec_story.csv'
NUM_CATEGORIES = 19
IGNORE_COLS = ['url', 'story', 'title', 'first_cover_image', 'story_images']
Y_COLS = ['raised']
NUM_TEST = 30000
LIMIT = -1
BATCH_SIZE = 200
DEVICE = 'cuda'
LEARNING_RATE=0.01
HIDDEN_DIMS = [300, 300, 200, 100, 50, 25, 10]

class FundraisingDataset(IterableDataset):
    def __init__(self, file_name, skip=0, limit=-1):
        self.skipped = skip
        self.limit = limit
        self.n = 0

        self.csv_file = open(file_name, 'r')
        self.csv_reader = csv.reader(self.csv_file, delimiter=',')
        self.row0 = next(self.csv_reader)
        self.category_index = self.row0.index('category')
        self.num_cols = len(self.row0)
        self._skip_init()

    def _skip_init(self):
        for _ in range(self.skipped):
            next(self.csv_reader)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n != self.limit:
            self.n += 1
            return next(self.csv_reader)
        else:
            raise StopIteration

    def rewind(self):
        self.csv_file.seek(0)
        next(self.csv_reader)
        self._skip_init()

train_dataset = FundraisingDataset(FILENAME, skip=NUM_TEST)
EXPECTED_X_COLS = len(train_dataset.row0) - len(IGNORE_COLS) - 1 + NUM_CATEGORIES - len(Y_COLS)
EXPECTED_Y_COLS = len(Y_COLS)
device = torch.device(DEVICE)
log_file = open(LOG_FILE, 'ab+', buffering=0)

def generate_data(dataset, sample, batch_size):
    torch_x, torch_y = [], []
    for batch_index in range(batch_size):
        if len(sample) != dataset.num_cols:
            return None
        curr_x, curr_y = [], []
        for index, data in enumerate(sample):
            col_name = dataset.row0[index]
            if col_name in IGNORE_COLS:
                continue
            try:
                if col_name in Y_COLS:
                    curr_y.append(float(data[batch_index]))
                elif index == dataset.category_index:
                    category_onehot = [0. for _ in range(NUM_CATEGORIES)]
                    category_onehot[int(data[batch_index])] = 1.
                    curr_x.extend(category_onehot)
                else:
                    curr_x.append(float(data[batch_index]))
            except:
                return None
        if len(curr_x) != EXPECTED_X_COLS:
            raise RuntimeError('Expected {} data cols, found {} cols'.format(EXPECTED_X_COLS, len(curr_x)))
        if len(curr_y) != EXPECTED_Y_COLS:
            raise RuntimeError('Expected {} result cols, found {} cols'.format(EXPECTED_Y_COLS, len(curr_y)))
        torch_x.append(curr_x)
        torch_y.append(curr_y)
    
    x = torch.FloatTensor(torch_x).to(device)
    y = torch.FloatTensor(torch_y).to(device)
    return x, y 

log_file.write('Generating {} test samples.\n'.format(NUM_TEST).encode())
test_dataset = FundraisingDataset(FILENAME, limit=NUM_TEST)
test_data = []
for test_sample in DataLoader(test_dataset, batch_size=1):
    data = generate_data(test_dataset, test_sample, 1)
    if data is None:
        raise RuntimeError('Expected valid test data.')
    x, y = data
    test_data.append((x, y))
log_file.write('Generated test data.\n'.encode())

class MLP(torch.nn.Module):
    def __init__(self, hidden_dims=None):
        super(MLP, self).__init__()
        if hidden_dims is None or len(hidden_dims) == 0:
            hidden_dims = [100]

        self.input_layer = torch.nn.Linear(EXPECTED_X_COLS, hidden_dims[0])
        self.hidden_layers = torch.nn.ModuleList()
        for curr in range(1, len(hidden_dims)):
            self.hidden_layers.append(torch.nn.Linear(hidden_dims[curr - 1], hidden_dims[curr]))
        self.output_layer = torch.nn.Linear(hidden_dims[-1], EXPECTED_Y_COLS)
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        x = self.input_layer(x)
        x = self.relu(x)
        for layer in self.hidden_layers:
            x = layer(x)
            x = self.relu(x)
        return self.output_layer(x)

model = MLP(hidden_dims=HIDDEN_DIMS).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
loss_func = torch.nn.MSELoss()
log_file.write('Built model\n'.encode())

it = 0
for train_sample in DataLoader(train_dataset, batch_size=BATCH_SIZE):
    model.train()
    data = generate_data(train_dataset, train_sample, BATCH_SIZE)
    if data is None:
        continue
    x, y = data

    pred = model(x)
    train_loss = loss_func(pred, y)
    optimizer.zero_grad()
    train_loss.backward()
    optimizer.step()
    train_loss = train_loss.item()

    if it % 10 == 0:
        model.eval()
        test_loss = 0.0
        abs_loss = 0.0
        for x, y in test_data:
            pred_test = model(x)
            test_loss += loss_func(pred_test, y).item()
            abs_loss += F.l1_loss(pred_test, y).item()
        log_file.write('Iteration: {}, MSE train loss: {}, MSE test loss: {}, Absolute test loss: {}\n'.format(
            it, train_loss, test_loss, abs_loss).encode())
    it += 1

log_file.write('Finished.\n')
