import torch.nn as nn
class FcEncoder(nn.Module):
    def __init__(self, fc_num, input_size, output_size):
        super(FcEncoder, self).__init__()
        self.first_mlp = nn.Sequential(
                nn.Linear(input_size, output_size), nn.ReLU(), nn.LayerNorm(output_size)
            )
        self.mlp = nn.Sequential()
        for _ in range(fc_num - 1):
            self.mlp.append(nn.Sequential(
                nn.Linear(output_size, output_size), nn.ReLU(), nn.LayerNorm(output_size)
            ))

    def forward(self, x):
        output = self.first_mlp(x)
        return self.mlp(output)